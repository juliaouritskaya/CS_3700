# Project 4: Reliable Transport Protocol

## High-Level Approach

This project implements a reliable transport protocol over an unreliable network, focusing on
handling packet corruption, loss, and efficiently managing network bandwidth. Our approach was 
to implement mechanisms similar to TCP, such as checksums for error detection, ACKs for 
confirmations, and dynamic window sizing for congestion control.

## Challenges Faced

- **Packet Corruption (Level 5 Tests)**: Tackled random packet corruption using checksum verification at both sender and receiver ends to ensure data integrity.
- **Dynamic Window Sizing (Level 7 Tests)**: Addressed the need for adaptive window sizing under varying bandwidths, especially in test 7-3 with high data volume, by implementing a New Reno-like congestion control strategy.
- **Debug Functionality**: Implementing reliable corruption detection and handling without a debug functionality was tedious and required extensive logging for troubleshooting.

## Design Features/Properties 

- **Reliability**: Ensure data integrity and delivery confirmation.
- **Efficiency**: Maximizes throughput by adapting window size according to network conditions. 
- **Scalability**: Robust across diverse network environments, including those with high loss and bandwidth.

## Testing Overview

Ran tests locally, relying on extensive logging to observe the protocol's behavior across different 
scenarios, focusing on addressing packet corruption and dynamic bandwidth utilization challenges. 