# Project 2: FTP Client 

## High-Level Approach

This project implements a basic FTP client in Python capable of interacting with an FTP server to perform operations 
such as listing directories, uploading, downloading, deleting files, and managing directories. 
The client uses a command-line interface for operation execution, including support for standard FTP operations like 
`ls`, `rm`, `rmdir`, `mkdir`, `cp`, and `mv`.

The development process involved:

- Establishing a control connection to the FTP server using sockets.
- Implementing command parsing to handle different FTP operations.
- Managing data transfer through a separate data channel in passive mode.
- Creating a URL parsing mechanism to extract credentials and paths from FTP URLs.

## Challenges Faced

### Timeout Errors on GradeScope

Encountered timeout errors when running the client on GradeScope, which were challenging to diagnose. 
This required careful debugging to identify which operations were causing the timeouts 
and under what circumstances they occurred.

### Authentication Issues

Initially, the client was designed to use hardcoded credentials for connecting to the FTP server. 
However, when integrating with GradeScope, I realized that a more flexible solution was needed 
to support dynamic authentication. This led to the development of the `parse_url` function, which extracts the username, password, and path from FTP URLs.

### Data Channel Management

Correctly managing the data channel for file transfers presented several challenges, 
especially in ensuring that the channel was properly opened and closed for each operation 
and that data transfers were correctly initiated and terminated.

## Testing Overview

Testing was conducted primarily through the command line, using a series of manual tests to validate each FTP operation. 
This involved:

- Creating empty text files and directories to serve as test data.
- Executing each operation (e.g., `ls`, `mkdir`, `cp`, `mv`) and verifying the outcomes both locally and on the FTP server.
- Using print statements to track the flow of commands and responses between the client and the server, ensuring that operations were executed as expected.
