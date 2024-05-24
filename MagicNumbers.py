from Pieces import Piece
from CustomRandom import Random
from Rooks import Rook
from Bishops import Bishop

class MagicNumbers:
    
    def __init__(self):
        self.random = Random()
        
        
    def get_occupancy_set(self, index, bits_in_mask, attack_mask):
        occupancy = Piece(0)
        
        for count in range(bits_in_mask):
            square = attack_mask.get_LSB()
            attack_mask = attack_mask.remove_bit(square)
            
            if index & (1 << count):
                occupancy = occupancy.set_bit(square)
                
        return occupancy
    
    def find_magic_numbers(self, square, relevant_bits, attack_mask, piece):
        occupancies = [Piece() for i in range(4096)]
        attacks = [Piece() for i in range(4096)]
        used_attacks = [Piece() for i in range(4096)]
        occupancy_indices = 1 << relevant_bits
        
        for index in range(occupancy_indices):
            occupancies[index] = self.get_occupancy_set(index, relevant_bits, attack_mask)
            piece.generate_attacks(occupancies[index])
            attacks[index] = piece.ATTACKS[square]
            
        for rand_ct in range(100000000):
            magic_number = self.random.get_magic_number_candidate()
            if ((magic_number * attack_mask) & 0xFF00000000000000).count_bits() < 6:
                continue
            
            fail = 0
            used_attacks = [Piece() for _ in range(4096)]
            
            for index in range(occupancy_indices):
                magic_index = (((occupancies[index] * magic_number) >> (64 - relevant_bits)) & 0xFFFFFFFF).PIECE
                if used_attacks[magic_index].PIECE == 0:
                    used_attacks[magic_index] = attacks[index]
                elif used_attacks[magic_index].PIECE != attacks[index].PIECE:
                    fail = 1
                    break
                    
            if not fail:
                return magic_number

        return Piece(0)
    
    def magic_numbers(self, piece):
        magic_numbers_list = []
        for square in range(64):
            magic_number = self.find_magic_numbers(square, piece.RELEVANT_BITS[square], piece.ATTACK_MASK[square], piece)
            magic_numbers_list.append(hex(magic_number.PIECE))
            print(f'Index = {square}, Magic Number = {magic_number.PIECE}')
        print()
        return magic_numbers_list
            

if __name__== '__main__':
    magic_instance = MagicNumbers()

    # Obtain magic numbers for Rooks and Bishops
    rook_magic_numbers = magic_instance.magic_numbers(Rook())
    bishop_magic_numbers = magic_instance.magic_numbers(Bishop())

    # Write magic numbers to a text file
    with open("magic_numbers.txt", "w") as file:
        file.write("Rook Magic Numbers:\n")
        file.write(", ".join(rook_magic_numbers))
        file.write("\n\nBishop Magic Numbers:\n")
        file.write(", ".join(bishop_magic_numbers))

    print("Magic numbers saved to 'magic_numbers.txt'.")