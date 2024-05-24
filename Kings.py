from Pieces import Piece

class King:
    def __init__(self, piece = 0x1400000000000014):
        self.PIECE = Piece(piece)
        self.WHITE = 0        
        self.BLACK = 1        
        self.RANKS = [Piece() for i in range(8)]
        self.ATTACKS = [Piece(0) for i in range(64)]
        self.initialize_ranks()
        self.initialize_attacks()
        
    def initialize_ranks(self):
        self.RANKS[0].PIECE = 0xFF
        for i in range(1, 8):
            self.RANKS[i] = self.RANKS[i - 1] << 8
            
            
    def initialize_attacks(self):
        for i in range(64):
            king = Piece(1) << i
            moves = [Piece(0) for _ in range(8)]
            moves[0] = king.moveU()
            moves[1] = king.moveUL()
            moves[2] = king.moveUR()
            moves[3] = king.moveD()
            moves[4] = king.moveDL()
            moves[5] = king.moveDR()
            moves[6] = king.moveL()
            moves[7] = king.moveR()
            
            for move in moves:
                self.ATTACKS[i] |= move
            