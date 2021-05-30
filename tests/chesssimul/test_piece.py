from sourcecode.chesssimul.piece import Piece, PieceType, Color

blackPawn: Piece = Piece(PieceType.PAWN, Color.BLACK)
batman: Piece = Piece(PieceType.KNIGHT, Color.BLACK)
blackBishop: Piece = Piece(PieceType.BISHOP, Color.BLACK)
blackRook: Piece = Piece(PieceType.ROOK, Color.BLACK)
blackQueen: Piece = Piece(PieceType.QUEEN, Color.BLACK)
blackKing: Piece = Piece(PieceType.KING, Color.BLACK)
whitePawn: Piece = Piece(PieceType.PAWN, Color.WHITE)
whiteKnight: Piece = Piece(PieceType.KNIGHT, Color.WHITE)
whiteBishop: Piece = Piece(PieceType.BISHOP, Color.WHITE)
whiteRook: Piece = Piece(PieceType.ROOK, Color.WHITE)
whiteQueen: Piece = Piece(PieceType.QUEEN, Color.WHITE)
whiteKing: Piece = Piece(PieceType.KING, Color.WHITE)


def test_unicode():
    assert blackPawn.to_unicode() == '\u265F'
    assert batman.to_unicode() == '\u265E'
    assert blackBishop.to_unicode() == '\u265D'
    assert blackRook.to_unicode() == '\u265C'
    assert blackQueen.to_unicode() == '\u265B'
    assert blackKing.to_unicode() == '\u265A'
    assert whitePawn.to_unicode() == '\u2659'
    assert whiteKnight.to_unicode() == '\u2658'
    assert whiteBishop.to_unicode() == '\u2657'
    assert whiteRook.to_unicode() == '\u2656'
    assert whiteQueen.to_unicode() == '\u2655'
    assert whiteKing.to_unicode() == '\u2654'
