from square import Square
from piece import *

Columns: dict[str, int] = {
    'a': 0,
    'b': 1,
    'c': 2,
    'd': 3,
    'e': 4,
    'f': 5,
    'g': 6,
    'h': 7
}

Lines: dict[str, int] = {
    '1': 7,
    '2': 6,
    '3': 5,
    '4': 4,
    '5': 3,
    '6': 2,
    '7': 1,
    '8': 0
}


class Board:
    board: list[list[Square]]
    to_move: Color
    can_white_queen_side_castle: bool
    can_white_king_side_castle: bool
    can_black_queen_side_castle: bool
    can_black_king_side_castle: bool
    en_passant_target_square: tuple[int, int] or None
    halfmove_clock: int
    fullmove_number: int

    def getSquare(self, square: str) -> Square:
        square_list = list(square)
        return self.board[Lines.get(square_list[1])][Columns.get(square_list[0])]

    def setEnPassantTargetSquare(self):
        self.en_passant_target_square = (4, 4)

    def init_board(self):
        self.board = list()
        self.to_move = Color.WHITE
        self.can_black_king_side_castle = True
        self.can_black_queen_side_castle = False
        self.can_white_king_side_castle = True
        self.can_white_queen_side_castle = False
        self.en_passant_target_square = None
        self.halfmove_clock = 0
        self.fullmove_number = 0
        for lin in range(8):
            self.board.append(list())
            for col in range(8):
                self.board[lin].append(Square())

        for col in range(8):
            self.board[Lines.get('7')][col].piece = str_to_piece['p']
            self.board[Lines.get('2')][col].piece = str_to_piece['P']
        self.getSquare('a1').piece = str_to_piece['R']
        self.getSquare('b1').piece = str_to_piece['N']
        self.getSquare('c1').piece = str_to_piece['B']
        self.getSquare('d1').piece = str_to_piece['Q']
        self.getSquare('e1').piece = str_to_piece['K']
        self.getSquare('f1').piece = str_to_piece['B']
        self.getSquare('g1').piece = str_to_piece['N']
        self.getSquare('h1').piece = str_to_piece['R']
        self.getSquare('a8').piece = str_to_piece['r']
        self.getSquare('b8').piece = str_to_piece['n']
        self.getSquare('c8').piece = str_to_piece['b']
        self.getSquare('d8').piece = str_to_piece['q']
        self.getSquare('e8').piece = str_to_piece['k']
        self.getSquare('f8').piece = str_to_piece['b']
        self.getSquare('g8').piece = str_to_piece['n']
        self.getSquare('h8').piece = str_to_piece['r']

    def to_unicode(self) -> str:
        board_string = ''
        for line in range(8):
            board_string += '|'
            for col in range(8):
                square = self.board[line][col]
                if square.isEmpty():
                    board_string += '  '
                else:
                    board_string += square.piece.to_unicode()
                board_string += '|'
            board_string += '\n'
        return board_string

    def move(self, lam: str):
        lamlist = list(lam)
        pawn_passant = ''
        start_square: Square = self.board[Lines.get(lam[1])][Columns.get(lam[0])]
        arrival_square: Square = self.board[Lines.get(lam[3])][Columns.get(lam[2])]
        arrival_square.piece = start_square.piece
        start_square.piece = None

    def to_fen(self) -> str:
        board_fen = ''
        for line in range(8):
            board_fen += '/'
            empty_squares = 0
            for col in range(8):
                square = self.board[line][col]
                if square.isEmpty():
                    empty_squares += 1
                    board_fen += ''
                else:
                    if empty_squares > 0:
                        empty_number = str(empty_squares)
                        board_fen += empty_number
                    piece = str(square.piece.piece_to_str())
                    board_fen += piece
                    empty_squares = 0
            if empty_squares > 0:
                empty_number = str(empty_squares)
                board_fen += empty_number
        board_fen = board_fen[1:]
        if self.to_move == Color.BLACK:
            board_fen += " b "
        else:
            board_fen += " w "

        if self.can_white_king_side_castle:
            board_fen += "K"
        if self.can_white_queen_side_castle:
            board_fen += "Q"
        if self.can_black_king_side_castle:
            board_fen += "k"
        if self.can_black_queen_side_castle:
            board_fen += "q"

        lines = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        columns = ['8', '7', '6', '5', '4', '3', '2', '1']


        if self.en_passant_target_square is not None:
            enpassant = self.en_passant_target_square
            chessline = lines[enpassant[0]]
            chesscolumn = columns[enpassant[1]]
            enpassant_target = ' ' + chessline + chesscolumn + ' '
            board_fen += enpassant_target
        else:
            board_fen += ' - '

        halfmove = str(self.halfmove_clock)
        board_fen += halfmove
        board_fen += ' '
        fullmove = str(self.fullmove_number)
        board_fen += fullmove

        return board_fen


board: Board = Board()
board.init_board()
print(board.to_unicode())
board.move('e2e4')
board.setEnPassantTargetSquare()
print(board.to_unicode())
print(board.to_fen())
print(board.board[0][0].piece.kind)
print(board.board[0][0].piece.color)
print(board.board[4][4].piece.kind)
print(board.board[4][4].piece.color)

