from typing import Tuple
from piece import PieceType
from piece import Piece


class Move:
    start: Tuple[int, int]
    end: Tuple[int, int]
    promotion_kind: PieceType
    piece: Piece
    eat: bool
    is_castled: bool
    castling: str

    def __init__(self, start, end, promotion=None):
        self.start = start
        self.end = end
        self.promotion_kind = promotion
        self.eat = False
        self.is_castled = False
        self.castling = ''