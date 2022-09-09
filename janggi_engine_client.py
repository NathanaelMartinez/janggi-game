import struct
from socket import *
from errno import *
import sys
import pickle
import janggi_game

# set constants
HEADER_LENGTH = 8
ADDRESS = "localhost"
PORT = 7777

# 1. The client creates a socket and connects to ‘localhost’ and port xxxx
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect((ADDRESS, PORT))
print(f'Connected to: {ADDRESS} on port: {PORT}...')
client_socket.setblocking(False)


def send_game(game):
    """This function requests a move by the client and then sends the game to the server"""
    # get user input
    move = input('Your Move: ')

    # If the move is /q, the client quits
    if move and move == "/q":
        print(f'Closed connection to server on: {ADDRESS} on port: {PORT}...')

        # 8. Sockets are closedZ
        client_socket.close()
        sys.exit()

    if move:
        move_arr = move.split(',')
        # Player makes move
        game.make_move(move_arr[0], move_arr[1].strip())

        # Encode game to bytes, prepare header and convert to bytes, then send
        payload = pickle.dumps(game)
        # header needed to signal how much text to receive
        header = struct.pack('!Q', len(payload))
        # move_header = f"{len(move):<{HEADER_LENGTH}}".encode()

        packet = header + payload
        client_socket.send(packet)


def main():
    # When connected, the client prompts for a move to send
    print("Type /q to quit")

    # instantiate game
    game = janggi_game.JanggiGame()
    game.print_board()

    send_game(game)

    while True:
        try:
            while True:

                # Receive header containing move length, it's size is defined and constant
                header = client_socket.recv(HEADER_LENGTH)

                # If we received no data, server gracefully closed a connection
                if not len(header):
                    print('Connection closed by the server')

                    # make sure socket closed
                    client_socket.close()
                    sys.exit()

                # The client calls recv to receive data
                game_size = struct.unpack("!Q", header)[0]
                game = pickle.loads(client_socket.recv(game_size))

                # The client prints the board
                game.print_board()

                while game.get_game_state() == "unfinished":
                    send_game(game)

        except IOError as e:
            # catch errors from possible operating systems due to nonblocking socket
            if e.errno != EAGAIN and e.errno != EWOULDBLOCK:
                print('Reading error: {}'.format(str(e)))
                sys.exit()

            # We just did not receive anything
            continue

        except Exception as e:
            # Any other exception - something happened, exit
            print('Reading error: {}'.format(str(e)))
            sys.exit()


if __name__ == "__main__":
    main()