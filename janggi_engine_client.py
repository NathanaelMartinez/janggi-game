from socket import *
from errno import *
import sys
import pickle
import janggi_game

# set constants
HEADER_LENGTH = 10
ADDRESS = "localhost"
PORT = 7777

# 1. The client creates a socket and connects to ‘localhost’ and port xxxx
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect((ADDRESS, PORT))
print(f'Connected to: {ADDRESS} on port: {PORT}...')
client_socket.setblocking(False)

def validate_move(move):
    valid_columns = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
    valid_rows = ['1', '2', '3', '4', '5', '6', '7', '8', '9']

    if move == '/q':
        return True

    if ',' not in move:
        return False

    split_coords = move.split(',')

    for coord in split_coords:
        coord = coord.strip()

        if coord == '':
            return False

        if coord[0].upper() not in valid_columns:
            return False

        if (coord[1] not in valid_rows) or (len(coord) > 2 and coord[2] > 0):
            return False

    return True


def send_move():
    """This function requests a move by the client and then sends the game to the server"""
    # get user input
    move = input('Your Move: ')
    if not validate_move(move):
        print("Please enter your move as 'source coordinate (column row), destination coordinate (column row)'")
        send_move()

    # 3. If the move is /q, the client quits
    if move and move == "/q":
        print(f'Closed connection to server on: {ADDRESS} on port: {PORT}...')

        # 8. Sockets are closedZ
        client_socket.close()
        sys.exit()

    # 4. Otherwise, the client sends the game
    if move:
        # Encode game to bytes, prepare header and convert to bytes, then send
        move = move.encode()
        # header needed to signal how much text to receive
        move_header = f"{len(move):<{HEADER_LENGTH}}".encode()
        client_socket.send(move_header + move)


def main():
    # When connected, the client prompts for a move to send
    print("Type /q to quit")

    # instantiate game
    game = janggi_game.JanggiGame()
    game.print_board()

    send_move()

    while True:
        try:
            while True:

                # Receive header containing move length, it's size is defined and constant
                move_header = client_socket.recv(HEADER_LENGTH)

                # If we received no data, server gracefully closed a connection
                if not len(move_header):
                    print('Connection closed by the server')

                    # make sure socket closed
                    client_socket.close()
                    sys.exit()

                # The client calls recv to receive data
                move_length = int(move_header.decode().strip())
                move = client_socket.recv(move_length).decode()

                # The client prints the data
                print(f'{move}')

                # Back to step 2
                send_move()

        except IOError as e:
            # catch errors from possible operating systems due to nonblocking socket
            if e.errno != EAGAIN and e.errno != EWOULDBLOCK:
                print('Reading error: {}'.format(str(e)))
                sys.exit()

            # We just did not receive anything
            continue

        except Exception as e:
            # Any other exception - something happened, exit
            print('Reading error: '.format(str(e)))
            sys.exit()


if __name__ == "__main__":
    main()