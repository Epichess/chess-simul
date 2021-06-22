
from square import Square
from piece import *
from coup import Move
from typing import Callable

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
    white_check: bool
    black_check: bool
    
    def __init__(self):
        self.move_list = list()

    def getSquare(self, square: str) -> Square:
        square_list = list(square)
        return self.board[Lines.get(square_list[1])][Columns.get(square_list[0])]

    # def switcher_make_move(self, move: Move):
    #     start_square: Square = self.board[move.start[0]][move.start[1]]
    #     type_piece_start: PieceType = start_square.piece.kind
    #     switcher = {
    #         PieceType.KING: self.move_knight(move),
    #         PieceType.QUEEN,
    #         PieceType.ROOK,
    #         PieceType.BISHOP,
    #         PieceType.KNIGHT,
    #         PieceType.KNIGHT,
    #     }
    #     return switcher.get(type_piece_start, None)

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
        self.white_check = False
        self.black_check = False
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

    def __str__(self):
        return self.to_unicode()

    def move(self, lam: str):
        lamlist = list(lam)
        pawn_passant = ''
        start_square: Square = self.board[Lines.get(lam[1])][Columns.get(lam[0])]
        arrival_square: Square = self.board[Lines.get(lam[3])][Columns.get(lam[2])]
        arrival_square.piece = start_square.piece
        start_square.piece = None

    def make_move(self, move: Move) -> bool:
        is_move_valid: bool

        move_switcher: dict[PieceType, Callable] = {
            PieceType.PAWN: self.move_pawn,
            PieceType.KNIGHT: self.move_knight,
            PieceType.ROOK: self.move_rook,
            PieceType.BISHOP: self.move_bishop,
            PieceType.QUEEN: self.move_queen,
            PieceType.KING: self.move_king
        }

        if 0 <= move.end[0] <= 7 and 0 <= move.end[1] <= 7:
            # postion de la pièce avant son déplacement dans l'échiquier
            start_square: Square = self.board[move.start[0]][move.start[1]]
            if not (start_square.isEmpty()):
                type_piece_start: PieceType = start_square.piece.kind
                is_move_valid = move_switcher.get(type_piece_start)(move, False)
            else:
                print("Aucune pièce à déplacer")
                is_move_valid = False
        else:
            print("déplacement d'une pièce en dehors de l'échiquier")
            is_move_valid = False

        if is_move_valid:
            self.king_check(move)
            self.move_list.append(move)
            if self.to_move == Color.WHITE:
                self.to_move = Color.BLACK
            else:
                self.to_move = Color.WHITE
        return is_move_valid

    def take_piece(self, move: Move, check: bool) -> bool:
        start_square: Square = self.board[move.start[0]][move.start[1]]
        end_square: Square = self.board[move.end[0]][move.end[1]]
        if end_square.piece.color != start_square.piece.color:
            if check is False:
                self.board[move.end[0]][move.end[1]].piece = start_square.piece
                self.board[move.start[0]][move.start[1]].piece = None
            print("piece taken")
            return True
        else:
            print("impossible to take piece of your own color")
            return False

    def move_piece(self, move: Move, check: bool) -> bool:
        if check is False:
            start_square: Square = self.board[move.start[0]][move.start[1]]
            self.board[move.end[0]][move.end[1]].piece = start_square.piece
            self.board[move.start[0]][move.start[1]].piece = None
            print("piece moved")
        return True
        

    def check_pin(self, move: Move) -> bool:
        for lin in range(8):
            for col in range(8):
                if self.board[lin][col].piece.kind == PieceType.KING:
                    for i in range(lin, 8):
                        if self.board[i][col]:
                            print("pas fini")

    def king_check(self, move: Move) -> bool:
        color_piece: Color = self.board[move.end[0]][move.end[1]].piece.color
        for lin in range(8):
            for col in range(8):
                if not self.board[lin][col].isEmpty():
                    if (self.board[lin][col].piece.kind == PieceType.KING) and (self.board[lin][col].piece.color != color_piece):
                        if self.board[move.end[0]][move.end[1]].piece.kind == PieceType.KNIGHT:
                            if self.move_knight(Move(move.end, [lin, col]), True):
                                if color_piece == Color.WHITE:
                                    self.black_check = True
                                else:
                                    self.white_check = True
                                print("check black / white = ", self.black_check, self.white_check)
                                return True
                            else:
                                print("pas d'échec")
                                return False
                        elif self.board[move.end[0]][move.end[1]].piece.kind == PieceType.BISHOP:
                            if self.move_bishop(Move(move.end, [lin, col]), True):
                                if color_piece == Color.WHITE:
                                    self.black_check = True
                                else:
                                    self.white_check = True
                                print("check black / white = ", self.black_check, self.white_check)
                                return True
                            else:
                                print("pas d'échec")
                                return False
                        elif self.board[move.end[0]][move.end[1]].piece.kind == PieceType.ROOK:
                            if self.move_rook(Move(move.end, [lin, col]), True):
                                if color_piece == Color.WHITE:
                                    self.black_check = True
                                else:
                                    self.white_check = True
                                print("check black / white = ", self.black_check, self.white_check)
                                return True
                            else:
                                print("pas d'échec")
                                return False
                        elif self.board[move.end[0]][move.end[1]].piece.kind == PieceType.QUEEN:
                            if self.move_queen(Move(move.end, [lin, col]), True):
                                if color_piece == Color.WHITE:
                                    self.black_check = True
                                else:
                                    self.white_check = True
                                print("check black / white = ", self.black_check, self.white_check)
                                return True
                            else:
                                print("pas d'échec")
                                return False
                        elif self.board[move.end[0]][move.end[1]].piece.kind == PieceType.KING:
                            if self.move_king(Move(move.end, [lin, col]), True):
                                if color_piece == Color.WHITE:
                                    self.black_check = True
                                else:
                                    self.white_check = True
                                print("check black / white = ", self.black_check, self.white_check)
                                return True
                            else:
                                print("pas d'échec")
                                return False
                        elif self.board[move.end[0]][move.end[1]].piece.kind == PieceType.KING:
                            if self.move_pawn(Move(move.end, [lin, col]), True):
                                if color_piece == Color.WHITE:
                                    self.black_check = True
                                else:
                                    self.white_check = True
                                print("check black / white = ", self.black_check, self.white_check)
                                return True
                            else:
                                print("pas d'échec")
                                return False
                        else:
                            print("Pas d'échec")
                            return False
        return False

    def move_knight(self, move: Move, check: bool) -> bool:
        # postion de la pièce avant son déplacement dans l'échiquier
        start_square: Square = self.board[move.start[0]][move.start[1]]
        # postion de la pièce après son déplacement dans l'échiquier
        end_square: Square = self.board[move.end[0]][move.end[1]]
        if move.end[0] == move.start[0] + 2 or move.end[0] == move.start[0] - 2:
            if move.end[1] == move.start[1] + 1 or move.end[1] == move.start[1] - 1:
                if end_square.isEmpty():
                    return self.move_piece(move, check)
                elif not end_square.isEmpty():
                    return self.take_piece(move, check)
            else:
                print("Impossible de déplacer le cavalier à cet endroit")
                return False

        elif move.end[1] == move.start[1] + 2 or move.end[1] == move.start[1] - 2:
            if move.end[0] == move.start[0] + 1 or move.end[0] == move.start[0] - 1:
                if end_square.isEmpty():
                    return self.move_piece(move, check)
                else:
                    return self.take_piece(move, check)
            else:
                print("Impossible de déplacer le cavalier à cet endroit")
                return False
        else:
            print("Impossible de déplacer le cavalier à cet endroit")
            return False

    def move_bishop(self, move: Move) -> bool:

        iteration_lin: int = abs(move.end[0] - move.start[0])
        iteration_col: int = abs(move.end[1] - move.start[1])
        lin_sign: int = 1
        col_sign: int = 1

        if iteration_lin == iteration_col:
            if (move.end[0] - move.start[0]) < 0:
                lin_sign = -1
            if (move.end[1] - move.start[1]) < 0:
                col_sign = -1

            for i in range(1, iteration_lin):
                # si la case testée n'est pas vide et qu'elle n'est pas l'emplacement finale de la pièce
                if not self.board[move.start[0] + lin_sign * i][move.start[1] + col_sign * i].isEmpty():
                    print("Une pièce bloque le passage du fou")
                    return False
            # si elle est vide et l'emplacement finale
            if self.board[move.end[0]][move.end[1]].isEmpty():
                return self.move_piece(move)
            # si elle n'est pas vide et que c'est l'emplacement finale
            else:
                return self.take_piece(move)
        else:
            return False

    def move_rook(self, move: Move) -> bool:
        iteration_lin: int = abs(move.end[0] - move.start[0])
        iteration_col: int = abs(move.end[1] - move.start[1])

        lin_sign: int = 1
        col_sign: int = 1

        # si le déplacement se fait bien en ligne droite
        if (move.end[0] != move.start[0] and move.end[1] == move.start[1]) or (move.end[0] == move.start[0] and move.end[1] != move.start[1]):

            # dans quelle direction se déplace t'on
            if (move.end[0] - move.start[0]) < 0:
                lin_sign = -1
            elif (move.end[1] - move.start[1]) < 0:
                col_sign = -1

            # déplacement en ligne
            if move.end[0] != move.start[0]:
                for i in range(1, iteration_lin):
                    if not self.board[move.start[0] + lin_sign * i][move.start[1]].isEmpty():
                        print("Une pièce bloque le passage de la tour")
                        return False
                # si elle est vide et l'emplacement finale
                if self.board[move.end[0]][move.end[1]].isEmpty():
                    return self.move_piece(move)
                # si elle n'est pas vide et que c'est l'emplacement finale
                else:
                    return self.take_piece(move)
            # déplacement en colonne
            elif move.end[1] != move.start[1]:
                for i in range(1, iteration_col):
                    if not self.board[move.start[0]][move.start[1] + col_sign * i].isEmpty():
                        print("Une pièce bloque le passage de la tour")
                        return False
                # si elle est vide et l'emplacement finale
                if self.board[move.end[0]][move.end[1]].isEmpty():
                    return self.move_piece(move)
                # si elle n'est pas vide et que c'est l'emplacement finale
                else:
                    return self.take_piece(move)
        else:
            print("Impossible de déplacer la tour à cet endroit")
            return False

    def move_queen(self, move: Move) -> bool:

        iteration_lin: float = abs(move.end[0] - move.start[0])
        iteration_col: float = abs(move.end[1] - move.start[1])

        lin_sign: int = 1
        col_sign: int = 1

        # si le déplacement se fait bien en ligne droite
        if (move.end[0] != move.start[0] and move.end[1] == move.start[1]) or (move.end[0] == move.start[0] and move.end[1] != move.start[1]):

            # dans quelle direction se déplace t'on
            if (move.end[0] - move.start[0]) < 0:
                lin_sign = -1
            elif (move.end[1] - move.start[1]) < 0:
                col_sign = -1

            # déplacement en ligne
            if move.end[0] != move.start[0]:
                for i in range(1, iteration_lin):
                    if not self.board[move.start[0] + lin_sign * i][move.start[1]].isEmpty():
                        print("Une pièce bloque le passage de la dame")
                        return False
                # si elle est vide et l'emplacement finale
                if self.board[move.end[0]][move.end[1]].isEmpty():
                    return self.move_piece(move)
                # si elle n'est pas vide et que c'est l'emplacement finale
                else:
                    return self.take_piece(move)
            # déplacement en colonne
            elif move.end[1] != move.start[1]:
                for i in range(1, iteration_col):
                    if not self.board[move.start[0]][move.start[1] + col_sign * i].isEmpty():
                        print("Une pièce bloque le passage de la dame")
                        return False
                # si elle est vide et l'emplacement finale
                if self.board[move.end[0]][move.end[1]].isEmpty():
                    return self.move_piece(move)
                # si elle n'est pas vide et que c'est l'emplacement finale
                else:
                    return self.take_piece(move)

        #si le déplacement se fait en diagonale
        elif iteration_lin == iteration_col:
            if (move.end[0] - move.start[0]) < 0:
                lin_sign = -1
            if (move.end[1] - move.start[1]) < 0:
                col_sign = -1

            for i in range(1, iteration_lin):
                # si la case testée n'est pas vide et qu'elle n'est pas l'emplacement finale de la pièce
                if not self.board[move.start[0] + lin_sign * i][move.start[1] + col_sign * i].isEmpty():
                    print("Une pièce bloque le passage de la dame")
                    return False
            # si elle est vide et l'emplacement finale
            if self.board[move.end[0]][move.end[1]].isEmpty():
                return self.move_piece(move)
            # si elle n'est pas vide et que c'est l'emplacement finale
            else:
                return self.take_piece(move)
        else:
            print("Impossible de déplacer la dame à cet endroit")
            return False
        
    def move_king(self, move: Move) -> bool:

        if (move.start[0] - 1 <= move.end[0] <= move.start[0] + 1) and (move.start[1] - 1 <= move.end[1] <= move.start[1] + 1):
            # si la case est vide et c'est l'emplacement final
            if self.board[move.end[0]][move.end[1]].isEmpty():
                return self.move_piece(move)
            # si elle n'est pas vide et que c'est l'emplacement final
            else:
                return self.take_piece(move)
        else:
            print("Impossible de déplacer le roi à cet endroit")
            return False


    def move_pawn(self, move: Move) -> bool:
        start_square: Square = self.board[move.start[0]][move.start[1]]
        end_square: Square = self.board[move.end[0]][move.end[1]]

        if start_square.piece.color == Color.BLACK:
            if move.end[1] == move.start[1] and end_square.isEmpty():
                # Pawns can only move forward one square at a time
                if move.end[0] == move.start[0] + 1:
                    if move.end[0] == 7:
                        return self.promotion(move)
                    else:
                        return self.move_piece(move)
                # except for their very first move where they can move forward two squares.
                elif move.end[0] == move.start[0] + 2 and move.start[0] == 1:
                    self.setEnPassantTargetSquare(move.end[0] - 1, move.end[1])
                    return self.move_piece(move)
            # Pawns can only capture one square diagonally in front of them
            elif move.end[0] == move.start[0] + 1 and (move.end[1] == move.start[1] - 1 or move.end[1] == move.start[1] + 1):
                if end_square.isEmpty() is False:
                    if move.end[0] == 7 and end_square.piece.color != start_square.piece.color:
                        return self.promotion(move)
                    else:
                        return self.take_piece(move)
                else:
                    print("cannot move pawn here.")
                    return False
        elif start_square.piece.color == Color.WHITE:
            if move.end[1] == move.start[1] and end_square.isEmpty():
                if move.end[0] == move.start[0] - 1:
                    if move.end[0] == 0:
                        return self.promotion(move)
                    else:
                        return self.move_piece(move)
                elif move.end[0] == move.start[0] - 2 and move.start[0] == 6:
                    self.setEnPassantTargetSquare(move.end[0] + 1, move.end[1])
                    return self.move_piece(move)
                elif move.end[0] == move.start[0] - 1 and (move.end[1] == move.start[1] - 1 or move.end[1] == move.start[1] + 1):
                    if end_square.isEmpty() is False:
                        if move.end[0] == 0 and end_square.piece.color != start_square.piece.color:
                            return self.promotion(move)
                        else:
                            return self.take_piece(move)
                    else:
                        print("cannot move pawn here.")
                        return False
        else:
            return False

    def promotion(self, move: Move) -> bool:
        if move.promotion_kind is None:
            return False
        new_piece_color = self.board[move.start[0]][move.start[1]].piece.color
        new_piece = Piece(move.promotion_kind, new_piece_color)
        self.board[move.start[0]][move.start[1]].piece = None
        self.board[move.end[0]][move.end[1]].piece = new_piece
        return True

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
