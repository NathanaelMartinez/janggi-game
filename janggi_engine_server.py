from socket import *
from select import *
import sys
import pickle
import janggi_game

# set constants
HEADER_LENGTH = 10
ADDRESS = "localhost"
PORT = 7777

# The server creates a socket and binds to ‘localhost’ and port xxxx
server_socket = socket(AF_INET, SOCK_STREAM)

# so no hanging occurs when testing
server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
server_socket.bind((ADDRESS, PORT))

# The server then listens for a connection
server_socket.listen(1)
print(f'Server listening on: {ADDRESS} on port: {PORT}...')

# select will use these to make subsets
sockets_list = [server_socket]


def receive_message(client_socket):
    """This function receives messages from the client and returns False if an error occurs"""
    try:
        message_header = client_socket.recv(HEADER_LENGTH)

        if not len(message_header):
            return False

        # get header to know how much to receive
        message_length = int(message_header.decode().strip())

        return {'header': message_header, 'data': client_socket.recv(message_length)}

    except Exception:
        return False


def send_reply(write_sockets):
    """This function sends a message to the client and returns False if an error occurs"""
    # iterate over read_sockets
    for socket in write_sockets:
        # get user input
        message = input('> ')

        # If message is not empty - send it
        if message:
            # Encode message to bytes, prepare header and convert to bytes, then send
            message = message.encode()
            message_header = f"{len(message):<{HEADER_LENGTH}}".encode()
            socket.send(message_header + message)


def main():
    while True:
        # get read and exception sockets - pass write_sockets
        read_sockets, write_sockets, exception_sockets = select(sockets_list, sockets_list, sockets_list)

        # iterate over read_sockets
        for socket in read_sockets:

            # if socket is a server socket - new connection, accept it
            if socket == server_socket:

                # accept new connection
                client_socket, client_address = server_socket.accept()

                # add client socket to socket_list
                sockets_list.append(client_socket)

                print("Connected by ('{}',:{})".format(*client_address))

            # Else existing socket is sending a message
            else:
                print("Waiting for first move...")
                # When connected, the server calls recv to receive data
                message = receive_message(socket)

                # If the reply is /q (there will be no message received, client exited), the server quits
                if not message:
                    print(f'Closed connection from: {sockets_list[1].getpeername()}')

                    # Remove from sockets_list for socket() at start of loop
                    sockets_list.remove(socket)

                    # make sure socket closed
                    socket.close()

                    # wait for another client
                    # continue

                # The server prints the data, then prompts for a reply
                print(f'{message["data"].decode()}')


                # board = receive_message(socket)
                # Otherwise, the server sends the reply
                send_reply(write_sockets)


if __name__ == "__main__":
    main()
