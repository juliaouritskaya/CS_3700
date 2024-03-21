import re
import socket
from pathlib import Path


class FTPClient:
    """
    FTPClient handles communication with an FTP server, supporting operations like
    list directory, upload, download, delete, and manage directories.
    """

    def __init__(self, operation, params):
        """
        Initializes the FTPClient with a specific operation and parameters, then
        executes the operation against the FTP server.

        :param operation: The FTP operation to perform ('ls, 'rm', 'rmdir', 'mkdir', 'cp', 'mv').
        :param params: Parameters for the operation, such as paths or filenames.
        """
        self.server = "ftp.3700.network"
        self.port = 21
        self.operation = operation
        self.params = params

        # Establish control connection to the server
        self.control_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.control_socket.connect((self.server, self.port))

        # Read and print the server's greeting message
        print(self.read_response())

        # Parse URL to extract username, password, and path
        username, password, path = self.parse_url(operation, params)

        # Authenticate with the server using provided credentials
        print(self.send_command(f"USER {username}"))
        print(self.send_command(f"PASS {password}"))

        # Set TYPE, MODE, and STRU right after successful login
        self.send_type("I") # Binary mode for file transfer
        self.send_mode("S") # Stream mode
        self.send_stru("F") # File structure mode

        # Depending on operation, call the respective method
        if operation == 'cp' or operation == 'mv':
            if len(self.params) < 2:
                print("Error: 'cp' and 'mv' operations require two arguments.")
                exit(1)
            if operation == 'cp':
                self.send_cp(self.params[0], self.params[1])
            elif operation == 'mv':
                self.send_mv(self.params[0], self.params[1])
        elif operation == 'rm':
            if len(self.params) < 1:
                print("Error: 'rm' operation requires a file path.")
                exit(1)
            self.send_dele(path)
        elif operation == 'ls':
            self.send_ls(path)
        elif operation == 'mkdir':
            self.send_mkdir(path)
        elif operation == 'rmdir':
            self.send_rmdir(path)

        # Send QUIT before ending the program
        self.send_quit()

    def send_command(self, command):
        """
        Sends a command to the FTP server and returns the server's response.

        :param command: The FTP command to send.
        :return: The server's response to the command.
        """

        self.control_socket.sendall(f"{command}\r\n".encode())
        response = self.read_response()
        return response

    def read_response(self):
        """
        Reads the server's response to a previously sent command.

        :return: The server's response as a decoded string.
        """

        response = self.control_socket.recv(4096).decode()
        return response

    def send_ls(self, path="."):
        """
        Requests a listing of the directory contents from the FTP server at the specified path.

        Establishes a data channel by entering passive mode, then sends the LIST command
        to receive the directory contents.

        :param path: The path of the directory to list. Defaults to the current directory.
        """

        # Enter passive mode to initiate a data connection
        ip_address, port = self.enter_passive_mode()

        # Open a new socket for the data channel
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as data_socket:
            data_socket.connect((ip_address, port))
            # Send LIST command and print server's response to control channel command
            response = self.send_command(f"LIST {path}")
            print(response)
            # Read and print the directory listing from the data channel
            directory_listing = data_socket.recv(4096).decode()
            print(directory_listing)

    def send_mkdir(self, directory):
        """
        Sends a command to the FTP server to create a new directory at the specified path.

        Checks the server's response to determine if the directory was created successfully.

        :param directory: The path of the new directory to create on the server.
        """

        # Send MKD command to attempt to create the directory
        response = self.send_command(f"MKD {directory}")
        # Check if the directory was created successfully
        if response.startswith('257'):
            print(f"Directory '{directory}' created successfully.")
        else:
            print(f"Failed to create directory '{directory}'. Server response: {response}")

    def send_rmdir(self, directory):
        """
        Sends a command to the FTP server to remove the specified directory.

        Verifies the operation's success by checking the server's response.

        :param directory: The pat of the directory to remove from the server.
        """

        # Send RMD command to attempt to remove the directory
        response = self.send_command(f"RMD {directory}")
        # Check if the directory was removed successfully
        if response.startswith('250'):
            print(f"Directory '{directory}' removed successfully.")
        else:
            print(f"Failed to remove directory '{directory}'. Server response: {response}")

    def send_cp(self, source_path, destination_path):
        """
         Copies a file from source_path to destination_path. The operation varies
         whether the source or destination is located on the FTP server.

        :param source_path: The path of the source file. Can be a local path or an FTP URL.
        :param destination_path: The path where the file will be copied to. Can be a local path or an FTP URL.
        """

        # Determine if the operation is download or upload based on the source path format
        if source_path.startswith('ftp://'):
            # Parse URL to extract the FTP path and perform download if the source is on the FTP server
            username, password, path = self.parse_url('cp', [source_path, ''])
            self.send_retr(path, destination_path)
        else:
            # Parse URL to extract the FTP path and perform upload if the destination is on the FTP server
            username, password, path = self.parse_url('cp', [destination_path, ''])
            self.send_stor(source_path, path)

    def send_mv(self, source_path, destination_path):
        """
        Moves a file from source_path to destination_path. This involves copying
        and then deleting the original. The operation varies depending on the source location.

        :param source_path: The path of the source file. Can be a local path or an FTP URL.
        :param destination_path: The path where the file will be moved to. Can be a local path or an FTP URL.
        """

        if source_path.startswith('ftp://'):
            # For FTP source, download the file then delete it from the FTP server
            username, password, path = self.parse_url('cp', [source_path, ''])
            self.send_retr(path, destination_path)
            self.send_dele(path)
        else:
            # For local source, upload the file then delete it locally
            username, password, path = self.parse_url('cp', [destination_path, ''])
            self.send_stor(source_path, path)
            Path(source_path).unlink()  # Corrected usage

    def enter_passive_mode(self):
        """
        Initiates passive mode, requesting the FTP server to open a port for data transfer.
        Parses the server's response to extract the IP address and port number for the data connection.

        :return: A tuple containing the IP address and port number for the data connection.
        """

        # Send PASV command to the server
        response = self.send_command("PASV")
        print("PASV Response:", response)

        # Extract the IP address and port from the response
        pasv_response_regex = r"(\d+),(\d+),(\d+),(\d+),(\d+),(\d+)"
        match = re.search(pasv_response_regex, response)
        if match:
            ip_parts = match.groups()[:4]
            port_parts = match.groups()[4:6]

            # The first four numbers are concatenated to form the IP address
            ip_address = '.'.join(ip_parts)
            # The last two numbers are used to calculate the port number
            port = (int(port_parts[0]) * 256) + int(port_parts[1])

            print(f"Data connection info - IPL {ip_address}, Port: {port}")
            return ip_address, port
        else:
            print("Could not parse PASV response.")
            return None, None

    def send_type(self, type_code="I"):
        """
        Sets the transfer type for the FTP session. 'I' for binary mode, 'A' for ASCII mode.

        :param type_code: 'I' for binary mode or 'A' for ASCII mode.
        """

        response = self.send_command(f"TYPE {type_code}")
        print(response)

    def send_mode(self, mode="S"):
        """
        Sets the transfer mode for the FTP session. 'S' for Stream mode.

        :param mode: 'S' for Stream mode.
        """

        response = self.send_command(f"MODE {mode}")
        print(response)

    def send_stru(self, structure="F"):
        """
        Sets the file structure for the FTP session. 'F' for File structure.

        :param structure: 'F' for File Structure.
        """

        response = self.send_command(f"STRU {structure}")
        print(response)

    def send_quit(self):
        """
        Sends the QUIT command to the FTP server, which terminates the session.
        """

        response = self.send_command("QUIT")
        print(response)

    def send_stor(self, local_file_path, remote_file_path):
        """
        Uploads a file to the FTP server by first entering passive mode to open a data channel,
        then sending the STOR command along with the file data.

        :param local_file_path: The path to the local file to be uploaded.
        :param remote_file_path: The path on the FTP server where the file will be stored.
        """

        # Check if the local file exists before attempting to upload
        if not Path(local_file_path).exists():
            print(f"Error: File {local_file_path} does not exist.")
            return

        # Enter passive mode to initiate data transfer
        ip_address, port = self.enter_passive_mode()

        # Open data channel connection to the server
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as data_socket:
            data_socket.connect((ip_address, port))

            # Send STOR command through control channel to notify the server of the file to be uploaded
            self.send_command(f"STOR {remote_file_path}")

            # Open the local file and read its contents
            with open(local_file_path, 'rb') as file:
                # Send file contents in chunks to the server
                data = file.read(4096)
                while data:
                    data_socket.sendall(data)
                    data = file.read(4096)

    def send_retr(self, remote_file_path, local_file_path):
        """
        Downloads a file from the FTP server by opening a data channel after entering passive mode,
        then using the RETR command to receive the file data.

        :param remote_file_path: The path on the FTP server to the file to be downloaded.
        :param local_file_path: The path where the downloaded file will be saved lcoally.
        """

        # Enter passive mode to prepare for data transfer
        ip_address, port = self.enter_passive_mode()  # Enter passive mode to get data channel details

        # Open data channel connection for the file transfer
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as data_socket:
            data_socket.connect((ip_address, port))

            # Send RETR command through control channel to request the file from the server
            self.send_command(f"RETR {remote_file_path}")

            # Open or create the local file to save the downloaded data
            with open(local_file_path, 'wb') as file:
                # Receive file data in chunks from the server and write locally
                while True:
                    data = data_socket.recv(4096)
                    if not data: # If no more data is received, break the loop
                        break
                    file.write(data)

    def send_dele(self, file_path):
        """
        Sends a DELE command to the FTP server to delete a specified file, using the control channel for the command.

        :param file_path: The path of the file on the FTP server to be deleted.
        """

        # Send DELE command through control channel and wait for response
        self.send_command(f"DELE {file_path}")

    def parse_url(self, operation, params):
        """
        Parses an FTP URL to extract the username, password, and path components.
        Used primarily for operations involving URLs, like 'cp' and 'mv'.

        :param operation: The operation being performed, affecting how URLs are parsed.
        :param params: A list of parameters for the operation, expected to include at elast one URL.
        :return: A tuple containing the username, password, and pth extracted from the URL.
        """

        url = ''

        # Determine the appropriate URL to parse based on the operation
        if operation == 'cp' or operation == 'mv':
            if params[0].startswith('ftp://'):
                url = params[0]
            else:
                url = params[1]
        else:
            url = params[0]

        # Remove the scheme part of the URL ('ftp://')
        url_body = url[6:]

        # Extract username by splitting at the first ':' and taking the first part
        username = url_body.split(':')[0]

        # Extract password and the rest of the URL after username
        password_and_path = url_body.split(':')[1]

        # Further split to separate password from path
        password = password_and_path.split('@')[0]

        # Ensure path starts with '/' or assign '/' as default
        if '/' in password_and_path:
            index = password_and_path.index('/')
            path = password_and_path[index:]
        else:
            path = '/'

        return username, password, path

