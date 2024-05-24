from Pieces import Piece
from Board import BOARD

class CASTLING_RIGHTS:

    def __init__(self):
        self.W_KING_SIDE = 1
        self.W_QUEEN_SIDE = 2
        self.B_KING_SIDE = 4
        self.B_QUEEN_SIDE = 8
        self.CASTLING_RIGHTS = 15


class GAME_PARAMETERS:

    def __init__(self):
        self.WHITE = 0
        self.BLACK = 1
        self.CURRENT_PLAYER = self.WHITE
        self.EN_PASSANT_SQUARE = -1
        self.CASTLING_RIGHTS = CASTLING_RIGHTS()

class Chess:
    def __init__(self):
        self.BOARD = BOARD()
        self.RANKS = [Piece() for i in range(8)]
        self.GAME_PARAMETERS = GAME_PARAMETERS()
        self.initialize_ranks()
    

    def initialize_ranks(self):

        self.RANKS[0].PIECE = 0xFF

        for i in range(1, 8):

            self.RANKS[i] = self.RANKS[i - 1] << 8

    def square_to_bitboard(self, square):
        if len(square) != 2:
            raise ValueError("Invalid square")
        
        file = square[0].lower()
        rank = square[1]

        if file < 'a' or file > 'h' or rank < '1' or rank > '8':
            raise ValueError("Invalid square")

        file_index = ord(file) - ord('a')
        rank_index = int(rank) - 1

        bit_position = rank_index * 8 + file_index


        return bit_position

    def print_board(self):

        print(self.BOARD)

    

chess = Chess()
chess.print_board()
