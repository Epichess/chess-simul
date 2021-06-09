from sourcecode.chesssimul.piece import Piece, Color, PieceType


class Bishop(Piece):
    def __init__(self, color: Color):
        super(Bishop, self).__init__(PieceType.BISHOP, color)

    def Move(self):
        pass
