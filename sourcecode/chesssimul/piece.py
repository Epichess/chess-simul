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


class Piece:
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

    def piece_to_str(self) -> str:
        white_piece: dict[PieceType, str] = {
            PieceType.KING: 'K',
            PieceType.QUEEN: 'Q',
            PieceType.ROOK: 'R',
            PieceType.BISHOP: 'B',
            PieceType.KNIGHT: 'N',
            PieceType.PAWN: 'P',
        }
        black_piece: dict[PieceType, str] = {
            PieceType.KING: 'k',
            PieceType.QUEEN: 'q',
            PieceType.ROOK: 'r',
            PieceType.BISHOP: 'b',
            PieceType.KNIGHT: 'n',
            PieceType.PAWN: 'p',
        }

        piece: dict[Color, dict[PieceType, str]] = {
            Color.BLACK: black_piece,
            Color.WHITE: white_piece
        }
        return piece.get(self.color).get(self.kind)

str_to_piece: dict[str, Piece] = {
    'k': Piece(PieceType.KING, Color.BLACK),
    'q': Piece(PieceType.QUEEN, Color.BLACK),
    'r': Piece(PieceType.ROOK, Color.BLACK),
    'b': Piece(PieceType.BISHOP, Color.BLACK),
    'n': Piece(PieceType.KNIGHT, Color.BLACK),
    'p': Piece(PieceType.PAWN, Color.BLACK),
    'K': Piece(PieceType.KING, Color.WHITE),
    'Q': Piece(PieceType.QUEEN, Color.WHITE),
    'R': Piece(PieceType.ROOK, Color.WHITE),
    'B': Piece(PieceType.BISHOP, Color.WHITE),
    'N': Piece(PieceType.KNIGHT, Color.WHITE),
    'P': Piece(PieceType.PAWN, Color.WHITE)
}

