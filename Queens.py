from Pieces import Piece
from Rooks import Rook
from Bishops import Bishop

class Queen:
    def __init__(self, piece = 0x800000000000008):
        self.PIECE = Piece(piece)
        self.WHITE = 0        
        self.BLACK = 1        
        self.Bishop = Bishop()
        self.Rook = Rook()


    def get_attack(self, square, occupancy):
        bishop_occupancy = Piece(occupancy)
        rook_occupancy = Piece(occupancy)
        bishop_occupancy &= self.Bishop.ATTACK_MASK[square]
        bishop_occupancy *= self.Bishop.MAGIC_NUMBERS[square]
        bishop_occupancy >>= (64 - self.Bishop.RELEVANT_BITS[square])
        rook_occupancy &= self.Rook.ATTACK_MASK[square]
        rook_occupancy *= self.Rook.MAGIC_NUMBERS[square]
        rook_occupancy >>= (64 - self.Rook.RELEVANT_BITS[square])

        return self.Rook.SLIDER_ATTACKS[square][rook_occupancy.PIECE] | self.Bishop.SLIDER_ATTACKS[square][bishop_occupancy.PIECE]
