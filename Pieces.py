class Piece:
    def __init__(self, PIECE = 0, max = 0xffffffffffffffff):
        if isinstance(PIECE, int):
            self.PIECE = PIECE
        else:
            self.PIECE = PIECE.PIECE
        self.MAX = max
        self.NOT_A_FILE = 0xfefefefefefefefe
        self.NOT_H_FILE = 0x7f7f7f7f7f7f7f7f
        
    def __lshift__(self, other):
        return Piece((self.PIECE << other) & self.MAX)
    
    def __rshift__(self, other):
        return Piece((self.PIECE >> other) & self.MAX)
    
    def __and__(self, other):
        if isinstance(other, int):
            return Piece(self.PIECE & other)
        return Piece(self.PIECE & other.PIECE)
    
    def __or__(self, other):
        if isinstance(other, int):
            return Piece(self.PIECE | other)
        return Piece(self.PIECE | other.PIECE)
    
    def __xor__(self, other):
        if isinstance(other, int):
            return Piece(self.PIECE ^ other)
        return Piece(self.PIECE ^ other.PIECE)
    
    def __invert__(self):
        return Piece(self.MAX ^ self.PIECE)
    
    def __str__(self):
        binary_string = bin(self.PIECE)[2:].zfill(64)
        formatted_string = '\n'.join((binary_string[i : i + 8])[::-1] for i in range(0, 64, 8))
        return formatted_string
    
    
    def __mul__(self, other):
        if isinstance(other, int):
            return Piece(self.PIECE * other)
        return Piece(self.PIECE * other.PIECE) & self.MAX
    
    def count_bits(self):
        count = 0
        piece = self.PIECE
        while(piece):
            count += 1
            piece &= piece - 1        
        return count
    
    def get_bit(self, bit):
        return self.PIECE & (1 << bit)
    
    def remove_bit(self, bit):
        if self.get_bit(bit):
            return self ^ (1 << bit)
        
    def set_bit(self, bit):
        return self | (1 << bit)
    
    def get_LSB(self):
        if self.PIECE == 0:
            return -1
        return Piece((self.PIECE & -self.PIECE) - 1).count_bits()
    
    def moveU(self):
        self <<= 8
        return self
        
    def moveD(self):
        self >>= 8
        return self
    
    def moveR(self):
        self <<= 1
        self &= self.NOT_A_FILE # Remove rotation
        return self
    
    def moveL(self):
        self >>= 1
        self &= self.NOT_H_FILE # Remove rotation
        return self
    
    def moveUR(self):
        self <<= 9
        self &= self.NOT_A_FILE
        return self
    
    def moveUL(self):
        self <<= 7
        self &= self.NOT_H_FILE # Remove rotation
        return self
    
    def moveDR(self):
        self >>= 7
        self &= self.NOT_A_FILE
        return self
    
    def moveDL(self):
        self >>= 9
        self &= self.NOT_H_FILE
        return self

