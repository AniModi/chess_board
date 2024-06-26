from Pieces import Piece
from Pawns import Pawn
from Knights import Knight
from Bishops import Bishop
from Kings import King
from Rooks import Rook
from Queens import Queen

class BOARD:
    def __init__(self):
        self.PAWN = 0
        self.ROOK = 1
        self.KNIGHT = 2
        self.BISHOP = 3
        self.QUEEN = 4
        self.KING = 5
        self.SIDES = [Piece(), Piece()]
        self.WHITE = 0
        self.BLACK = 1
        self.BOARD = [Pawn(), Rook(), Knight(), Bishop(), Queen(), King()]
        self.RANKS = [Piece() for i in range(8)]
        self.initialize_ranks()

    def initialize_board(self, board):

        self.SIDES[0].PIECE = board[0]
        self.SIDES[1].PIECE = board[1]
        for i in range(2, 8):
            self.BOARD[i - 2].PIECE = Piece(board[i])

    def initialize_ranks(self):
        self.RANKS[0].PIECE = 0xFF
        for i in range(1, 8):
            self.RANKS[i] = self.RANKS[i - 1] << 8

    def get_all_pieces(self):

        return self.SIDES[self.WHITE] | self.SIDES[self.BLACK]
        

    def get_piece(self, piece_id, color):

        return self.SIDES[color] & self.BOARD[piece_id].PIECE

    def get_piece_attacks(self, piece_id):
        if piece_id == self.BISHOP or piece_id == self.ROOK or piece_id == self.QUEEN:
            return self.BOARD[piece_id].get_attack
        return self.BOARD[piece_id].ATTACKS

    
    def place_piece_at(self, side, piece, pos):
        pos = self.square_to_bitboard(pos)
        self.BOARD[piece].PIECE = self.BOARD[piece].PIECE.set_bit(pos)
        self.SIDES[side].PIECE = self.SIDES[side].PIECE.set_bit(pos)

    def update_fen(self, fen):
        piece_symbols = {'p': 0, 'r': 1, 'n': 2, 'b': 3, 'q': 4, 'k': 5,
                            'P': 6, 'R': 7, 'N': 8, 'B': 9, 'Q': 10, 'K': 11}

        ranks = fen.split()[0].split('/')
        bitboard = [0] * 12

        for i, rank in enumerate(ranks):
            file_index = 0
            for char in rank:
                if char.isdigit():
                    file_index += int(char)
                else:
                    piece_index = piece_symbols[char]
                    square_index = (7 - i) * 8 + file_index
                    bitboard[piece_index] |= 1 << square_index
                    file_index += 1
        white_pieces = Piece()
        black_pieces = Piece()
        for i in range(6):
            black_pieces|= Piece(bitboard[i])
            white_pieces |= Piece(bitboard[6 + i])
        bitboard = [white_pieces, black_pieces] + [Piece(bitboard[i] | bitboard[6 + i]) for i in range(len(bitboard) // 2)]

        self.initialize_board(bitboard)


    def __str__(self):
        w_pawn = self.get_piece(self.PAWN, self.WHITE)
        w_rook = self.get_piece(self.ROOK, self.WHITE)
        w_knight = self.get_piece(self.KNIGHT, self.WHITE)
        w_bishop = self.get_piece(self.BISHOP, self.WHITE)
        w_queen = self.get_piece(self.QUEEN, self.WHITE)
        w_king = self.get_piece(self.KING, self.WHITE)

        b_pawn = self.get_piece(self.PAWN, self.BLACK)
        b_rook = self.get_piece(self.ROOK, self.BLACK)
        b_knight = self.get_piece(self.KNIGHT, self.BLACK)
        b_bishop = self.get_piece(self.BISHOP, self.BLACK)
        b_queen = self.get_piece(self.QUEEN, self.BLACK)
        b_king = self.get_piece(self.KING, self.BLACK)

        # Unicode chess symbols
        symbols = {
            'b_pawn': '♙', 'b_rook': '♖', 'b_knight': '♘', 'b_bishop': '♗', 'b_queen': '♕', 'b_king': '♔',
            'w_pawn': '♟', 'w_rook': '♜', 'w_knight': '♞', 'w_bishop': '♝', 'w_queen': '♛', 'w_king': '♚'
        }

        # Labels for files (columns) and ranks (rows)
        files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        ranks = ['8', '7', '6', '5', '4', '3', '2', '1']

        # Initial empty chessboard
        board = [['.' for _ in range(8)] for _ in range(8)]

        # Fill the board with piece symbols
        for row in range(8):
            for col in range(8):
                if (w_pawn & (1 << (63 - row * 8 - col))).PIECE:
                    board[row][col] = symbols['w_pawn']
                elif (w_rook & (1 << (63 - row * 8 - col))).PIECE:
                    board[row][col] = symbols['w_rook']
                elif (w_knight & (1 << (63 - row * 8 - col))).PIECE:
                    board[row][col] = symbols['w_knight']
                elif (w_bishop & (1 << (63 - row * 8 - col))).PIECE:
                    board[row][col] = symbols['w_bishop']
                elif (w_queen & (1 << (63 - row * 8 - col))).PIECE:
                    board[row][col] = symbols['w_queen']
                elif (w_king & (1 << (63 - row * 8 - col))).PIECE:
                    board[row][col] = symbols['w_king']
                elif (b_pawn & (1 << (63 - row * 8 - col))).PIECE:
                    board[row][col] = symbols['b_pawn']
                elif (b_rook & (1 << (63 - row * 8 - col))).PIECE:
                    board[row][col] = symbols['b_rook']
                elif (b_knight & (1 << (63 - row * 8 - col))).PIECE:
                    board[row][col] = symbols['b_knight']
                elif (b_bishop & (1 << (63 - row * 8 - col))).PIECE:
                    board[row][col] = symbols['b_bishop']
                elif (b_queen & (1 << (63 - row * 8 - col))).PIECE:
                    board[row][col] = symbols['b_queen']
                elif (b_king & (1 << (63 - row * 8 - col))).PIECE:
                    board[row][col] = symbols['b_king']

        # Build the board string with labels
        board_string = "  a b c d e f g h\n"
        for i in range(8):
            board_string += ranks[i] + ' ' + ' '.join(board[i][::-1]) + '\n'

        return board_string


    def square_to_bitboard(self, square):
        _file = square[0].lower()
        rank = square[1]
        file_index = ord(_file) - ord('a')
        rank_index = int(rank) - 1
        bit_position = rank_index * 8 + file_index
        return bit_position