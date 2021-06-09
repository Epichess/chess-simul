from piece import Piece


class Square:
    piece: Piece

    def __init__(self, piece: Piece = None):
        self.piece = piece

    def isEmpty(self) -> bool:
        if self.piece is None:
            return True
        else:
            return False
