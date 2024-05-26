class Move:
    '''
        Move encoding
        0000 0000 0000 0000 0011 1111 -> source             = 0x3f
        0000 0000 0000 1111 1100 0000 -> target             = 0xfc0
        0000 0000 1111 0000 0000 0000 -> piece              = 0xf000
        0000 1111 0000 0000 0000 0000 -> promotion_to       = 0xf0000
        0001 0000 0000 0000 0000 0000 -> is capture?        = 0x100000
        0010 0000 0000 0000 0000 0000 -> is double push?    = 0x200000
        0100 0000 0000 0000 0000 0000 -> is en-passant?     = 0x400000
        1000 0000 0000 0000 0000 0000 -> is castling?       = 0x800000
    '''

    PIECE_TYPES = {
        1: 'P',  # Pawn
        2: 'R',  # Rook
        3: 'N',  # Knight
        4: 'B',  # Bishop
        5: 'Q',  # Queen
        6: 'K'   # King
    }

    def __init__(*args):
        self = args[0]
        if len(args) == 1:
            self.MOVE = 0
        else:
            source, target, piece, promotion_to, is_capture, is_double_push, is_en_passant, is_castling = args[1:]
            self.MOVE = self.encode_move(source, target, piece, promotion_to, is_capture, is_double_push, is_en_passant, is_castling)

    def encode_move(self, source, target, piece, promotion_to, is_capture, is_double_push, is_en_passant, is_castling):
        encoding = 0
        encoding |= source
        encoding |= target << 6
        encoding |= piece << 12
        encoding |= promotion_to << 16
        encoding |= is_capture << 20
        encoding |= is_double_push << 21
        encoding |= is_en_passant << 22
        encoding |= is_castling << 23

        return encoding

    def get_source(self):
        return self.MOVE & 0x3f

    def get_target(self):
        return (self.MOVE & 0xfc0) >> 6

    def get_piece(self):
        return (self.MOVE & 0xf000) >> 12

    def get_promotion(self):
        return (self.MOVE & 0xf0000) >> 16
    
    def is_capture(self):
        return (self.MOVE & 0x100000) >> 20
        
    def is_double_push(self):
        return (self.MOVE & 0x200000) >> 21

    def is_en_passant(self):
        return (self.MOVE & 0x400000) >> 22

    def is_castling(self):
        return (self.MOVE & 0x800000) >> 23

    def square_to_notation(self, bit_position):
        file_index = bit_position % 8
        rank_index = bit_position // 8
        return chr(ord('a') + file_index) + str(rank_index + 1)

    def piece_to_string(self, piece):
        color = 'W' if piece & 0x8 == 0 else 'B'
        piece_type = piece & 0x7
        return f'{color}{self.PIECE_TYPES.get(piece_type, "?")}'

    def __str__(self):
        source = self.square_to_notation(self.get_source())
        target = self.square_to_notation(self.get_target())
        promotion = self.get_promotion()
        piece = self.piece_to_string(self.get_piece())
        promotion_str = ''
        if promotion:
            promotion_str = f' (promotes to {self.PIECE_TYPES.get(promotion & 0x7, "?")})'
        capture_str = ' (capture)' if self.is_capture() else ''
        double_push_str = ' (double push)' if self.is_double_push() else ''
        en_passant_str = ' (en passant)' if self.is_en_passant() else ''
        castling_str = ' (castling)' if self.is_castling() else ''

        return f'{piece}{source} -> {target}{promotion_str}{capture_str}{double_push_str}{en_passant_str}{castling_str}'
        
    def __repr__(self):
        source = self.square_to_notation(self.get_source())
        target = self.square_to_notation(self.get_target())
        promotion = self.get_promotion()
        piece = self.piece_to_string(self.get_piece())
        promotion_str = ''
        if promotion:
            promotion_str = f' (promotes to {self.PIECE_TYPES.get(promotion & 0x7, "?")})'
        capture_str = ' (capture)' if self.is_capture() else ''
        double_push_str = ' (double push)' if self.is_double_push() else ''
        en_passant_str = ' (en passant)' if self.is_en_passant() else ''
        castling_str = ' (castling)' if self.is_castling() else ''

        return f'{piece}{source} -> {target}{promotion_str}{capture_str}{double_push_str}{en_passant_str}{castling_str}'
