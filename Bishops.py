from Pieces import Piece
import os
import pickle


class Bishop:
    def __init__(self, piece = 0x2400000000000024):
        self.PIECE = Piece(piece)
        self.WHITE = 0        
        self.BLACK = 1        
        self.RANKS = [Piece() for i in range(8)]
        self.ATTACKS = [Piece(0) for i in range(64)]
        self.ATTACK_MASK = [Piece(0) for i in range(64)]
        self.RELEVANT_BITS = [6,5,5,5,5,5,5,6,5,5,5,5,5,5,5,5,5,5,7,7,7,7,5,5,5,5,7,9,9,7,5,5,5,5,7,9,9,7,5,5,5,5,7,7,7,7,5,5,5,5,5,5,5,5,5,5,6,5,5,5,5,5,5,6]
        self.MAGIC_NUMBERS = [0 for i in range(64)]
        self.SLIDER_ATTACKS = [[Piece(0) for i in range(512)] for j in range(64)]
        self.initialize_ranks()
        self.initialize_mask()
        self.set_magic_numbers()
        self.slider_attacks_file = "slider_attacks_bishop.pkl"
        self.load_or_generate_slider_attacks()


    def set_magic_numbers(self):
        nums = [0x40040844404084, 0x2004208a004208, 0x10190041080202, 0x108060845042010, 0x581104180800210, 0x2112080446200010, 0x1080820820060210, 0x3c0808410220200, 0x4050404440404, 0x21001420088, 0x24d0080801082102, 0x1020a0a020400, 0x40308200402, 0x4011002100800, 0x401484104104005, 0x801010402020200, 0x400210c3880100, 0x404022024108200, 0x810018200204102, 0x4002801a02003, 0x85040820080400, 0x810102c808880400, 0xe900410884800, 0x8002020480840102, 0x220200865090201, 0x2010100a02021202, 0x152048408022401, 0x20080002081110, 0x4001001021004000, 0x800040400a011002, 0xe4004081011002, 0x1c004001012080, 0x8004200962a00220, 0x8422100208500202, 0x2000402200300c08, 0x8646020080080080, 0x80020a0200100808, 0x2010004880111000, 0x623000a080011400, 0x42008c0340209202, 0x209188240001000, 0x400408a884001800, 0x110400a6080400, 0x1840060a44020800, 0x90080104000041, 0x201011000808101, 0x1a2208080504f080, 0x8012020600211212, 0x500861011240000, 0x180806108200800, 0x4000020e01040044, 0x300000261044000a, 0x802241102020002, 0x20906061210001, 0x5a84841004010310, 0x4010801011c04, 0xa010109502200, 0x4a02012000, 0x500201010098b028, 0x8040002811040900, 0x28000010020204, 0x6000020202d0240, 0x8918844842082200, 0x4010011029020020]
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
            for m,n in zip(range(x + 1, 7), range(y + 1, 7)):
                pos = Piece(1) << (8 * m + n)
                self.ATTACK_MASK[i] |= pos
                
            for m,n in zip(range(x - 1, 0, -1), range(y + 1, 7)):
                pos = Piece(1) << (8 * m + n)
                self.ATTACK_MASK[i] |= pos
                
            for m,n in zip(range(x + 1, 7), range(y - 1, 0, -1)):
                pos = Piece(1) << (8 * m + n)
                self.ATTACK_MASK[i] |= pos

            for m,n in zip(range(x - 1, 0, -1), range(y - 1, 0, -1)):
                pos = Piece(1) << (8 * m + n)
                self.ATTACK_MASK[i] |= pos
                
    def generate_attacks(self, board):
        self.ATTACKS = [Piece(0) for i in range(64)]
        for i in range(64):
            x = i // 8
            y = i % 8
            for m,n in zip(range(x + 1, 8), range(y + 1, 8)):
                pos = Piece(1) << (8 * m + n)
                self.ATTACKS[i] |= pos
                if (board & pos).PIECE != 0:
                    break
                
            for m,n in zip(range(x - 1, -1, -1), range(y + 1, 8)):
                pos = Piece(1) << (8 * m + n)
                self.ATTACKS[i] |= pos
                if (board & pos).PIECE != 0:
                    break
                
            for m,n in zip(range(x + 1, 8), range(y - 1, -1, -1)):
                pos = Piece(1) << (8 * m + n)
                self.ATTACKS[i] |= pos
                if (board & pos).PIECE != 0:
                    break

            for m,n in zip(range(x - 1, -1, -1), range(y - 1, -1, -1)):
                pos = Piece(1) << (8 * m + n)
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
                magic_index = (((occupancy * self.MAGIC_NUMBERS[square]) >> (64 - relevant_bits)) & 0xFFFFFFFF).PIECE
                self.generate_attacks(occupancy)
                self.SLIDER_ATTACKS[square][magic_index] = self.ATTACKS[square]


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
            

Bishop()