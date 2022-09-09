class GamePiece:
    """
    Represents the pieces on the board of Janggi. Each piece type subclass has their separate move-set and symbol
    representation associated with it. Each piece interacts with the JanggiGame class as it is used to create and move
    pieces and determine their move-sets throughout the game.
    """

    def __init__(self, color, column, row):
        """Initializes the GamePiece class. Each piece, when created, has an assigned color, location, and symbol
        associated with it"""
        self._color = color
        self._row = row
        self._column = column
        self._red_symbol = ""
        self._blue_symbol = ""

    def get_color(self):
        """Returns the color of the piece"""
        return self._color

    def get_row(self):
        """Returns the position of the row (the y-coordinate) of the piece"""
        return self._row

    def set_row(self, row):
        """Set's the row (the y-coordinate) of the piece"""
        self._row = row

    def get_column(self):
        """Returns the position of the column (the x-coordinate) of the piece"""
        return self._column

    def set_column(self, column):
        """Set's the column (the x-coordinate) of the piece"""
        self._column = column

    def get_symbol(self):
        """Returns unicode symbol of piece depending on color"""
        if self.get_color() == "Red":
            return self._red_symbol
        else:
            return self._blue_symbol

    @staticmethod
    def is_in_bounds(x, y):
        """
        Determines if the coordinates are within the boundaries of the board. Returns False if they are outside
        the bounds of the board
        """

        if x < 0 or x > 8:
            return False

        elif y < 0 or y > 9:
            return False

        else:
            return True

    @staticmethod
    def is_in_fortress(x, y):
        """
        Determines if the coordinates given are within the boundaries of a fortress. Used to prevent general and
        guards from leaving the fortress
        """
        if (3 <= x <= 5) and (0 <= y <= 2 or 7 <= y <= 9):
            return True
        else:
            return False


class Horse(GamePiece):
    """Represents a piece that can move forward one space unobstructed and forward diagonally another space"""

    def __init__(self, color, column, row):
        """Initializes the piece with its specific symbol representation"""
        super().__init__(color, column, row)
        self._red_symbol = "♞"
        self._blue_symbol = "♘"

    def is_legal_move(self, x, y):
        """Defines the legal move-set for the piece"""

        if self.is_in_bounds(x, y) is False:

            return False

        # functionally the same for both colors
        if (x == self.get_column() + 2 or x == self.get_column() - 2) and (
                y == self.get_row() + 1 or y == self.get_row() - 1):
            return True
        elif (x == self.get_column() + 1 or x == self.get_column() - 1) and (
                y == self.get_row() + 2 or y == self.get_row() - 2):
            return True
        else:

            return False


class Chariot(GamePiece):
    """Represents piece that can move in a straight line unobstructed, until the end of the board."""

    def __init__(self, color, column, row):
        """Initializes the piece with its specific symbol representation"""
        super().__init__(color, column, row)
        self._red_symbol = "♜"
        self._blue_symbol = "♖"

    def is_legal_move(self, x, y):
        """Defines the legal move-set for the piece"""

        if self.is_in_bounds(x, y) is False:

            return False

        # functionally the same for both colors
        # moves differently within fortresses
        if (self.get_column() == 4) and (self.get_row() == 1) and ((3 <= x <= 5) and (0 <= y <= 2)):
            return True
        if (self.get_column() == 4) and (self.get_row() == 8) and ((3 <= x <= 5) and (7 <= y <= 9)):
            return True
        if (x == 4) and (y == 1) and ((3 <= self.get_column() <= 5) and (0 <= self.get_row() <= 2)):
            return True
        if (x == 4) and (y == 8) and ((3 <= self.get_column() <= 5) and (7 <= self.get_row() <= 9)):
            return True

        if self.is_in_fortress(self.get_column(), self.get_row()) and self.is_in_fortress(x, y):

            # can move from one corner to the next diagonally in fortress
            if (x == self.get_column() + 2) and (y == self.get_row() + 2):
                return True
            if (x == self.get_column() - 2) and (y == self.get_row() - 2):
                return
            if (x == self.get_column() + 2) and (y == self.get_row() - 2):
                return True
            if (x == self.get_column() - 2) and (y == self.get_row() + 2):
                return True

        if x == self.get_column():
            return True

        if y == self.get_row():
            return True

        return False


class Elephant(GamePiece):
    """Represents a piece that can move two spaces forward unobstructed and 2 spaces diagonally"""

    def __init__(self, color, column, row):
        """Initializes the piece with its specific symbol representation"""
        super().__init__(color, column, row)
        self._red_symbol = "♣"
        self._blue_symbol = "♧"

    def is_legal_move(self, x, y):
        """Defines the legal move-set for the piece"""

        if self.is_in_bounds(x, y) is False:
            return False

        move_right = (self.get_column() + 3)
        move_left = (self.get_column() - 3)
        horizontal_then_down = (self.get_row() + 2)
        horizontal_then_up = (self.get_row() - 2)
        vertical_then_left = (self.get_column() + 2)
        vertical_then_right = (self.get_column() - 2)
        move_up = (self.get_row() - 3)
        move_down = (self.get_row() + 3)

        # functionally the same for both colors
        if (x == move_right or x == move_left) and (y == horizontal_then_down or y == horizontal_then_up):
            return True

        if (y == move_down or y == move_up) and (x == vertical_then_left or x == vertical_then_right):
            return True

        return False


class Cannon(GamePiece):
    """
    Represents a piece that can move in a straight line, but only if a friendly piece is somewhere in front of it.
    This piece cannot jump over more than one piece at a time, and it cannot capture or jump over other cannon pieces.
    """

    def __init__(self, color, column, row):
        """Initializes the piece with its specific symbol representation"""
        super().__init__(color, column, row)
        self._red_symbol = "♛"
        self._blue_symbol = "♕"

    def is_legal_move(self, x, y):
        """Defines the legal move-set for the piece"""

        if self.is_in_bounds(x, y) is False:

            return False

        # functionally the same for both colors

        # moves differently within fortresses
        if self.is_in_fortress(self.get_column(), self.get_row()) and self.is_in_fortress(x, y):

            # can move from one corner to the next diagonally in fortress
            if (x == self.get_column() + 2) and (y == self.get_row() + 2):
                return True
            if (x == self.get_column() - 2) and (y == self.get_row() - 2):
                return True
            if (x == self.get_column() + 2) and (y == self.get_row() - 2):
                return True
            if (x == self.get_column() - 2) and (y == self.get_row() + 2):
                return True

        if x == self.get_column():
            return True

        if y == self.get_row():
            return True

        return False


class General(GamePiece):
    """
    Represents a piece that can only move on space in any direction within the bounds of the 'fortress.'
    This piece must be protected and any threat to it results in a 'check' that requires that it move out of the range
    of the threat. If the threat cannot be avoided, then 'checkmate' is called and the game is lost in favor of the
    opponent
    """

    def __init__(self, color, column, row):
        """Initializes the piece with its specific symbol representation"""
        super().__init__(color, column, row)
        self._red_symbol = "♚"
        self._blue_symbol = "♔"

    def is_legal_move(self, x, y):
        """Defines the legal move-set for the piece"""

        if self.is_in_bounds(x, y) is False:

            return False

        if self.is_in_fortress(x, y) is False:

            return False

        if self.get_color() == "Blue":
            if (x == self.get_column() + 1 or x == self.get_column() - 1) and y == self.get_row():
                return True
            elif x == self.get_column() and (y == self.get_row() + 1 or y == self.get_row() - 1):
                return True
            elif x == 4 and y == 8:  # can move to middle from all positions in the fortress
                return True
            elif ((self.get_column() == 4) and (self.get_row() == 8)) and ((3 <= x <= 5) and (7 <= y <= 9)):
                return True

            else:

                return False

        if self.get_color() == "Red":
            if (x == self.get_column() + 1 or x == self.get_column() - 1) and y == self.get_row():
                return True
            elif x == self.get_column() and (y == self.get_row() + 1 or y == self.get_row() - 1):
                return True
            elif x == 4 and y == 1:  # can move to middle from all positions in the fortress
                return True
            elif ((self.get_column() == 4) and (self.get_row() == 1)) and ((3 <= x <= 5) and (0 <= y <= 2)):
                return True

            else:

                return False


class Guard(GamePiece):
    """Represents a piece that can only move on space in any direction within the bounds of the 'fortress'"""

    def __init__(self, color, column, row):
        """Initializes the piece with its specific symbol representation"""
        super().__init__(color, column, row)
        self._red_symbol = "♝"
        self._blue_symbol = "♗"

    def is_legal_move(self, x, y):
        """Defines the legal move-set for the piece"""

        if self.is_in_bounds(x, y) is False:

            return False

        if self.is_in_fortress(x, y) is False:

            return False

        if self.get_color() == "Blue":
            if (x == self.get_column() + 1 or x == self.get_column() - 1) and y == self.get_row():
                return True
            elif x == self.get_column() and (y == self.get_row() + 1 or y == self.get_row() - 1):
                return True
            elif x == 4 and y == 8:  # can move to middle from all positions in the fortress
                return True
            elif ((self.get_column() == 4) and (self.get_row() == 8)) and ((3 <= x <= 5) and (7 <= y <= 9)):
                return True

            else:

                return False

        if self.get_color() == "Red":
            if (x == self.get_column() + 1 or x == self.get_column() - 1) and y == self.get_row():
                return True
            elif x == self.get_column() and (y == self.get_row() + 1 or y == self.get_row() - 1):
                return True
            elif x == 4 and y == 1:  # can move to middle from all positions in the fortress
                return True
            elif ((self.get_column() == 4) and (self.get_row() == 1)) and ((3 <= x <= 5) and (0 <= y <= 2)):
                return True

            else:

                return False


class Soldier(GamePiece):
    """Represents a piece that can move one space forwards, backwards, or sideways. Inside the opposing color's
    fortress, it is able to move to the middle from any space and also from the middle, can move to any space"""

    def __init__(self, color, column, row):
        """Initializes the piece with its specific symbol representation"""
        super().__init__(color, column, row)
        self._red_symbol = "♟"
        self._blue_symbol = "♙"

    def is_legal_move(self, x, y):
        """Defines the legal move-set for the piece"""

        if self.is_in_bounds(x, y) is False:

            return False

        if self.get_color() == "Red":

            # moves differently within enemy fortress
            if (self.get_column() == 4) and (self.get_row() == 8) and ((3 <= x <= 5) and (7 <= y <= 9)):
                return True
            if ((x == 4) and (y == 8)) and ((3 <= self.get_column() <= 5) and (7 <= self.get_row() <= 9)):
                return True

            if (x == self.get_column() + 1 or x == self.get_column() - 1) and y == self.get_row():
                return True
            if x == self.get_column() and (y == self.get_row() + 1):
                return True

            return False

        if self.get_color() == "Blue":

            # moves differently within enemy fortress
            if ((self.get_column() == 4) and (self.get_row() == 1)) and ((3 <= x <= 5) and (0 <= y <= 2)):
                return True
            if ((x == 4) and (y == 1)) and ((3 <= self.get_column() <= 5) and (0 <= self.get_row() <= 2)):
                return True

            if (x == self.get_column() + 1 or x == self.get_column() - 1) and y == self.get_row():
                return True
            if x == self.get_column() and y == self.get_row() - 1:
                return True

            return False
