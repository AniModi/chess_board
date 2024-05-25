from Pieces import Piece
from Board import BOARD

empty_board = "8/8/8/8/8/8/8/8"
start_position = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
tricky_position = "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R"
killer_position = "rnbqkb1r/pp1p1pPp/8/2p1pP2/1P1P4/3P3P/P1P1P3/RNBQKBNR"
cmk_position = "r2q1rk1/ppp2ppp/2n1bn2/2b1p3/3pP3/3P1NPP/PPP1NPB1/R1BQ1RK1"

class CASTLING_RIGHTS:

    def __init__(self):
        self.W_KING_SIDE = 1
        self.W_QUEEN_SIDE = 2
        self.B_KING_SIDE = 4
        self.B_QUEEN_SIDE = 8
        self.CASTLING_RIGHTS = 15


class Chess:
    def __init__(self):
        self.BOARD = BOARD()
        self.RANKS = [Piece() for i in range(8)]
        self.WHITE = 0
        self.BLACK = 1
        self.CURRENT_PLAYER = self.WHITE
        self.EN_PASSANT_SQUARE = -1
        self.CASTLING_RIGHTS = CASTLING_RIGHTS()
        self.initialize_ranks()

    def square_to_bitboard(self, square):
        _file = square[0].lower()
        rank = square[1]
        file_index = ord(_file) - ord('a')
        rank_index = int(rank) - 1
        bit_position = rank_index * 8 + file_index
        return bit_position

    def get_pawn(self, side):
        return self.BOARD.get_piece(0, side)

    def get_rook(self, side):
        return self.BOARD.get_piece(1, side)
    def get_knight(self, side):
        return self.BOARD.get_piece(2, side)
        
    def get_bishop(self, side):
        return self.BOARD.get_piece(3, side)
        
    def get_queen(self, side):
        return self.BOARD.get_piece(4, side)

    def get_king(self, side):
        return self.BOARD.get_piece(5, side)

    def __str__(self):
        return self.BOARD.__str__()
    
    def initialize_ranks(self):
        self.RANKS[0].PIECE = 0xFF
        for i in range(1, 8):
            self.RANKS[i] = self.RANKS[i - 1] << 8


    def is_square_attacked(self, square, side):
        pos = self.square_to_bitboard(square)

        # Check if pawn attacks
        if (self.get_pawn(side) & self.BOARD.get_piece_attacks(0)[pos][1 - side]).PIECE:
            return True

        # # Check if rook attacks
        if (self.get_rook(side) & self.BOARD.get_piece_attacks(1)(pos, self.BOARD.get_all_pieces())).PIECE:
            return True

        # Check if knight attacks
        if (self.get_knight(side) & self.BOARD.get_piece_attacks(2)[pos]).PIECE:
            return True

        # # Check if bishop attacks
        if (self.get_bishop(side) & self.BOARD.get_piece_attacks(3)(pos, self.BOARD.get_all_pieces())).PIECE:
            return True

        # # Check if bishop attacks
        if (self.get_queen(side) & self.BOARD.get_piece_attacks(4)(pos, self.BOARD.get_all_pieces())).PIECE:
            return True

        # Check if king attacks
        if (self.get_king(side) & self.BOARD.get_piece_attacks(5)[pos]).PIECE:
            return True

        return False

    def print_attacked_sqaures(self, side):
        print("  a b c d e f g h")
        for r in range(7, -1, -1):
            print(r + 1, end = " ")
            for f in range(8):
                square = chr(97 + f) + str(r + 1)
                if self.is_square_attacked(square, side):
                    print('*', end = " ")
                else:
                    print('.', end = " ")
            print()

chess = Chess()
print(chess)