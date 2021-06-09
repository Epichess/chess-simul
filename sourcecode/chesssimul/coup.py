from typing import Tuple


class Move:
    start: Tuple[int, int]
    end: Tuple[int, int]

    def __init__(self, start, end):
        self.start = start
        self.end = end
