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
    en_passant_target_square: Square

    def getSquare(self, square: str) -> Square:
        square_list = list(square)
        return self.board[Lines.get(square_list[1])][Columns.get(square_list[0])]

    def init_board(self):
        self.board = list()
        for lin in range(8):
            self.board.append(list())
            for col in range(8):
                self.board[lin].append(Square())

        for col in range(8):
            self.board[Lines.get('7')][col].piece = str_to_piece['P']
            self.board[Lines.get('2')][col].piece = str_to_piece['p']
        self.getSquare('a1').piece = str_to_piece['r']
        self.getSquare('b1').piece = str_to_piece['n']
        self.getSquare('c1').piece = str_to_piece['b']
        self.getSquare('d1').piece = str_to_piece['q']
        self.getSquare('e1').piece = str_to_piece['k']
        self.getSquare('f1').piece = str_to_piece['b']
        self.getSquare('g1').piece = str_to_piece['n']
        self.getSquare('h1').piece = str_to_piece['r']
        self.getSquare('a8').piece = str_to_piece['R']
        self.getSquare('b8').piece = str_to_piece['N']
        self.getSquare('c8').piece = str_to_piece['B']
        self.getSquare('d8').piece = str_to_piece['Q']
        self.getSquare('e8').piece = str_to_piece['K']
        self.getSquare('f8').piece = str_to_piece['B']
        self.getSquare('g8').piece = str_to_piece['N']
        self.getSquare('h8').piece = str_to_piece['R']

    def to_unicode(self) -> str:
        board_string = ''
        for line in range(8):
            board_string += '|'
            for col in range(8):
                square = self.board[line][col]
                if square.isEmpty():
                    board_string += ' '
                else:
                    board_string += square.piece.to_unicode()
                board_string += '|'
            board_string += '\n'
        return board_string

    def move(self, lam: str):
        lamlist = list(lam)
        start_square: Square = self.board[Lines.get(lam[1])][Columns.get(lam[0])]
        arrival_square: Square = self.board[Lines.get(lam[3])][Columns.get(lam[2])]
        arrival_square.piece = start_square.piece
        start_square.piece = None


board: Board = Board()
board.init_board()
print(board.to_unicode())
board.move('e2e4')
print(board.to_unicode())
