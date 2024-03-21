# Project 3: BGP Router

## High-Level Approach

This project implements a BGP Router that establishes connections with its peers, processes various types of 
incoming messages (such as route updates, data packets, and dump requests), and manages a forwarding table to make 
routing decisions. The router operates based on predefined relationships with its neighbors, including 
customers, peers, and providers, and utilizes this information along with the contents of the forwarding table 
to determine the next hop for outgoing traffic.

### Key Aspects 

- **Socket Management**: Each neighbor connection is managed through a separate UDP socket. This allows the router to handle messages from multiple neighbors at the same time.
- **Message Handling**: The router distinguishes between different types of messages (handshake, update, data, dump) and processes each accordingly. This includes updating the forwarding table based on route announcements, forwarding data packets to their destination, and responding to dump requests with the current state of the forwarding table. 
- **Forwarding Table Management**: The forwarding table is an important aspect that stores route information. The router implements logic to update this table based on received route announcements, including the application of BGP policies for route selection and transmission. 
- **Connection with Peers**: The router establishes and maintains connections with its peers, facilitating the exchange of routing information and ensuring network reachability.


## Challenges Faced

- **Debugging Limitations**: Traditional debugging methods were ineffective due to the event-driven nature of the router. Extensive print statements were used to trace message processing and execution flow.
- **Unexpected Message Errors**: Dealt with errors caused by unexpected or improperly formatted messages. Thorough code examination was necessary to ensure correct message parsing and handling.
- **Source and Destination Path Extraction**: Extracting accurate source and destination paths from incoming messages posed challenges in interpreting them for routing decisions.
- **Conditional Inclusion of Route Attributes**: Confusion arose regarding the handling of route attributes like local pref, selfOrigin, and origin during route update processing. Balancing compliance with BGP policies and accurate dump responses was essential.
- **Complexity in Level 2 Test Configurations**: Implementing the BGP path selection algorithm, considering multiple attributes like localpref, ASPath, and origin, proved challenging. Understanding of BGP policies and meticulous coding were required for correctness.
- **Integrating Longest Prefix Matching with BGP Attributes**: Balancing longest prefix match for route selection with evaluating BGP attributes like AS path length, local preference, and origin type was challenging. The logic had to ensure both aspects worked together to choose the best path.
- **Implementing Route Aggregation and Disaggregation**: Aggregation, combining adjacent numerical routes into a single entry, was challenging. Ensuring accurate aggregation while maintaining necessary BGP attributes and handling disaggregation after withdraw messages required careful design and implementation. Rebuilding the forwarding table post-withdrawal added complexity.

## Design Features/Properties 

- **Flexibility**: The code is split into separate methods for handling different types of messages, which makes it easier to understand, maintain, and modify.
- **Efficiency**: The code uses non-blocking sockets to selectively forward route updates based on BGP relationships.
- **Robustness**: The code includes error handling for JSON parsing to handle unexpected message types. 

## Testing Overview

The router was tested using the all the configuration files, each simulating different network topologies.
This included:

- **Neighbor Connection Establishment**: Verifying successful connection establishment with neighbors and correct management of multiple connections.
- **Route Update Processing**: Testing correct forwarding table updates based on received route announcements and adherence to BGP policies.
- **Data Message Forwarding**: Validating accurate forwarding of data messages to intended destinations based on the forwarding table.
- **Dump Request Handling**: Confirming generation of accurate forwarding table representations in response to dump requests.
- **Level 2 Test Configurations**: Ensuring adherence to BGP path selection algorithms, especially in scenarios with multiple route options.
- **Route Aggregation and Disaggregation**: Testing router capability to perform route aggregation and disaggregation based on adjacency and attributes.
- **Debugging and Validation**: Extensive print statements were used for debugging, and the router was validated against all provided configuration files to detect and correct errors.