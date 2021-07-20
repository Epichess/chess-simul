from sourcecode.chesssimul.board import *


def test_board_init():
    board = Board()
    board.init_board()
    a2 = board.board[Lines['2']][Columns['a']]
    assert a2.piece.color == Color.WHITE
    assert a2.piece.kind == PieceType.PAWN


def test_move_knight():
    board = Board()
    board.init_board()
    board.make_move(Move((7, 6), (5, 5)))
    f3 = board.board[5][5]
    f5 = board.board[3][5]
    g1 = board.board[7][6]
    g8 = board.board[0][6]
    h2 = board.board[6][7]
    h6 = board.board[2][7]
    assert g1.piece is None
    assert f3.piece.kind == PieceType.KNIGHT
    assert f3.piece.color == Color.WHITE

    board.make_move(Move((0, 6), (2, 7)))
    assert g8.piece is None
    assert h6.piece.kind == PieceType.KNIGHT
    assert h6.piece.color == Color.BLACK

    board.make_move(Move((5, 5), (6, 7)))
    assert f3.piece.kind == PieceType.KNIGHT
    assert f3.piece.color == Color.WHITE
    assert h2.piece.kind == PieceType.PAWN
    assert h2.piece.color == Color.WHITE
    assert len(board.move_list) == 2

    board.make_move(Move((5, 5), (4, 7)))
    board.make_move(Move((2, 7), (3, 5)))
    board.make_move(Move((4, 7), (3, 5)))
    assert f5.piece.kind == PieceType.KNIGHT
    assert f5.piece.color == Color.WHITE

def test_check():
    board = Board()
    # reset
    board.fen_to_board = ("3k4/8/8/8/8/5N2/8/3K2r1 w - - 0 1")

    # move's knight / king check by rook
    assert board.king_check == True
    assert board.white_check == True
    assert board.make_move(Move((5, 5), (0, 6))) == True
    assert board.white_check == False
    print("should True")
    print(board.to_unicode())

    # reset
    board.fen_to_board = ("3k4/8/8/8/8/5N2/8/3K2r1 w - - 0 1")

    # move's knight / king check by rook
    assert board.king_check == True
    assert board.white_check == True
    assert ((5, 5), (3, 4)) in board.pos_piece_pin == True
    assert board.make_move(Move((5, 5), (3, 4))) == False
    print("should False")
    print(board.to_unicode())
    
    # move king to remove knight pin by rook
    assert board.make_move(Move((7, 3), (6, 2))) == True
    assert board.king_check == False
    assert board.white_check == False
    assert board.pos_piece_pin.length == 0
    print(board.to_unicode())

    # reset
    board.fen_to_board = ("3k4/8/8/8/8/5N2/8/3K2r1 w - - 0 1")

    # move's king check check by rook
    assert board.make_move(Move((7, 3), (6, 3))) == True
    print("should True")
    print(board.to_unicode())

    # reset
    board.fen_to_board = ("3k4/8/8/8/8/5N2/8/3K2r1 w - - 0 1")

    # move's king check check by rook
    assert board.make_move(Move((7, 3), (7, 2))) == False
    print("should False")
    print(board.to_unicode())

    

