from Pieces import Piece
import os
import pickle

class Rook:
    def __init__(self, piece = 0x8100000000000081):
        self.PIECE = Piece(piece)
        self.WHITE = 0        
        self.BLACK = 1        
        self.RANKS = [Piece() for i in range(8)]
        self.ATTACK_MASK = [Piece(0) for i in range(64)]
        self.ATTACKS = [Piece(0) for i in range(64)]
        self.RELEVANT_BITS = [12,11,11,11,11,11,11,12,11,10,10,10,10,10,10,11,11,10,10,10,10,10,10,11,11,10,10,10,10,10,10,11,11,10,10,10,10,10,10,11,11,10,10,10,10,10,10,11,11,10,10,10,10,10,10,11,12,11,11,11,11,11,11,12]
        self.MAGIC_NUMBERS = [0 for i in range(64)]
        self.SLIDER_ATTACKS = [[Piece(0) for i in range(4096)] for j in range(64)]
        self.slider_attacks_file = "slider_attacks_rook.pkl"
        self.initialize_ranks()
        self.initialize_mask()
        self.set_magic_numbers()
        self.load_or_generate_slider_attacks()

    def set_magic_numbers(self):
        nums = [0x8a80104000800020, 0x140002000100040, 0x2801880a0017001, 0x100081001000420, 0x200020010080420, 0x3001c0002010008, 0x8480008002000100, 0x2080088004402900, 0x800098204000, 0x2024401000200040, 0x100802000801000, 0x120800800801000, 0x208808088000400, 0x2802200800400, 0x2200800100020080, 0x801000060821100, 0x80044006422000, 0x100808020004000, 0x12108a0010204200, 0x140848010000802, 0x481828014002800, 0x8094004002004100, 0x4010040010010802, 0x20008806104, 0x100400080208000, 0x2040002120081000, 0x21200680100081, 0x20100080080080, 0x2000a00200410, 0x20080800400, 0x80088400100102, 0x80004600042881, 0x4040008040800020, 0x440003000200801, 0x4200011004500, 0x188020010100100, 0x14800401802800, 0x2080040080800200, 0x124080204001001, 0x200046502000484, 0x480400080088020, 0x1000422010034000, 0x30200100110040, 0x100021010009, 0x2002080100110004, 0x202008004008002, 0x20020004010100, 0x2048440040820001, 0x101002200408200, 0x40802000401080, 0x4008142004410100, 0x2060820c0120200, 0x1001004080100, 0x20c020080040080, 0x2935610830022400, 0x44440041009200, 0x280001040802101, 0x2100190040002085, 0x80c0084100102001, 0x4024081001000421, 0x20030a0244872, 0x12001008414402, 0x2006104900a0804, 0x1004081002402]
        for i in range(64):
            self.MAGIC_NUMBERS[i] = Piece(nums[i])
    
    def initialize_ranks(self):
        self.RANKS[0].PIECE = 0xFF
        for i in range(1, 8):
            self.RANKS[i] = self.RANKS[i - 1] << 8
            
    def initialize_mask(self):
        for i in range(64):
            x = i // 8
            y = i % 8
            for m in range(x + 1, 7):
                self.ATTACK_MASK[i] |= (Piece(1) << (8 * m + y))
                
            for m in range(x - 1, 0, -1):
                self.ATTACK_MASK[i] |= (Piece(1) << (8 * m + y))
                
            for n in range(y + 1, 7):
                self.ATTACK_MASK[i] |= (Piece(1) << (8 * x + n))
                
            for n in range(y - 1, 0, -1):
                self.ATTACK_MASK[i] |= (Piece(1) << (8 * x + n))
                
    def generate_attacks(self, board):
        self.ATTACKS = [Piece(0) for i in range(64)]
        for i in range(64):
            x = i // 8
            y = i % 8
            for m in range(x + 1, 8):
                pos = Piece(1) << (8 * m + y)
                self.ATTACKS[i] |= pos
                if (board & pos).PIECE != 0:
                    break
                
            for m in range(x - 1, -1, -1):
                pos = Piece(1) << (8 * m + y)
                self.ATTACKS[i] |= pos
                if (board & pos).PIECE != 0:
                    break
                
            for n in range(y + 1, 8):
                pos = Piece(1) << (8 * x + n)
                self.ATTACKS[i] |= pos
                if (board & pos).PIECE != 0:
                    break
                
            for n in range(y - 1, -1, -1):
                pos = Piece(1) << (8 * x + n)
                self.ATTACKS[i] |= pos
                if (board & pos).PIECE != 0:
                    break

    def generate_slider_attacks(self):
        
        for square in range(64):
            attack_mask = self.ATTACK_MASK[square]
            relevant_bits = self.RELEVANT_BITS[square]
            occupancy_indices = 1 << relevant_bits
            for index in range(occupancy_indices):
                occupancy = self.get_occupancy_set(index, relevant_bits, attack_mask)
                magic_index = ((occupancy * self.MAGIC_NUMBERS[square]) >> (64 - relevant_bits)) & 0xFFFFFFFF
                self.generate_attacks(occupancy)
                self.SLIDER_ATTACKS[square][magic_index.PIECE] = self.ATTACKS[square]

            print(square)



    def get_occupancy_set(self, index, bits_in_mask, attack_mask):
        occupancy = Piece(0)
        
        for count in range(bits_in_mask):
            square = attack_mask.get_LSB()
            attack_mask = attack_mask.remove_bit(square)
            
            if index & (1 << count):
                occupancy = occupancy.set_bit(square)
                
        return occupancy

    def get_attack(self, square, occupancy):

        occupancy &= self.ATTACK_MASK[square]
        occupancy *= self.MAGIC_NUMBERS[square]
        occupancy >>= (64 - self.RELEVANT_BITS[square])

        return self.SLIDER_ATTACKS[square][occupancy.PIECE]


    def save_slider_attacks(self):
        with open(self.slider_attacks_file, 'wb') as f:
            pickle.dump(self.SLIDER_ATTACKS, f)

    def load_slider_attacks(self):
        with open(self.slider_attacks_file, 'rb') as f:
            self.SLIDER_ATTACKS = pickle.load(f)

    def load_or_generate_slider_attacks(self):
        if os.path.exists(self.slider_attacks_file):
            self.load_slider_attacks()
        else:
            self.generate_slider_attacks()
            self.save_slider_attacks()



Rook()