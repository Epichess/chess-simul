from typing import Tuple
from piece import PieceType


class Move:
    start: Tuple[int, int]
    end: Tuple[int, int]
    promotion_kind: PieceType

    def __init__(self, start, end, promotion=None):
        self.start = start
        self.end = end
        self.promotion_kind = promotion
