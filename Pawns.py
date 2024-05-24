from Pieces import Piece

class Pawn:
    def __init__(self, piece = 0x00FF00000000FF00):
        self.PIECE = Piece(piece)
        self.WHITE = 0        
        self.BLACK = 1        
        self.RANKS = [Piece() for i in range(8)]
        self.ATTACKS = [[None for i in range(2)] for j in range(64)]
        self.initialize_ranks()
        self.initialize_attacks()
        
    def initialize_ranks(self):
        self.RANKS[0].PIECE = 0xFF
        for i in range(1, 8):
            self.RANKS[i] = self.RANKS[i - 1] << 8
            
    def initialize_attacks(self):
        for i in range(64):
            pawn = Piece(1) << i
            self.ATTACKS[i][self.WHITE] = pawn.moveUL() | pawn.moveUR()
            self.ATTACKS[i][self.BLACK] = pawn.moveDL() | pawn.moveDR()
    
    def get_piece(self, side):
        return self.PIECE & side
        
        
    def smove(self, color, sides):
        pawns = self.get_piece(sides[color])
        empty = ~(sides[0] | sides[1])
        if color == self.WHITE:
            pawns = pawns.moveU()
        else:
            pawns = pawns.moveD()
            
        pawns &= empty
        return pawns
    
    def dmove(self, color, sides):
        pawns = self.smove(color, sides)
        empty = ~(sides[0] | sides[1])
        if color == self.WHITE:
            pawns = pawns.moveU() & self.RANKS[3]
        else:
            pawns = pawns.moveD() & self.RANKS[4]
            
        pawns &= empty
        return pawns