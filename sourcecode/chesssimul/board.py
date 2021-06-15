from typing import Union

from square import Square
from piece import *
from coup import Move

IndexToLine = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
IndexToColumn = ['8', '7', '6', '5', '4', '3', '2', '1']

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
    move_list: list[Move]
    to_move: Color
    can_white_queen_side_castle: bool
    can_white_king_side_castle: bool
    can_black_queen_side_castle: bool
    can_black_king_side_castle: bool
    en_passant_target_square: tuple[int, int] or None
    halfmove_clock: int
    fullmove_number: int

    def __init__(self):
        self.move_list = list()

    def getSquare(self, square: str) -> Square:
        square_list = list(square)
        return self.board[Lines.get(square_list[1])][Columns.get(square_list[0])]

    def string_to_piece(piece: str) -> PieceType:
        switcher = {
            "King": PieceType.KING,
            "Queen": PieceType.QUEEN,
            "Rook": PieceType.ROOK,
            "Bishop": PieceType.BISHOP,
            "Knight": PieceType.KNIGHT,
        }
        return switcher.get(piece, None)

    def setEnPassantTargetSquare(self, line: int, column: int):
        self.en_passant_target_square = (line, column)

    def init_board(self):
        self.board = list()
        self.to_move = Color.WHITE
        self.can_black_king_side_castle = True
        self.can_black_queen_side_castle = True
        self.can_white_king_side_castle = True
        self.can_white_queen_side_castle = True
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
                    board_string += ' '
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

    def make_move(self, move: Move) -> bool:

        self.move_list.append(move)

        if move.end[0] in range(0, 8) and move.end[1] in range(0, 8):
            # postion de la pièce avant son déplacement dans l'échiquier
            start_square: Square = self.board[move.start[0]][move.start[1]]
            # Y a t'il une pièce à déplacer
            if not (start_square.isEmpty()):
                # type de la pièce que nous voulons déplacer
                type_piece_start: PieceType = start_square.piece.kind
                print(type_piece_start)
                # Si c'est le cavalier
                if type_piece_start == PieceType.KNIGHT:
                    print("vérification du coup du cavalier")
                    if self.move_knight(move):
                        return True
                elif type_piece_start == PieceType.BISHOP:
                    print("vérification du coup du fou")
                    if self.move_bishop(move):
                        return True
                elif type_piece_start == PieceType.PAWN:
                    print("vérification du coup du pion")
                    if self.move_pawn(move):
                        return True
                else:
                    return False
            else:
                print("Aucune pièce à déplacer")
                return False
        else:
            print("déplacement d'un pion en dehors de l'échiquier")
            return False

    def take_piece(self, move: Move) -> bool:
        start_square: Square = self.board[move.start[0]][move.start[1]]
        end_square: Square = self.board[move.end[0]][move.end[1]]
        if end_square.piece.color != start_square.piece.color:
            self.board[move.end[0]][move.end[1]].piece = start_square.piece
            self.board[move.start[0]][move.start[1]].piece = None
            print("piece taken")
            return True
        else:
            print("impossible to take piece of your own color")
            return False

    def move_piece(self, move: Move) -> bool:
        start_square: Square = self.board[move.start[0]][move.start[1]]
        self.board[move.end[0]][move.end[1]].piece = start_square.piece
        self.board[move.start[0]][move.start[1]].piece = None
        print("piece moved")
        return True

    def move_knight(self, move: Move) -> bool:
        # postion de la pièce avant son déplacement dans l'échiquier
        start_square: Square = self.board[move.start[0]][move.start[1]]
        # postion de la pièce après son déplacement dans l'échiquier
        end_square: Square = self.board[move.end[0]][move.end[1]]
        if move.end[0] == move.start[0] + 2 or move.end[0] == move.start[0] - 2:
            if move.end[1] == move.start[1] + 1 or move.end[1] == move.start[1] - 1:
                if end_square.isEmpty() is False:
                    return self.take_piece(move)
                else:
                    print("got here")
                    return self.move_piece(move)
            else:
                print("Impossible de déplacer le cavalier à cet endroit")
                return False

        elif move.end[1] == move.start[1] + 2 or move.end[1] == move.start[1] - 2:
            if move.end[0] == move.start[0] + 1 or move.end[0] == move.start[0] - 1:
                if end_square.isEmpty():
                    return self.move_piece(move)
                else:
                    return self.take_piece(move)
            else:
                print("Impossible de déplacer le cavalier à cet endroit")
                return False
        else:
            print("Impossible de déplacer le cavalier à cet endroit")
            return False

    def move_bishop(self, move: Move) -> bool:

        # variable test
        self.board[6][1].piece = None

        print(range(move.start[0], move.end[0]))
        # postion de la pièce avant son déplacement dans l'échiquier
        start_square: Square = self.board[move.start[0]][move.start[1]]
        # postion de la pièce après son déplacement dans l'échiquier
        end_square: Square = self.board[move.end[0]][move.end[1]]
        # Pion sur le chemin du fou
        for line in range(move.end[0]):
            print("line")
            print(line)
            # if (move.start[0] == line):

            for col in move.start[1:move.end[1]]:
                print(col)
                if not (self.board[line][col].isEmpty()):
                    ###Pièce sur le chemin du fou
                    print("Une pièce bloque la diagonale du fou")
                    break
                elif (line == move.end[0] and col == move.end[1]):
                    if (end_square.piece.color == start_square.piece.color):
                        ###Pièce de même color
                        print("prise impossible, pièce de même couleur")
                        break
                    if (end_square.piece.color != start_square.piece.color):
                        self.board[move.end[0]][move.end[1]] = start_square
        print('end')

    def move_pawn(self, move: Move) -> bool:
        start_square: Square = self.board[move.start[0]][move.start[1]]
        end_square: Square = self.board[move.end[0]][move.end[1]]
        # Pawns can only move forward one square at a time
        if start_square.piece.color == Color.BLACK:
            if move.end[0] == move.start[0] + 1 and move.end[1] == move.start[1] and end_square.isEmpty():
                if move.end[0] == 7:
                    self.promotion(move)
                else:
                    self.move_piece(move)
            # except for their very first move where they can move forward two squares.
            elif move.end[0] == move.start[0] + 2 and move.start[0] == 1 and move.end[1] == move.start[
                1] and end_square.isEmpty():
                self.setEnPassantTargetSquare(move.end[0] - 1, move.end[1])
                self.move_piece(move)
            # Pawns can only capture one square diagonally in front of them
            elif move.end[0] == move.start[0] + 1 and move.end[1] == move.start[1] - 1 or move.end[1] == move.start[1] + 1:
                if end_square.isEmpty() is False:
                    self.take_piece(move)
                else:
                    print("cannot move pawn here.")
                    return False
        elif start_square.piece.color == Color.WHITE:
            if move.end[0] == move.start[0] - 1 and move.end[1] == move.start[1] and end_square.isEmpty():
                if move.end[0] == 0:
                    self.promotion(move)
                else:
                    self.move_piece(move)
            elif move.end[0] == move.start[0] - 2 and move.start[0] == 6 and move.end[1] == move.start[1] and end_square.isEmpty():
                self.setEnPassantTargetSquare(move.end[0] + 1, move.end[1])
                self.move_piece(move)
            elif move.end[0] == move.start[0] - 1 and move.end[1] == move.start[1] - 1 or move.end[1] == move.start[
                1] + 1:
                if end_square.isEmpty() is False:
                    self.take_piece(move)
                else:
                    print("cannot move pawn here.")
                    return False
        else:
            return False

    def promotion(self, move: Move):
        newpiece_color = self.board[move.start[0]][move.start[1]].piece.color
        new_piece = Piece(move.promotion_kind, newpiece_color)
        self.board[move.start[0]][move.start[1]].piece = None
        self.board[move.end[0]][move.end[1]].piece = new_piece

    def board_to_fen(self) -> str:
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

        if self.en_passant_target_square is not None:
            enpassant = self.en_passant_target_square
            chessline = IndexToLine[enpassant[0]]
            column = enpassant[1]
            enpassant_column = column + 1
            chesscolumn = IndexToColumn[enpassant_column]
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
