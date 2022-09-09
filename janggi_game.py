import sys
import os
from janggi_pieces import *


class JanggiGame:
    """
    Represents a virtual version of the board game, Janggi. The 9x10 board is populated with 16 pieces on each side to
    represent the pieces of each player. The pieces consist of 7 types, all with their own set of legal moves.
    The objective of the game is for a player to use their pieces to put their opponent's general in checkmate.
    This class sets the board and controls the game flow. In doing so, it must communicate with the GamePiece
    class that represents the pieces on the board
    """

    def __init__(self):
        """
        Initializes the board game with the pieces in the correct spots, sets the game as unfinished, and
        sets the turn to the Cho (Blue) player. Must communicate with the GamePiece class to populate the board
        and to move the pieces in the board.
        """

        self._current_state = "UNFINISHED"
        self._pieces = self.initialize_pieces()
        self._board = self.place_pieces(self._pieces)
        self._turn = "Blue"
        self._check = ""

    def get_game_state(self):
        """Returns the current state of the game (the game is unfinished, or which player has won)"""
        return self._current_state

    def set_game_state(self, color):
        """Modifies the game state to declare a winner. Called by checkmate check when a color is put in checkmate"""

        if color == "Blue":
            winner = "Red"
        else:
            winner = "Blue"

        self._current_state = winner.upper() + "_WON"

    def get_check_state(self):
        """Returns the check state of player"""
        return self._check

    def set_check_state(self, color):
        """
        Takes a color and puts them in check, forcing that color to move their general in the next turn. If they
        cannot, then the game ends in a checkmate and victory for the aggressor
        """
        self._check = color

    def get_turn(self):
        """Returns the color of whose turn it is"""
        return self._turn

    def get_next_turn(self):
        """Returns the color of the player whose turn is next"""
        if self.get_turn() == "Blue":
            return "Red"
        else:
            return "Blue"

    def is_in_check(self, color):
        """
        takes as a parameter either 'red' or 'blue' and returns True if that player is in check, but returns False
        otherwise.
        """

        if self.get_check_state().upper() == color.upper():
            print("game.is_in_check('" + color + "')  # returns True")
            return True

        print("game.is_in_check('" + color + "')  # returns False")
        return False

    def check_check(self, color):
        """
        Takes a color and finds if that color's general can be threatened by an opposing player's piece. It does so by
        calling a helper function to find the general's location and then iterates through the game board to find all
        pieces of the opposing color and iterates through them to see if they can reach the general by checking all
        their possible moves with the method move_check(). If any can, check_check() returns True, otherwise, it
        returns False
        """

        if color == "Blue":
            opposing_color = "Red"
        else:
            opposing_color = "Blue"

        (general_column, general_row) = self.get_general_coords(color)

        for coordinate in self.get_board():
            piece = self.get_piece_by_coordinate(coordinate[0], coordinate[1])
            if (piece is not None) and (piece.get_color() == opposing_color):
                # test possible moves
                if self.move_check(piece.get_column(), piece.get_row(), general_column, general_row):
                    return True
        return False

    def checkmate_check(self, color):
        """
        Takes a color and checks if any possible move will not end in check. It does so by making a copy of the board
        that can be reverted to if need be, then it iterates through the board and finds every piece of the given color.
        The method then sends the piece and all positions on the board to a helper function, will_move_end_check()
        that determines if any piece can move in such a way that does not end in check. If such a move exists and that
        helper function returns True, then checkmate_check() returns False, meaning there is no checkmate.
        """
        board = self.get_board().copy()

        for coordinate in board:
            piece = self.get_piece_by_coordinate(coordinate[0], coordinate[1])
            if (piece is not None) and (piece.get_color() == color):
                for x in range(9):
                    for y in range(10):
                        if self.will_move_end_check(piece, x, y):
                            return False

        return True

    def will_move_end_check(self, piece, x, y):
        """
        Helper method for checkmate_check(). Is fed the pieces of a specific color in a loop along with all positions
        on the board and checks if each piece can move in such a way that doesn't result in check. It does so by calling
        move_check() to find if there are any valid movements, then calls move_piece() to move the pieces there and then
        calls check_check() to see if those moves result in a situation such that that color is not in check. If such
        a move doesn't exist, then this method returns False and therefore, checkmate is True.
        """

        if self.move_check(piece.get_column(), piece.get_row(), x, y):
            pre_x = piece.get_column()
            pre_y = piece.get_row()
            self.move_piece(piece, pre_x, pre_y, x, y)
            out_of_check = not self.check_check(piece.get_color())
            self.move_piece(piece, x, y, pre_x, pre_y)
            return out_of_check
        return False

    def get_general_coords(self, color):
        """
        Helper method for check_check(). Returns general's location on the board. It does so by iterating through the
        board and finding pieces that correspond to the General class and then determines if the color is the same as
        the one that was fed to the method. Once found, the General's location is then returned to check_check()"""
        for coordinate in self.get_board():
            piece = self.get_piece_by_coordinate(coordinate[0], coordinate[1])
            if piece is not None:
                if (type(piece) == General) and piece.get_color() == color:
                    return [piece.get_column(), piece.get_row()]

    def move_check(self, source_column, source_row, dest_column, dest_row):
        """
        Makes sure a piece located at the source coordinates can move to the destination coordinates. It does so by
        retrieving the piece at the given source coordinates and then determines the type of that piece. Then the
        piece is sent to a specific set of rules for that type of piece. Then the piece is sent that piece type's
        move-set. If the piece is attempting a move that does not follow those rules or its move-set, this method
        returns False, otherwise, if the move is valid, it returns True.
        """

        piece = self.get_piece_by_coordinate(source_column, source_row)

        piece_type = type(piece)

        if piece_type == Horse:
            if not self.make_horse_move(source_column, source_row, dest_column, dest_row):
                return False

        if piece_type == Chariot:
            if not self.make_chariot_move(source_column, source_row, dest_column, dest_row):
                return False

        if piece_type == Elephant:
            if not self.make_elephant_move(source_column, source_row, dest_column, dest_row):
                return False

        if piece_type == Cannon:
            if not self.make_cannon_move(source_column, source_row, dest_column, dest_row):
                return False

        if piece_type == General:
            if not self.make_general_move(source_column, source_row, dest_column, dest_row):
                return False

        if piece_type == Guard:
            if not self.make_guard_move(source_column, source_row, dest_column, dest_row):
                return False

        if piece_type == Soldier:
            if not self.make_soldier_move(source_column, source_row, dest_column, dest_row):
                return False

        if not piece.is_legal_move(dest_column, dest_row):
            return False

        return True

    def get_board(self):
        """Returns game board dictionary"""
        return self._board

    @staticmethod
    def initialize_pieces():
        """
        Initializes GamePiece class objects in a dictionary in their appropriate starting positions and assigns them
        each to a player
        """
        pieces = {
            Chariot("Red", 0, 0), Elephant("Red", 1, 0), Horse("Red", 2, 0), Guard("Red", 3, 0), General("Red", 4, 1),
            Guard("Red", 5, 0), Elephant("Red", 6, 0), Horse("Red", 7, 0), Chariot("Red", 8, 0),
            Cannon("Red", 1, 2), Cannon("Red", 7, 2),
            Soldier("Red", 0, 3), Soldier("Red", 2, 3), Soldier("Red", 4, 3), Soldier("Red", 6, 3),
            Soldier("Red", 8, 3),
            Soldier("Blue", 0, 6), Soldier("Blue", 2, 6), Soldier("Blue", 4, 6), Soldier("Blue", 6, 6),
            Soldier("Blue", 8, 6),
            Cannon("Blue", 1, 7), Cannon("Blue", 7, 7),
            Chariot("Blue", 0, 9), Elephant("Blue", 1, 9), Horse("Blue", 2, 9), Guard("Blue", 3, 9),
            General("Blue", 4, 8), Guard("Blue", 5, 9), Elephant("Blue", 6, 9), Horse("Blue", 7, 9),
            Chariot("Blue", 8, 9)
        }
        return pieces

    @staticmethod
    def place_pieces(pieces, game_board=None):
        """
        Initializes a new game.
        Takes dictionary of pieces and enters each one into the board dictionary.
        """
        if game_board is None:
            game_board = {}
        for piece in pieces:
            game_board[piece.get_column(), piece.get_row()] = piece
        return game_board

    def toggle_turn(self):
        """Toggles whose turn it is"""
        if self._turn == "Blue":
            self._turn = "Red"
        elif self._turn == "Red":
            self._turn = "Blue"

    @staticmethod
    def get_coordinates(algebraic):
        """Helper method for make_move(). Returns coordinates in a usable x, y format from coordinates entered in
        algebraic notation"""
        alpha = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']  # 9 columns
        nums = [str(num) for num in range(1, 11)]  # 10 rows
        return [alpha.index(algebraic[0].upper()), nums.index(algebraic[1:])]

    def get_piece_by_coordinate(self, column, row):
        """Returns piece on the board at the given coordinates"""
        keys = sorted(self.get_board().keys())
        for key in keys:
            if key[0] == column and key[1] == row:
                if self.get_board()[key] is not None:
                    return self.get_board()[key]

        return None

    def move_piece(self, piece, source_column, source_row, dest_column, dest_row):
        """
        Moves a given piece within the board dictionary by removing it from its source coordinates and then
        saves it in the new location by calling the piece's set_column() and set_row() functions with the given
        destination coordinates
        """
        self.get_board()[source_column, source_row] = None
        piece.set_column(dest_column)
        piece.set_row(dest_row)
        self.get_board()[dest_column, dest_row] = piece

    def print_board(self):
        """
        Prints the board for the user so that the game can be visualized at certain points. Called after each
        move is made
        """
        print()
        print("  |   A   |   B   |   C   |   D   |   E   |   F   |   G   |   H   |   I   ", end="")
        rows = ["1 ", "2 ", "3 ", "4 ", "5 ", "6 ", "7 ", "8 ", "9 ", "10"]

        for row in range(10):
            print('|')
            print('-' * 75)
            print(rows[row], end='')

            for column in range(9):
                piece = self.get_piece_by_coordinate(column, row)

                if piece is None:
                    print('|  ---  ', end='')
                else:
                    symbol = self.get_piece_by_coordinate(column, row).get_symbol()
                    print('|   ' + symbol, end='   ')

        print('|')
        print('-' * 75)

        print()
        print(self.get_game_state())
        print()
        print(self.get_turn() + "'s turn")
        print()

    def make_move(self, alg_source, alg_destination):
        """
        Takes a source square and a destination square in algebraic notation and then converts that into a usable
        format by calling get_coordinates(). The method then takes the piece at the given source by calling
        get_piece_by_coordinate and then moves that piece to the specified destination coordinates. If the piece is
        unable to perform the move legally, is not of the player in question, or if the game is over, it returns False.
        Otherwise, it updates the turn to the next player and returns True. The method calls methods such as
        move_check(), check_check(), and checkmate_check() to determine if the move is legal or not or if a check or
        checkmate has occurred and then updates the status of self._check or self._current_status by calling their
        setter methods to declare a check or a winner of the game. If move_check() is passed and True is returned, then
        the pieces are updated in the board dictionary with move_piece() and the turn is toggled with the toggle_turn()
        method.
        The method also allows the player to skip their turn by entering the same coordinates for destination and their
        entered source.
        """

        if str(alg_source) == str(alg_destination):  # player passes turn
            if self.get_check_state() != self.get_turn():
                print()
                print("Turn Passed")
                print()
                self.toggle_turn()
                print(str(self.get_turn()) + "'s turn")
                print()
                return True
            else:
                return False

        source = self.get_coordinates(alg_source)
        source_column = source[0]
        source_row = source[1]

        destination = self.get_coordinates(alg_destination)
        dest_column = destination[0]
        dest_row = destination[1]

        print("game.make_move('" + str(alg_source) + "', '" + str(alg_destination) + "')")
        print("game.print_board()")

        piece = self.get_piece_by_coordinate(source_column, source_row)

        if self.get_game_state() != "UNFINISHED":
            return False

        if piece is None:  # if no piece at location
            print("No piece selected, try again")
            return False

        piece_color = piece.get_color()
        if piece_color != self.get_turn():
            print("Piece not your color. Try again")
            return False

        if self.move_check(source_column, source_row, dest_column, dest_row) is False:
            return False

        self.move_piece(piece, piece.get_column(), piece.get_row(), dest_column, dest_row)
        if self.check_check(self.get_turn()):
            self.move_piece(piece, piece.get_column(), piece.get_row(), source_column, source_row)
            return False

        self.set_check_state("")
        self.toggle_turn()
        if self.check_check(self.get_turn()):
            # opponent in check
            self.set_check_state(self.get_turn())

        if self.is_in_check(self.get_turn()):
            if self.checkmate_check(self.get_turn()):
                self.set_game_state(self.get_turn())
                return False

        return True

    def make_horse_move(self, source_column, source_row, dest_column, dest_row):
        """
        Helper to move_check(). Determines the rules for the Horse piece. The Horse can be blocked by having a friendly
        piece in the destination or by having a piece in the first space on the way to the destination
        """
        # blockers
        front_piece = self.get_piece_by_coordinate(source_column, source_row - 1)
        back_piece = self.get_piece_by_coordinate(source_column, source_row + 1)
        left_piece = self.get_piece_by_coordinate(source_column - 1, source_row)
        right_piece = self.get_piece_by_coordinate(source_column + 1, source_row)

        # move-set
        move_up = (source_row - 2)
        move_down = (source_row + 2)
        diag_right = (source_column + 1)
        diag_left = (source_column - 1)

        move_left = (source_column - 2)
        move_right = (source_column + 2)
        diag_up = (source_row - 1)
        diag_down = (source_row + 1)

        # can't jump on friendly piece
        if self.empty_or_enemy(source_column, source_row, dest_column, dest_row) is False:
            return False

        if not front_piece and ((dest_column == diag_right or dest_column == diag_left) and dest_row == move_up):
            return True

        if not back_piece and ((dest_column == diag_right or dest_column == diag_left) and dest_row == move_down):
            return True

        if not left_piece and ((dest_column == move_left) and (dest_row == diag_up or dest_row == diag_down)):
            return True

        if not right_piece and ((dest_column == move_right) and (dest_row == diag_up or dest_row == diag_down)):
            return True

        return False

    def make_chariot_move(self, source_column, source_row, dest_column, dest_row):
        """
        Helper to move_check(). Determines rules for the Chariot piece. Chariots can move in a straight line over the
        whole board - given that it is unobstructed.
        """

        smaller_column = min(source_column, dest_column)
        larger_column = max(source_column, dest_column)
        smaller_row = min(source_row, dest_row)
        larger_row = max(source_row, dest_row)

        # can't take friendly pieces
        if self.empty_or_enemy(source_column, source_row, dest_column, dest_row) is False:
            return False

        # destination must be unobstructed
        for space in range(smaller_column + 1, larger_column):
            if self.get_piece_by_coordinate(space, source_row) is not None:
                return False

        for space in range(smaller_row + 1, larger_row):
            if self.get_piece_by_coordinate(source_column, space) is not None:
                return False

        return True

    def make_elephant_move(self, source_column, source_row, dest_column, dest_row):
        """
        Helper to move_check(). Determines rules for Elephant piece. An elephant can be blocked if there is a piece
        in the first space in the direction it wants to move and then if there is a piece in the block immediately
        diagonal to that one in the direction it wants to move. Destination space cannot be occupied by a friendly piece
        """

        # piece immediately in front
        front_piece = self.get_piece_by_coordinate(source_column, source_row - 1)

        # piece in front and then diagonally to the right
        front_diagonal_r = self.get_piece_by_coordinate(source_column + 1, source_row - 2)

        # piece in front and then diagonally to the left
        front_diagonal_l = self.get_piece_by_coordinate(source_column - 1, source_row - 2)

        # piece immediately behind
        back_piece = self.get_piece_by_coordinate(source_column, source_row + 1)

        # piece behind and then diagonally to the right
        back_diagonal_r = self.get_piece_by_coordinate(source_column + 1, source_row + 2)

        # piece behind and then diagonally to the left
        back_diagonal_l = self.get_piece_by_coordinate(source_column - 1, source_row + 2)

        # piece immediately to the player's left
        left_piece = self.get_piece_by_coordinate(source_column - 1, source_row)

        # piece left and then diagonally up
        left_diagonal_u = self.get_piece_by_coordinate(source_column - 2, source_row - 1)

        # piece left and then diagonally down
        left_diagonal_d = self.get_piece_by_coordinate(source_column - 2, source_row + 1)

        # piece immediately to the player's right
        right_piece = self.get_piece_by_coordinate(source_column + 1, source_row)

        # piece right and then diagonally up
        right_diagonal_u = self.get_piece_by_coordinate(source_column + 2, source_row - 1)

        # piece right and then diagonally down
        right_diagonal_d = self.get_piece_by_coordinate(source_column + 2, source_row + 1)

        move_up = (source_row - 3)
        move_down = (source_row + 3)
        diag_right = (source_column + 2)
        diag_left = (source_column - 2)

        move_left = (source_column - 3)
        move_right = (source_column + 3)
        diag_up = (source_row - 2)
        diag_down = (source_row + 2)

        # space must be empty
        if self.empty_or_enemy(source_column, source_row, dest_column, dest_row) is False:
            return False

        if not (front_piece or front_diagonal_r) and (dest_row == move_up and dest_column == diag_right):
            return True

        if not (front_piece or front_diagonal_l) and (dest_row == move_up and dest_column == diag_left):
            return True

        if not (back_piece or back_diagonal_r) and (dest_row == move_down and dest_column == diag_right):
            return True

        if not (back_piece or back_diagonal_l) and (dest_row == move_down and dest_column == diag_left):
            return True

        if not (left_piece or left_diagonal_u) and (dest_column == move_left and dest_row == diag_up):
            return True

        if not (left_piece or left_diagonal_d) and (dest_column == move_left and dest_row == diag_down):
            return True

        if not (right_piece or right_diagonal_u) and (dest_column == move_right and dest_row == diag_up):
            return True

        if not (right_piece or right_diagonal_d) and (dest_column == move_right and dest_row == diag_down):
            return True

        return False

    def make_cannon_move(self, source_column, source_row, dest_column, dest_row):
        """
        Helper to move_check(). Determines rules for Cannon piece. Cannon moves like a Chariot, but must first jump
        1 - and only 1 - piece. Cannons cannot jump over or capture opposing Cannons.
        """

        smaller_column = min(source_column, dest_column)
        larger_column = max(source_column, dest_column)
        smaller_row = min(source_row, dest_row)
        larger_row = max(source_row, dest_row)

        # can't capture friendly
        if self.empty_or_enemy(source_column, source_row, dest_column, dest_row) is False:
            return False

        # can't capture Cannon
        if type(self.get_piece_by_coordinate(dest_column, dest_row)) == Cannon:
            return False

        count = 0

        for space in range(smaller_column + 1, larger_column):
            if self.get_piece_by_coordinate(space, source_row) is not None:
                if type(self.get_piece_by_coordinate(space, source_row)) is not Cannon:
                    count += 1

        for space in range(smaller_row + 1, larger_row):
            if self.get_piece_by_coordinate(source_column, space) is not None:
                if type(self.get_piece_by_coordinate(source_column, space)) is not Cannon:
                    count += 1

        # need to jump 1 - and only 1 - piece to move
        if count != 1:
            return False

        return True

    def make_general_move(self, source_column, source_row, dest_column, dest_row):
        """
        Helper to move_check(). Determines rules for General piece. Cannot capture friendly pieces
        """
        if self.empty_or_enemy(source_column, source_row, dest_column, dest_row):
            return True

        return False

    def make_guard_move(self, source_column, source_row, dest_column, dest_row):
        """
        Helper to move_check(). Determines rules for Guard piece. Cannot capture friendly pieces
        """

        if self.empty_or_enemy(source_column, source_row, dest_column, dest_row):
            return True

        return False

    def make_soldier_move(self, source_column, source_row, dest_column, dest_row):
        """
        Helper to move_check(). Determines rules for Soldier piece. Cannot capture friendly pieces
        """
        if self.empty_or_enemy(source_column, source_row, dest_column, dest_row):
            return True

        return False

    def empty_or_enemy(self, source_column, source_row, dest_column, dest_row):
        """
        Determines if a space is empty or occupied by an enemy piece to be captured. Used in preventing player
        from capturing own pieces
        """
        other_piece = self.get_piece_by_coordinate(dest_column, dest_row)
        piece_color = self.get_piece_by_coordinate(source_column, source_row).get_color()

        if not other_piece:
            return True

        # there is a piece in the space
        other_piece_color = self.get_piece_by_coordinate(dest_column, dest_row).get_color()
        return self.is_enemy(piece_color, other_piece_color)

    @staticmethod
    def is_enemy(piece_color, other_piece_color):
        """
        Helper method for empty_or_enemy. Determines if the space is occupied by a piece of the opposing color.
        Returns False if piece is of the same color as the players
        """
        return piece_color != other_piece_color
