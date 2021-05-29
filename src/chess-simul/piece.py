from enum import Enum


class PieceType(Enum):
    PAWN = 1
    KNIGHT = 2
    BISHOP = 3
    ROOK = 4
    QUEEN = 5
    KING = 6


class Color(Enum):
    BLACK = 0
    WHITE = 1


class Piece:
    type: PieceType
    color: Color

    def to_unicode(self) -> str:
        white_switcher: dict[PieceType, str] = {
            PieceType.KING: '\u2654',
            PieceType.QUEEN: '\u2655',
            PieceType.ROOK: '\u2656',
            PieceType.BISHOP: '\u2657',
            PieceType.KNIGHT: '\u2658',
            PieceType.PAWN: '\u2659'
        }
        black_switcher: dict[PieceType, str] = {
            PieceType.KING: '\u265A',
            PieceType.QUEEN: '\u265B',
            PieceType.ROOK: '\u265C',
            PieceType.BISHOP: '\u265D',
            PieceType.KNIGHT: '\u265E',
            PieceType.PAWN: '\u265F'
        }

        switcher: dict[Color, dict[PieceType, str]] = {
            Color.BLACK: black_switcher,
            Color.WHITE: white_switcher
        }
        return switcher.get(self.color).get(self.type)
