import abc
from enum import Enum
from abc import ABC


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


class Piece():
    kind: PieceType
    color: Color

    def __init__(self, kind: PieceType, color: Color):
        self.color = color
        self.kind = kind

    def to_unicode(self) -> str:
        white_switcher: dict[PieceType, str] = {
            PieceType.KING: '\u265A',
            PieceType.QUEEN: '\u265B',
            PieceType.ROOK: '\u265C',
            PieceType.BISHOP: '\u265D',
            PieceType.KNIGHT: '\u265E',
            PieceType.PAWN: '\u265F'
        }
        black_switcher: dict[PieceType, str] = {
            PieceType.KING: '\u2654',
            PieceType.QUEEN: '\u2655',
            PieceType.ROOK: '\u2656',
            PieceType.BISHOP: '\u2657',
            PieceType.KNIGHT: '\u2658',
            PieceType.PAWN: '\u2659'
        }

        switcher: dict[Color, dict[PieceType, str]] = {
            Color.BLACK: black_switcher,
            Color.WHITE: white_switcher
        }
        return switcher.get(self.color).get(self.kind)


str_to_piece: dict[str, Piece] = {
    'K': Piece(PieceType.KING, Color.BLACK),
    'Q': Piece(PieceType.QUEEN, Color.BLACK),
    'R': Piece(PieceType.ROOK, Color.BLACK),
    'B': Piece(PieceType.BISHOP, Color.BLACK),
    'N': Piece(PieceType.KNIGHT, Color.BLACK),
    'P': Piece(PieceType.PAWN, Color.BLACK),
    'k': Piece(PieceType.KING, Color.WHITE),
    'q': Piece(PieceType.QUEEN, Color.WHITE),
    'r': Piece(PieceType.ROOK, Color.WHITE),
    'b': Piece(PieceType.BISHOP, Color.WHITE),
    'n': Piece(PieceType.KNIGHT, Color.WHITE),
    'p': Piece(PieceType.PAWN, Color.WHITE)
}
