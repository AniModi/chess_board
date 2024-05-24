from Pieces import Piece

class Random:
    
    def __init__(self):
        self.initial_state = Piece(1804289383)
        
    
    def get_random(self):
        number = self.initial_state
        
        number ^= number << 13 & 0xffffffff
        number ^= (number >> 17) & 0xffffffff
        number ^= number << 5 & 0xffffffff
        
        self.initial_state = Piece(number)
        
        return number
    
    def get_pseudo_legal_number(self):
        n1 = self.get_random() & 0xffff
        n2 = self.get_random() & 0xffff
        n3 = self.get_random() & 0xffff
        n4 = self.get_random() & 0xffff
        
        return Piece(n1 | n2 << 16 | n3 << 32 | n4 << 48)
    
    def get_magic_number_candidate(self):
        return self.get_pseudo_legal_number() & self.get_pseudo_legal_number() & self.get_pseudo_legal_number()

