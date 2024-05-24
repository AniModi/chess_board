from Pieces import Piece
from Pawns import Pawn
from Knights import Knight
from Bishops import Bishop
from Kings import King
from Rooks import Rook


class CASTLING_RIGHTS:

    def __init__(self):
        self.W_KING_SIDE = 1
        self.W_QUEEN_SIDE = 2
        self.B_KING_SIDE = 4
        self.B_QUEEN_SIDE = 8
        self.CASTLING_RIGHTS = 15

class Chess:
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
        self.BOARD = [Pawn(), Rook(), Knight(), Bishop(), Piece(), King()]
        self.RANKS = [Piece() for i in range(8)]
        self.CURRENT_PLAYER = self.WHITE
        self.EN_PASSANT_SQUARE = -1
        self.CASTLING_RIGHTS = CASTLING_RIGHTS()
        self.initialize_board()
        self.initialize_ranks()
    

    def initialize_ranks(self):

        self.RANKS[0].PIECE = 0xFF

        for i in range(1, 8):

            self.RANKS[i] = self.RANKS[i - 1] << 8
            

    def initialize_board(self, board = [0xFFFF, 0xFFFF000000000000, 0x00FF00000000FF00, 0x8100000000000081, 0x4200000000000042, 0x2400000000000024, 0x800000000000008, 0x1000000000000010]):

        self.SIDES[0].PIECE = board[0]
        self.SIDES[1].PIECE = board[1]
        for i in range(2, 8):
            self.BOARD[i - 2].PIECE = Piece(board[i])

    def get_all_pieces(self):

        return self.SIDES[self.WHITE] | self.SIDES[self.BLACK]
        

    def get_piece(self, piece_id, color):

        return self.SIDES[color] & self.BOARD[piece_id].PIECE

    def get_bishop_moves(self, square, color):
            
            return self.BOARD[self.BISHOP].get_attack(square, self.get_all_pieces())

    def update_fen(self, fen):
        piece_symbols = {'p': 0, 'r': 1, 'n': 2, 'b': 3, 'q': 4, 'k': 5,
                            'P': 6, 'R': 7, 'N': 8, 'B': 9, 'Q': 10, 'K': 11}

        ranks = fen.split()[0].split('/')
        bitboard = [0] * 12  # Initialize empty bitboards for each piece type

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


    def print_board(self):
        w_pawn = self.get_piece(self.PAWN, self.WHITE)
        print(w_pawn)
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

        # Print the board with labels
        print("  a b c d e f g h")
        for i in range(8):
            print(ranks[i], ' '.join(board[i][::-1]))

    

chess = Chess()
chess.print_board()
print(chess.get_piece(chess.PAWN, chess.WHITE))

