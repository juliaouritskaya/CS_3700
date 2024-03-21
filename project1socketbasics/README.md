# Project 1: Socket Basics

## Project Overview
This project involves the development of a client program that plays a variant of the recently-popular game Wordle 
over network sockets. The client communicates with a server to make guesses for the secret word, and receives information
on how close the guess is.

## High-Level Approach
The client is implemented in Python and uses TCP sockets for communication with the server. It supports both 
non-encrypted and TLS-encrypted connections. The main functionalities include sending a "hello" message to
initiate the game, making word guesses, and handling server responses.

## Challenges Faced
One significant challenge encountered was related to the socket connection management. Initially, the client was opening 
and closing a new socket connection for each message sent to the server. This behavior led to the server perceiving each
message as coming from a new client session, particularly evident when the server repeatedly expected a "hello" message 
after each guess. This issue was resolved after realizing the necessity of maintaining a persistent socket connection 
throughout the session, ensuring consistent communication with the server. 

## Guessing Strategy
The client implements an intelligent strategy for guessing words based on the feedback (marks) received from the server. The approach involves:

- **Initial Guess**: The client starts with a random guess selected from the provided word list.

- **Feedback Analysis**: After each guess, the server returns feedback marks for each letter in the guessed word, indicating:
    - `2`: The letter is in the word and in the correct position.
    - `1`: The letter is in the word but in the wrong position.
    - `0`: The letter is not in the word.

- **Word List Refinement**:
    - Based on the feedback, the `refine_word_list` function refines the list of potential words:
        - If a letter in the guess is marked `2`, the function includes only words with that letter in the same position.
        - If a letter is marked `1`, it includes words containing the letter but excludes those with the letter in the guessed position.
        - Letters marked `0` are excluded from all future guesses.
    - This refinement narrows down the possibilities, making each subsequent guess more informed.

- **Selecting the Next Guess**: 
    - The `choose_next_guess` function then selects the next guess from the refined list of potential words. If no guesses have been made yet, it chooses a random word.
    - As the game progresses, the word list becomes increasingly refined based on accumulated feedback, making guesses more accurate.

This strategy efficiently narrows down the potential words with each guess, leading to a quick and effective discovery of the secret word.


## Testing Overview
The client was thoroughly tested by running it against the server under various scenarios:
- Ensuring the correct handling of the initial "hello" message and game initiation.
- Verifying that the guessing strategy adapts based on server feedback.
- Testing both non-encrypted and TLS-encrypted connections.
- Confirming the proper handling of server responses, including "retry" and "bye" messages.
