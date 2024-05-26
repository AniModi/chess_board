from Pieces import Piece
from Board import BOARD
from Move import Move

empty_board = "8/8/8/8/8/8/8/8 w - - "
start_position = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1 "
tricky_position = "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1 "
killer_position = "rnbqkb1r/pp1p1pPp/8/2p1pP2/1P1P4/3P3P/P1P1P3/RNBQKBNR w KQkq e6 0 1"
cmk_position = "r2q1rk1/ppp2ppp/2n1bn2/2b1p3/3pP3/3P1NPP/PPP1NPB1/R1BQ1RK1 b - - 0 9 "

class CASTLING_RIGHTS:

    def __init__(self):
        self.W_KING_SIDE = 1
        self.W_QUEEN_SIDE = 2
        self.B_KING_SIDE = 4
        self.B_QUEEN_SIDE = 8
        self.CASTLING_RIGHTS = 15

    def __str__(self):
        rights = ""
        if self.CASTLING_RIGHTS & self.W_KING_SIDE:\
            rights += "K"
        if self.CASTLING_RIGHTS & self.W_QUEEN_SIDE:
            rights += 'Q' 
        if self.CASTLING_RIGHTS & self.B_KING_SIDE:
            rights += 'k' 
        if self.CASTLING_RIGHTS & self.B_QUEEN_SIDE:
        	rights += 'q' 
        return rights if rights != "" else "-"

    def update_castling_rights(self, rights):
        self.CASTLING_RIGHTS = 0
        for ch in rights:
            match ch:
                case 'K':
                    self.CASTLING_RIGHTS |= self.W_KING_SIDE
                    continue
                case 'Q':
                    self.CASTLING_RIGHTS |= self.W_QUEEN_SIDE
                    continue
                case 'k':
                    self.CASTLING_RIGHTS |= self.B_KING_SIDE
                    continue
                case 'q':
                    self.CASTLING_RIGHTS |= self.B_QUEEN_SIDE
                    continue


PAWN = 1
ROOK = 2
KNIGHT = 3
BISHOP = 4
QUEEN = 5
KING = 6

B_PAWN = 8 | PAWN
B_ROOK = 8 | ROOK
B_KNIGHT = 8 | KNIGHT
B_BISHOP = 8 | BISHOP
B_QUEEN = 8 | QUEEN
B_KING = 8 | KING



class Chess:
    def __init__(self):
        self.BOARD = BOARD()
        self.WHITE = 0
        self.BLACK = 1
        self.CURRENT_PLAYER = self.WHITE
        self.EN_PASSANT_SQUARE = -1
        self.CASTLING_RIGHTS = CASTLING_RIGHTS()
        self.MOVES = []
        self.BOARD.update_fen(start_position)

    def get_piece(self, piece, side):
        return self.BOARD.get_piece(piece, side)

    def __str__(self):
        return self.BOARD.__str__()
    
    def is_square_attacked(self, square, side):
        pos = self.square_to_bitboard(square)

        # Check if pawn attacks
        if (self.get_piece(0, side) & self.BOARD.get_piece_attacks(0)[pos][1 - side]).PIECE:
            return True

        # # Check if rook attacks
        if (self.get_piece(1, side) & self.BOARD.get_piece_attacks(1)(pos, self.BOARD.get_all_pieces())).PIECE:
            return True

        # Check if knight attacks
        if (self.get_piece(2, side) & self.BOARD.get_piece_attacks(2)[pos]).PIECE:
            return True

        # # Check if bishop attacks
        if (self.get_piece(3 ,side) & self.BOARD.get_piece_attacks(3)(pos, self.BOARD.get_all_pieces())).PIECE:
            return True

        # # Check if bishop attacks
        if (self.get_piece(4, side) & self.BOARD.get_piece_attacks(4)(pos, self.BOARD.get_all_pieces())).PIECE:
            return True

        # Check if king attacks
        if (self.get_piece(5, side) & self.BOARD.get_piece_attacks(5)[pos]).PIECE:
            return True

        return False
 
    def generate_moves(self):
        self.MOVES = []
        side = self.CURRENT_PLAYER
        source = 0
        target = 0

        board_copy = 0
        attacks = 0

        for piece in range(0, 6):
            board_copy = self.get_piece(piece, side)
            # Pawn
            if piece == 0:
                pawn_attacks = self.BOARD.get_piece_attacks(0)
                if side == self.WHITE:
                    while board_copy.PIECE:

                        source = board_copy.get_LSB()
                        board_copy = board_copy.remove_bit(source)
                        target = source + 8
                        if target <= 64 and not self.BOARD.get_all_pieces().get_bit(target):
                            if source >= 48 and source <= 55:
                                self.MOVES.append(Move(source, target, PAWN, ROOK, 0, 0, 0, 0))
                                self.MOVES.append(Move(source, target, PAWN, KNIGHT, 0, 0, 0, 0))
                                self.MOVES.append(Move(source, target, PAWN, BISHOP, 0, 0, 0, 0))
                                self.MOVES.append(Move(source, target, PAWN, QUEEN, 0, 0, 0, 0))
                            
                            else:
                                self.MOVES.append(Move(source, target, PAWN, 0, 0, 1, 0, 0))
                                if source >= 8 and source <= 15 and not self.BOARD.get_all_pieces().get_bit(target + 8):
                                    self.MOVES.append(Move(source, target + 8, PAWN, 0, 0, 1, 0, 0))
                        
                        attacks = pawn_attacks[source][self.WHITE] & self.BOARD.SIDES[1].PIECE

                        while attacks.PIECE:
                            target = attacks.get_LSB()
                            attacks = attacks.remove_bit(target)
                            if source >= 48 and source <= 55:
                                self.MOVES.append(Move(source, target, PAWN, ROOK, 1, 0, 0, 0))
                                self.MOVES.append(Move(source, target, PAWN, KNIGHT, 1, 0, 0, 0))
                                self.MOVES.append(Move(source, target, PAWN, BISHOP, 1, 0, 0, 0))
                                self.MOVES.append(Move(source, target, PAWN, QUEEN, 1, 0, 0, 0))
                        
                        if self.EN_PASSANT_SQUARE != -1:
                            en_passant_attack = pawn_attacks[source][side] & Piece(1 << self.EN_PASSANT_SQUARE)
                            if en_passant_attack.PIECE:
                                self.MOVES.append(Move(source, en_passant_attack, PAWN, 0, 1, 0, 1, 0))
                else:
                    while board_copy.PIECE:
                        source = board_copy.get_LSB()
                        board_copy = board_copy.remove_bit(source)
                        target = source - 8
                        if target >= 0 and not self.BOARD.get_all_pieces().get_bit(target):
                            if source >= 8 and source <= 15:
                                self.MOVES.append(Move(source, target, B_PAWN, B_ROOK, 0, 0, 0, 0))
                                self.MOVES.append(Move(source, target, B_PAWN, B_KNIGHT, 0, 0, 0, 0))
                                self.MOVES.append(Move(source, target, B_PAWN, B_BISHOP, 0, 0, 0, 0))
                                self.MOVES.append(Move(source, target, B_PAWN, B_QUEEN, 0, 0, 0, 0))
                            
                            else:
                                self.MOVES.append(Move(source, target, B_PAWN, 0, 0, 1, 0, 0))
                                if source >= 48 and source <= 55 and not self.BOARD.get_all_pieces().get_bit(target - 8):
                                    self.MOVES.append(Move(source, target - 8, B_PAWN, 0, 0, 1, 0, 0))

                        attacks = pawn_attacks[source][self.BLACK] & self.BOARD.SIDES[0].PIECE
                        while attacks.PIECE:
                            target = attacks.get_LSB()
                            attacks = attacks.remove_bit(target)
                            if source >= 8 and source <= 15:
                                self.MOVES.append(Move(source, target, B_PAWN, B_ROOK, 1, 0, 0, 0))
                                self.MOVES.append(Move(source, target, B_PAWN, B_KNIGHT, 1, 0, 0, 0))
                                self.MOVES.append(Move(source, target, B_PAWN, B_BISHOP, 0, 0, 0, 0))
                                self.MOVES.append(Move(source, target, B_PAWN, B_QUEEN, 1, 0, 0, 0))

                        if self.EN_PASSANT_SQUARE != -1:
                            en_passant_attack = pawn_attacks[source][side] & Piece(1 << self.EN_PASSANT_SQUARE)
                            if en_passant_attack.PIECE:
                                self.MOVES.append(Move(source, en_passant_attack, PAWN, 0, 1, 0, 1, 0))
            # Rook
            if piece == 1:
                rook_attacks = self.BOARD.get_piece_attacks(1)
                while board_copy.PIECE:
                    source = board_copy.get_LSB()
                    board_copy = board_copy.remove_bit(source)
                    attacks = rook_attacks(source, self.BOARD.get_all_pieces()) & ~self.BOARD.SIDES[side].PIECE

                    while attacks.PIECE:
                        target = attacks.get_LSB()
                        attacks = attacks.remove_bit(target)
                        if not self.BOARD.SIDES[1 - side].get_bit(target).PIECE:
                            self.MOVES.append(Move(source, target, ROOK if side == self.WHITE else B_ROOK, 0, 0, 0, 0, 0))
                        else:
                            self.MOVES.append(Move(source, target, ROOK if side == self.WHITE else B_ROOK, 0, 1, 0, 0, 0))
            # Knight
            if piece == 2:
                print("-"*8 + "Knights" + "-"*8)
                knight_attacks = self.BOARD.get_piece_attacks(2)
                while board_copy.PIECE:
                    source = board_copy.get_LSB()
                    board_copy = board_copy.remove_bit(source)
                    attacks = knight_attacks[source] & ~self.BOARD.SIDES[side].PIECE

                    while attacks.PIECE:
                        target = attacks.get_LSB()
                        attacks = attacks.remove_bit(target)
                        if not self.BOARD.SIDES[1 - side].get_bit(target).PIECE:
                            self.MOVES.append(Move(source, target, KNIGHT if side == self.WHITE else B_KNIGHT, 0, 0, 0, 0, 0))
                        else:
                            self.MOVES.append(Move(source, target, KNIGHT if side == self.WHITE else B_KNIGHT, 0, 1, 0, 0, 0))
            # Bishop
            if piece == 3:
                bishop_attacks = self.BOARD.get_piece_attacks(3)
                while board_copy.PIECE:
                    source = board_copy.get_LSB()
                    board_copy = board_copy.remove_bit(source)
                    attacks = bishop_attacks(source, self.BOARD.get_all_pieces()) & ~self.BOARD.SIDES[side].PIECE

                    while attacks.PIECE:
                        target = attacks.get_LSB()
                        attacks = attacks.remove_bit(target)
                        if not self.BOARD.SIDES[1 - side].get_bit(target).PIECE:
                            self.MOVES.append(Move(source, target, BISHOP if side == self.WHITE else B_BISHOP, 0, 0, 0, 0, 0))
                        else:
                            self.MOVES.append(Move(source, target, BISHOP if side == self.WHITE else B_BISHOP, 0, 1, 0, 0, 0))
            # Queen
            if piece == 4:
                print("-"*8 + "Queens" + "-"*8)
                queen_attacks = self.BOARD.get_piece_attacks(4)
                while board_copy.PIECE:
                    source = board_copy.get_LSB()
                    board_copy = board_copy.remove_bit(source)
                    attacks = queen_attacks(source, self.BOARD.get_all_pieces()) & ~self.BOARD.SIDES[side].PIECE

                    while attacks.PIECE:
                        target = attacks.get_LSB()
                        attacks = attacks.remove_bit(target)
                        if not self.BOARD.SIDES[1 - side].get_bit(target).PIECE:
                            self.MOVES.append(Move(source, target, QUEEN if side == self.WHITE else B_QUEEN, 0, 0, 0, 0, 0))
                        else:
                            self.MOVES.append(Move(source, target, QUEEN if side == self.WHITE else B_QUEEN, 0, 1, 0, 0, 0))
            # King
            if piece == 5:
                occupancy =  self.BOARD.get_all_pieces()
                king_attacks = self.BOARD.get_piece_attacks(5)
                while board_copy.PIECE:
                    source = board_copy.get_LSB()
                    board_copy = board_copy.remove_bit(source)
                    attacks = king_attacks[source] & ~self.BOARD.SIDES[side].PIECE

                    while attacks.PIECE:
                        target = attacks.get_LSB()
                        attacks = attacks.remove_bit(target)
                        if not self.BOARD.SIDES[1 - side].get_bit(target).PIECE:
                            self.MOVES.append(Move(source, target, KING if side == self.WHITE else B_KING, 0, 0, 0, 0, 0))
                        else:
                            self.MOVES.append(Move(source, target, KING if side == self.WHITE else B_KING, 0, 1, 0, 0, 0))

                if side == self.WHITE:
                    if self.CASTLING_RIGHTS.CASTLING_RIGHTS & self.CASTLING_RIGHTS.W_KING_SIDE:
                        if not occupancy.get_bit(5) and not occupancy.get_bit(6):
                            if not self.is_square_attacked("f1", self.BLACK) and not self.is_square_attacked("g1", self.BLACK) and not self.is_square_attacked("e1", self.BLACK):
                                self.MOVES.append(Move(source, target, KING, 0, 0, 0, 0, 1))
                    if self.CASTLING_RIGHTS.CASTLING_RIGHTS & self.CASTLING_RIGHTS.W_QUEEN_SIDE:
                        if not occupancy.get_bit(1) and not occupancy.get_bit(2) and not occupancy.get_bit(3):
                            if not self.is_square_attacked("c1", self.BLACK) and not self.is_square_attacked("d1", self.BLACK) and not self.is_square_attacked("e1", self.BLACK):
                                self.MOVES.append(Move(source, target, KING, 0, 0, 0, 0, 1))
                else:
                    if self.CASTLING_RIGHTS.CASTLING_RIGHTS & self.CASTLING_RIGHTS.B_KING_SIDE:
                        if not occupancy.get_bit(61) and not occupancy.get_bit(62):
                            if not self.is_square_attacked("f8", self.BLACK) and not self.is_square_attacked("g8", self.BLACK) and not self.is_square_attacked("e8", self.BLACK):
                                self.MOVES.append(Move(source, target, B_KING, 0, 0, 0, 0, 1))
                    if self.CASTLING_RIGHTS.CASTLING_RIGHTS & self.CASTLING_RIGHTS.B_QUEEN_SIDE:
                        if not occupancy.get_bit(57) and not occupancy.get_bit(58) and not occupancy.get_bit(59):
                            if not self.is_square_attacked("c8", self.BLACK) and not self.is_square_attacked("d8", self.BLACK) and not self.is_square_attacked("e8", self.BLACK):
                                self.MOVES.append(Move(source, target, B_KING, 0, 0, 0, 0, 1))

    def print_attacked_squares(self, side):
        print("  a b c d e f g h")
        for r in range(7, -1, -1):
            print(r + 1, end = " ")
            for f in range(8):
                square = self.get_square_from_pos(f, r)
                if self.is_square_attacked(square, side):
                    print('*', end = " ")
                else:
                    print('.', end = " ")
            print()

    def get_square_from_pos(*args):
        if len(args) == 2:
            return chr(97 + args[1] % 8) + str(1 + args[1] // 8)
        else:
            return chr(97 + args[1]) + str(1 + args[2])

    def square_to_bitboard(self, square):
        _file = square[0].lower()
        rank = square[1]
        file_index = ord(_file) - ord('a')
        rank_index = int(rank) - 1
        bit_position = rank_index * 8 + file_index
        return bit_position

    def update_fen(self, fen):
        fen_param = fen.split()
        self.BOARD.update_fen(fen_param[0])
        self.CURRENT_PLAYER = 0 if fen_param[1] == 'w' else 1
        self.CASTLING_RIGHTS.update_castling_rights(fen_param[2])
        self.EN_PASSANT_SQUARE = -1 if fen_param[3] == '-' else self.square_to_bitboard(fen_param[3])


chess = Chess()
chess.update_fen(start_position)
# print(chess.get_square_from_pos(chess.EN_PASSANT_SQUARE))
chess.update_fen("r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R 2 KQkq - 0 1")
chess.generate_moves()
# print(chess.BOARD.SIDES[1].PIECE)
print(chess)

print(chess.MOVES)




# print(chess.square_to_bitboard("e4"))
# print(chess.get_square_from_pos(0, 7))