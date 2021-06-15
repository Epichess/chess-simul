from sourcecode.chesssimul.board import *

def test_board():
    board = Board()
    board.init_board()
    assert board.board[1][5].piece.kind == PieceType.PAWN
