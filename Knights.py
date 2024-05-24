from Pieces import Piece

class Knight:
    def __init__(self, piece = 0x4200000000000042):
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
            knight = Piece(1) << i
            moves = [Piece(0) for _ in range(8)]
            moves[0] = knight.moveU().moveU().moveL()
            moves[1] = knight.moveU().moveU().moveR()
            moves[2] = knight.moveD().moveD().moveL()
            moves[3] = knight.moveD().moveD().moveR()
            moves[4] = knight.moveL().moveL().moveU()
            moves[5] = knight.moveL().moveL().moveD()
            moves[6] = knight.moveR().moveR().moveU()
            moves[7] = knight.moveR().moveR().moveD()
            
            for move in moves:
                self.ATTACKS[i] |= move
            