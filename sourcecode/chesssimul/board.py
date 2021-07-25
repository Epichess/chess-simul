from square import Square
from piece import *
from move import Move
from typing import BinaryIO, Callable, List
#from log import *
from copy import copy, deepcopy

#######################################
# create logger with 'spam_application'
#logger = logging.getLogger("My_app")
#logger.setLevel(logging.DEBUG)
#
## create console handler with a higher log level
#ch = logging.StreamHandler()
#ch.setLevel(logging.DEBUG)
#
#ch.setFormatter(CustomFormatter())
#
#logger.addHandler(ch)
#######################################

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
    list_white_check: list()
    list_black_check: list()
    list_white_pin: list()
    list_black_pin: list()
    pin_color: list()
    
    def __init__(self):
        self.move_list = list()

    def getSquare(self, square: str) -> Square:
        square_list = list(square)
        return self.board[Lines.get(square_list[1])][Columns.get(square_list[0])]

    def setEnPassantTargetSquare(self, line: int, column: int):
        self.en_passant_target_square = (line, column)

    def init_board(self):
        self.pin_color = list()
        self.list_white_check = list()
        self.list_black_check = list()
        self.list_white_pin = list()
        self.list_black_pin = list()
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

    def restore_board(self, cp):
        board_restored = list()
        for i in range(8):
        	board_restored.append([0] * 8)
        for lin in range(8):
            for col in range(8):
                board_restored[lin][col] = cp[lin][col]
        return board_restored
        

    def make_move(self, move: Move) -> bool:
        is_move_valid: bool = False

        if (0 <= move.end[0] <= 7 and 0 <= move.end[1] <= 7) and (move.start != move.end):
            # postion de la pièce avant son déplacement dans l'échiquier
            start_square: Square = self.board[move.start[0]][move.start[1]]
            # vérification qu'il y a une pièce à déplacer et qu'elle ne soit pas dans la liste list_piece_pin qui empêche l'échec de son roi
            self.king_check()
            if (not start_square.isEmpty()) and start_square.piece.color == self.to_move:
                type_piece_start: PieceType = start_square.piece.kind

                # copy board to test move
                #copy_board = self.board
                copy_board = deepcopy(self.board)

                move_switcher: dict[PieceType, Callable] = {                    
                            PieceType.PAWN: self.move_pawn,
                            PieceType.KNIGHT: self.move_knight,
                            PieceType.ROOK: self.move_rook,
                            PieceType.BISHOP: self.move_bishop,
                            PieceType.QUEEN: self.move_queen,
                            PieceType.KING: self.move_king 
                        }

                type_piece_cp: PieceType = copy_board[move.start[0]][move.start[1]].piece.kind
                color_piece_cp: Color = copy_board[move.start[0]][move.start[1]].piece.color


                if move_switcher.get(type_piece_cp)(move, False):
                    self.king_check()
                    print('check white king')
                    print(self.white_check)
                    if (not self.white_check and color_piece_cp == Color.WHITE) or (not self.black_check and color_piece_cp == Color.BLACK):

                        #is_move_valid = move_switcher.get(type_piece_cp)(move, False)
                        is_move_valid = True
                    else:
                        self.board = copy_board
                        #self.board = self.restore_board(copy_board)
                        is_move_valid = False
                        print('The king will be check by that move')
                        return False
                else:
                    print('déplacement interdit')
                    self.board = copy_board
                    is_move_valid = False
                    return False
            else:
                print("Aucune pièce à déplacer ou pas au tour de cette couleur")
                is_move_valid = False
        else:
            print("déplacement d'une pièce en dehors de l'échiquier ou pièce non déplacée")
            is_move_valid = False

        if is_move_valid:
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
                move.eat = True
                print("piece taken")
            if end_square.piece.kind == PieceType.KING:
                if end_square.piece.color == Color.WHITE:
                    self.list_white_check.append((move.start[0], move.start[1]))
                    self.white_check = True
                elif end_square.piece.color == Color.BLACK:
                    self.list_black_check.append((move.start[0], move.start[1]))
                    self.black_check = True
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

    def queen_castle(self, move: Move):
        start_square: Square = self.board[move.start[0]][move.start[1]]
        end_square: Square = self.board[move.end[0]][move.end[1]]
        start_line = move.start[0]
        start_col = move.start[1]
        rook_start_square: Square = self.board[start_line][start_col - 4]
        rook_end_square: Square = self.board[start_line][start_col - 1]

        if self.king_check():
            rook_end_square.piece = rook_start_square.piece
            rook_start_square.piece = None
            end_square.piece = start_square.piece
            start_square.piece = None

            move.is_castled = True
            move.castling = 'QUEEN_CASTLING'
            print("Queen castling.")
            return True
        else:
            print("Cannot queen castle because king will be in check.")
            return False

    def king_castle(self, move: Move):
        start_square: Square = self.board[move.start[0]][move.start[1]]
        end_square: Square = self.board[move.end[0]][move.end[1]]
        start_line = move.start[0]
        start_col = move.start[1]
        rook_start_square: Square = self.board[start_line][start_col + 3]
        rook_end_square: Square = self.board[start_line][start_col + 1]

        if self.king_check():
            rook_end_square.piece = rook_start_square.piece
            rook_start_square.piece = None
            end_square.piece = start_square.piece
            start_square.piece = None

            move.is_castled = True
            move.castling = 'KING_CASTLING'
            print("King castling.")
            return True
        else:
            print("Cannot king castle because king will be in check.")
            return False

    def king_check(self) -> bool:

        # réinitialisation de la liste des pièces qui mettent en echec le roi
        self.list_white_check.clear()
        self.list_black_check.clear()
        self.list_white_pin.clear()
        self.list_black_pin.clear()
        self.pin_color.clear()
        
        self.white_check = False
        self.black_check = False

        move_switcher: dict[PieceType, Callable] = {
            PieceType.ROOK: self.move_rook,
            PieceType.BISHOP: self.move_bishop,
            PieceType.QUEEN: self.move_queen,
        }
        
        color_switcher: dict[Color, Callable] = {
            Color.WHITE: self.list_black_pin,
            Color.BLACK: self.list_white_pin
        }

        # modélisation du board en matrice 8x8
        model_board = list()
        #initialisation de la matrice du board à 0
        for i in range(8):
        	model_board.append([0] * 8)

        coup_knight: list[int] = list([2, 1])
        sign: list[int] = list([1, -1])
        for lin in range(8):
            for col in range(8):
                if not self.board[lin][col].isEmpty():
                    type_piece_start: PieceType = self.board[lin][col].piece.kind
                    color_piece_start: PieceType = self.board[lin][col].piece.color

                    #test move khight
                    if self.board[lin][col].piece.kind == PieceType.KNIGHT:
                        for i in range(2):
                            for n in range(2):
                                if 0 <= lin + sign[n] * coup_knight[i] <= 7 and 0 <= col + sign[n] * list(reversed(coup_knight))[i] <= 7:
                                    if self.move_knight(Move([lin, col], [lin + sign[n] * coup_knight[i], col + sign[n] * list(reversed(coup_knight))[i]]), True):
                                        model_board[lin + sign[n] * coup_knight[i]][col + sign[n] * list(reversed(coup_knight))[i]] = 1
                                else:
                                    print("déplacement hors de l'échiquier")
                        for i in range(2):
                            for n in range(2):
                                if 0 <= lin + list(reversed(sign))[n] * coup_knight[i] <= 7 and 0 <= col - list(reversed(sign))[n] * list(reversed(coup_knight))[i] <= 7:
                                    if self.move_knight(Move([lin, col], [lin + list(reversed(sign))[n] * coup_knight[i], col - list(reversed(sign))[n] * list(reversed(coup_knight))[i]]), True):
                                        model_board[lin + list(reversed(sign))[n] * coup_knight[i]][col - list(reversed(sign))[n] * list(reversed(coup_knight))[i]] = 1
                                else:
                                    print("déplacement hors de l'échiquier")
                    
                    # test move rook et dame pour ses déplacements en lignes
                    elif self.board[lin][col].piece.kind == PieceType.ROOK or self.board[lin][col].piece.kind == PieceType.QUEEN:
                        for i in range(2):
                            for j in range(8):
                                if 0 <= lin + sign[i] * j <= 7 and 0 <= col <= 7:
                                    if move_switcher.get(type_piece_start)(Move([lin, col], [lin + sign[i] * j, col]), True):
                                        model_board[lin + sign[i] * j][col] = 1
                                        if not self.board[lin + sign[i] * j][col].isEmpty():
                                            if self.board[lin + sign[i] * j][col].piece.kind != PieceType.KING:
                                                if 0 < lin + sign[i] * j < 7 and 0 < col < 7:
                                                    for k in range(1, 8):
                                                        if 0 <= (lin + sign[i] * j) + (sign[i] * k) <= 7 and 0 <= col <= 7:
                                                            if not self.board[(lin + sign[i] * j) + (sign[i] * k)][col].isEmpty():
                                                                #logger.warning("coordonné board : %s", self.board[(lin + sign[i] * j) + (sign[i] * k)][col].piece.kind)
                                                                if self.board[(lin + sign[i] * j) + (sign[i] * k)][col].piece.kind == PieceType.KING:
                                                                    color_switcher.get(color_piece_start).append((lin + sign[i] * j, col))
                                                                    self.pin_color.append(self.board[lin + sign[i] * j][col].piece.color)
                                                                else:
                                                                    break
                                else:
                                    print("déplacement hors de l'échiquier")

                        for i in range(2):
                            for j in range(8):
                                if 0 <= lin <= 7 and 0 <= col + sign[i] * j <= 7:
                                    if move_switcher.get(type_piece_start)(Move([lin, col], [lin, col + sign[i] * j]), True):
                                        model_board[lin][col + sign[i] * j] = 1
                                        # test si il y a une pièce qui empêche le check (stratégie pin)
                                        if not self.board[lin][col + sign[i] * j].isEmpty():
                                            if self.board[lin][col + sign[i] * j].piece.kind != PieceType.KING:
                                                if 0 < lin < 7 and 0 < col + sign[i] * j < 7:
                                                    for k in range(1, 8):
                                                        if 0 <= lin <= 7 and 0 <= ((col + sign[i] * j) + (sign[i] * k)) <= 7:
                                                            #logger.warning("k et sens: %s %s", k, sign[i])
                                                            if not self.board[lin][(col + sign[i] * j) + (sign[i] * k)].isEmpty():
                                                                #logger.warning("coordonné board : %s", self.board[lin][(col + sign[i] * j) + (sign[i] * k)].piece.kind)
                                                                if self.board[lin][(col + sign[i] * j) + (sign[i] * k)].piece.kind == PieceType.KING:
                                                                    #logger.warning("king")
                                                                    color_switcher.get(color_piece_start).append((lin, col + sign[i] * j))
                                                                    self.pin_color.append(self.board[lin][col + sign[i] * j].piece.color)
                                                                else:
                                                                    #logger.critical("break")
                                                                    break
                                else:
                                    print("déplacement hors de l'échiquier")

                    # test move bishop et dame pour ses déplacements en diagonales
                    if self.board[lin][col].piece.kind == PieceType.BISHOP or self.board[lin][col].piece.kind == PieceType.QUEEN:
                        for i in range(2):
                            for j in range(8):
                                if 0 <= lin + sign[i] * j <= 7 and 0 <= col + sign[i] * j <= 7:
                                    if move_switcher.get(type_piece_start)(Move([lin, col], [lin + sign[i] * j, col + sign[i] * j]), True):
                                        model_board[lin + sign[i] * j][col + sign[i] * j] = 1
                                        # test si il y a une pièce qui empêche le check (stratégie pin)
                                        if not self.board[lin + sign[i] * j][col + sign[i] * j].isEmpty():
                                            if self.board[lin + sign[i] * j][col + sign[i] * j].piece.kind != PieceType.KING:
                                                if 0 < lin + sign[i] * j < 7 and 0 < col + sign[i] * j < 7:
                                                    for k in range(1, 8):
                                                        if 0 <= ((lin + sign[i] * j) + (sign[i] * k)) <= 7 and 0 <= ((col + sign[i] * j) + (sign[i] * k)) <= 7:
                                                            if not self.board[(lin + sign[i] * j) + (sign[i] * k)][(col + sign[i] * j) + (sign[i] * k)].isEmpty():
                                                                #logger.warning("coordonné board : %s", self.board[(lin + sign[i] * j) + (sign[i] * k)][(col + sign[i] * j) + (sign[i] * k)].piece.kind)
                                                                if self.board[(lin + sign[i] * j) + (sign[i] * k)][(col + sign[i] * j) + (sign[i] * k)].piece.kind == PieceType.KING:
                                                                    #logger.warning("king")
                                                                    color_switcher.get(color_piece_start).append((lin + sign[i] * j, col + sign[i] * j))
                                                                    self.pin_color.append(self.board[lin + sign[i] * j][col + sign[i] * j].piece.color)
                                                                else:
                                                                    break
                                else:
                                    print("déplacement hors de l'échiquier")
                        for i in range(2):
                            for j in range(8):
                                if 0 <= lin + list(reversed(sign))[i] * j <= 7 and 0 <= col + sign[i] * j <= 7:
                                    if move_switcher.get(type_piece_start)(Move([lin, col], [lin + list(reversed(sign))[i] * j, col + sign[i] * j]), True):
                                        model_board[lin + list(reversed(sign))[i] * j][col + sign[i] * j] = 1
                                        # test si il y a une pièce qui empêche le check (stratégie pin)
                                        if not self.board[lin + list(reversed(sign))[i] * j][col + sign[i] * j].isEmpty():
                                            if self.board[lin + list(reversed(sign))[i] * j][col + sign[i] * j].piece.kind != PieceType.KING:
                                                if 0 < lin + list(reversed(sign))[i] * j < 7 and 0 < col + sign[i] * j < 7:
                                                    for k in range(1, 8):
                                                        if 0 <= (lin + list(reversed(sign))[i] * j) + (list(reversed(sign))[i] * k) <= 7 and 0 <= ((col + sign[i] * j) + sign[i] * k) <= 7:
                                                            if not self.board[(lin + list(reversed(sign))[i] * j) + (list(reversed(sign))[i] * k)][((col + sign[i] * j) + sign[i] * k)].isEmpty():
                                                                #logger.warning("coordonné board : %s", ([(lin + list(reversed(sign))[i] * j) + (list(reversed(sign))[i] * k)], [(col + sign[i] * j) + sign[i] * k]))
                                                                if self.board[(lin + list(reversed(sign))[i] * j) + (list(reversed(sign))[i] * k)][((col + sign[i] * j) + sign[i] * k)].piece.kind == PieceType.KING:
                                                                    #logger.warning("king")
                                                                    color_switcher.get(color_piece_start).append((lin + list(reversed(sign))[i] * j, col + sign[i] * j))
                                                                    self.pin_color.append(self.board[lin + list(reversed(sign))[i] * j][col + sign[i] * j].piece.color)
                                                                else:
                                                                    break
                                else:
                                    print("déplacement hors de l'échiquier")

                    # test move pawn
                    elif self.board[lin][col].piece.kind == PieceType.PAWN:
                        # diagonal movement
                        for i in range(2):
                            if 0 <= lin + sign[i] <= 7 and 0 <= col + sign[i] <= 7:
                                if self.move_pawn(Move([lin, col], [lin + sign[i], col + sign[i]]), True):
                                    model_board[lin + sign[i]][col + sign[i]] = 1
                            else:
                                print("déplacement hors de l'échiquier")
                        # diagonal movement
                        for i in range(2):
                            if 0 <= lin + sign[i] <= 7 and 0 <= col + list(reversed(sign))[i] <= 7:
                                if self.move_pawn(Move([lin, col], [lin + sign[i], col + list(reversed(sign))[i]]), True):
                                    model_board[lin + sign[i]][col + list(reversed(sign))[i]] = 1
                            else:
                                print("déplacement hors de l'échiquier")
                        # linear movement
                        for i in range(2):
                            if 0 <= lin + sign[i] <= 7 and 0 <= col <= 7:
                                if self.move_pawn(Move([lin, col], [lin + sign[i], col]), True):
                                    model_board[lin + sign[i]][col] = 1
                            else:
                                print("déplacement hors de l'échiquier")
                        # linear movement
                        for i in range(2):
                            if 0 <= lin <= 7 and 0 <= col + list(reversed(sign))[i] <= 7:
                                if self.move_pawn(Move([lin, col], [lin, col + list(reversed(sign))[i]]), True):
                                    model_board[lin][col + list(reversed(sign))[i]] = 1
                            else:
                                print("déplacement hors de l'échiquier")

                    # test move king
                    elif self.board[lin][col].piece.kind == PieceType.KING:

                        # diagonal movement
                        for i in range(2):
                            if 0 <= lin + sign[i] <= 7 and 0 <= col + sign[i] <= 7:
                                if self.move_king(Move((lin, col), (lin + sign[i], col + sign[i])), True):
                                    model_board[lin + sign[i]][col + sign[i]] = 1
                            else:
                                print("déplacement hors de l'échiquier")
                        for i in range(2):
                            if 0 <= lin + sign[i] <= 7 and 0 <= col + list(reversed(sign))[i] <= 7:
                                if self.move_king(Move([lin, col], [lin + sign[i], col + list(reversed(sign))[i]]), True):
                                    model_board[lin + sign[i]][col + list(reversed(sign))[i]] = 1
                            else:
                                print("déplacement hors de l'échiquier")
                        
                        # linear movement
                        for i in range(2):
                            if 0 <= lin + sign[i] <= 7 and 0 <= col <= 7:
                                if self.move_king(Move([lin, col], [lin + sign[i], col]), True):
                                    model_board[lin + sign[i]][col] = 1
                            else:
                                print("déplacement hors de l'échiquier")

                        for i in range(2):
                            if 0 <= lin <= 7 and 0 <= col + sign[i] <= 7:
                                if self.move_king(Move([lin, col], [lin, col + sign[i]]), True):
                                    model_board[lin][col + sign[i]] = 1
                            else:
                                print("déplacement hors de l'échiquier")

        ############################
        ############test############
        ############################
        print(model_board[0])
        print(model_board[1])
        print(model_board[2])
        print(model_board[3])
        print(model_board[4])
        print(model_board[5])
        print(model_board[6])
        print(model_board[7])
        
        print(self.to_unicode())

        #logger.warning("white_check : %s", self.white_check)
        #logger.warning("black_check : %s", self.black_check)
        #logger.warning("list_white_check : %s", self.list_white_check)
        #logger.warning("list_black_check : %s", self.list_black_check)
        #logger.warning("list_white_pin : %s", self.list_white_pin)
        #logger.warning("list_black_pin : %s", self.list_black_pin)
        #logger.warning("pin_color : %s", self.pin_color)
        ############################
        ############test############
        ############################

        if self.white_check:
            return True
        if self.black_check:
            return True

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

    def move_bishop(self, move: Move, check: bool) -> bool:

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
                return self.move_piece(move, check)
            # si elle n'est pas vide et que c'est l'emplacement finale
            else:
                return self.take_piece(move, check)
        else:
            return False

    def move_rook(self, move: Move, check: bool) -> bool:
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
                    return self.move_piece(move, check)
                # si elle n'est pas vide et que c'est l'emplacement finale
                else:
                    return self.take_piece(move,check)
            # déplacement en colonne
            elif move.end[1] != move.start[1]:
                for i in range(1, iteration_col):
                    if not self.board[move.start[0]][move.start[1] + col_sign * i].isEmpty():
                        print("Une pièce bloque le passage de la tour")
                        return False
                # si elle est vide et l'emplacement finale
                if self.board[move.end[0]][move.end[1]].isEmpty():
                    return self.move_piece(move, check)
                # si elle n'est pas vide et que c'est l'emplacement finale
                else:
                    return self.take_piece(move, check)
        else:
            print("Impossible de déplacer la tour à cet endroit")
            return False

    def move_queen(self, move: Move, check: bool) -> bool:

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
                    return self.move_piece(move, check)
                # si elle n'est pas vide et que c'est l'emplacement finale
                else:
                    return self.take_piece(move, check)
            # déplacement en colonne
            elif move.end[1] != move.start[1]:
                for i in range(1, iteration_col):
                    if not self.board[move.start[0]][move.start[1] + col_sign * i].isEmpty():
                        print("Une pièce bloque le passage de la dame")
                        return False
                # si elle est vide et l'emplacement finale
                if self.board[move.end[0]][move.end[1]].isEmpty():
                    return self.move_piece(move, check)
                # si elle n'est pas vide et que c'est l'emplacement finale
                else:
                    return self.take_piece(move, check)

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
                return self.move_piece(move, check)
            # si elle n'est pas vide et que c'est l'emplacement finale
            else:
                return self.take_piece(move, check)
        else:
            print("Impossible de déplacer la dame à cet endroit")
            return False
    
    def move_king(self, move: Move, check: bool) -> bool:
        start_square = self.board[move.start[0]][move.start[1]]
        end_square = self.board[move.end[0]][move.end[1]]

        # Check who can castle
        # Castling is only possible if king has never moved.
        moves = self.move_list
        #has_white_king_already_moved = any(
        #    movehistory.piece.kind == PieceType.KING and movehistory.piece.color == Color.WHITE for movehistory in
        #    moves)
        #has_black_king_already_moved = any(
        #    movehistory.piece.kind == PieceType.KING and movehistory.piece.color == Color.BLACK for movehistory in
        #    moves)
#
        ## Castling is only possible if rook has never moved.
        #has_white_king_rook_already_moved = any(
        #    movehistory.piece.kind == PieceType.ROOK and movehistory.piece.color == Color.WHITE and movehistory.start ==
        #    [7, 7] for movehistory in moves)
        #has_white_queen_rook_already_moved = any(
        #    movehistory.piece.kind == PieceType.ROOK and movehistory.piece.color == Color.WHITE and movehistory.start ==
        #    [7, 0] for movehistory in moves)
        #has_black_king_rook_already_moved = any(
        #    movehistory.piece.kind == PieceType.ROOK and movehistory.piece.color == Color.BLACK and movehistory.start ==
        #    [0, 7] for movehistory in moves)
        #has_black_queen_rook_already_moved = any(
        #    movehistory.piece.kind == PieceType.ROOK and movehistory.piece.color == Color.BLACK and movehistory.start ==
        #    [0, 0] for movehistory in moves)

        # A king can only move one step forward, backwards, left or right
        if (move.start[0] - 1 <= move.end[0] <= move.start[0] + 1) and (
                move.start[1] - 1 <= move.end[1] <= move.start[1] + 1):
            # If square is empty
            if end_square.isEmpty():
                return self.move_piece(move, check)
            # If square is not empty
            elif end_square.isEmpty() is False:
                print("Cannot take piece of your own color.")
            else:
                return self.take_piece(move, check)

        # Elif queen's side castling
        elif move.start[0] == move.end[0] and move.start[1] - 2 == move.end[1]:
            if move.piece.color == Color.BLACK and has_black_king_already_moved is False:
                if has_black_queen_rook_already_moved is False and self.board[0][1].isEmpty() and self.board[0][
                    2].isEmpty() and self.board[0][3].isEmpty():
                    self.can_black_queen_side_castle = True
                    return self.queen_castle(move)
                else:
                    return False
            elif move.piece.color == Color.WHITE and has_white_king_already_moved is False:
                if has_white_queen_rook_already_moved is False and self.board[7][1].isEmpty() and self.board[7][
                    2].isEmpty() and self.board[7][3].isEmpty():
                    self.can_white_queen_side_castle = True
                    return self.queen_castle(move)
                else:
                    return False
        # Elif king's side castling
        elif move.start[0] == move.end[0] and move.start[1] + 2 == move.end[1]:

            if move.piece.color == Color.BLACK and has_black_king_already_moved is False:
                if has_black_king_rook_already_moved is False and self.board[0][5].isEmpty() and self.board[0][
                    6].isEmpty():
                    self.can_black_king_side_castle = True
                    return self.king_castle(move)
                else:
                    return False
            elif move.piece.color == Color.WHITE and has_white_king_already_moved is False:
                if has_white_king_rook_already_moved is False and self.board[7][5].isEmpty() and self.board[7][
                    6].isEmpty():
                    self.can_white_king_side_castle = True
                    return self.king_castle(move)
                else:
                    return False
        else:
            self.can_white_queen_side_castle = False
            self.can_white_king_side_castle = False
            self.can_black_queen_side_castle = False
            self.can_black_king_side_castle = False
            print("Cannot move king at this place.")
            return False



    def move_pawn(self, move: Move, check: bool) -> bool:
        start_square: Square = self.board[move.start[0]][move.start[1]]
        end_square: Square = self.board[move.end[0]][move.end[1]]

        if start_square.piece.color == Color.BLACK:
            if move.end[1] == move.start[1] and end_square.isEmpty():
                # Pawns can only move forward one square at a time
                if move.end[0] == move.start[0] + 1:
                    if move.end[0] == 7:
                        return self.promotion(move, check)
                    else:
                        return self.move_piece(move, check)
                # except for their very first move where they can move forward two squares.
                elif move.end[0] == move.start[0] + 2 and move.start[0] == 1:
                    self.setEnPassantTargetSquare(move.end[0] - 1, move.end[1])
                    return self.move_piece(move, check)
            # Pawns can only capture one square diagonally in front of them
            elif move.end[0] == move.start[0] + 1 and (
                    move.end[1] == move.start[1] - 1 or move.end[1] == move.start[1] + 1):
                if end_square.isEmpty() is False:
                    if move.end[0] == 7 and end_square.piece.color != start_square.piece.color:
                        return self.promotion(move, check)
                    else:
                        return self.take_piece(move, check)
                else:
                    print("cannot move pawn here.")
                    return False
        elif start_square.piece.color == Color.WHITE:
            print("pawn is white.")
            if move.end[1] == move.start[1] and end_square.isEmpty():
                print("Pawn wants to move on same column and ensquare is empty.")
                if move.end[0] == move.start[0] - 1:
                    if move.end[0] == 0:
                        return self.promotion(move, check)
                    else:
                        return self.move_piece(move, check)
                elif move.end[0] == move.start[0] - 2 and move.start[0] == 6:
                    self.setEnPassantTargetSquare(move.end[0] + 1, move.end[1])
                    return self.move_piece(move, check)
            elif move.end[0] == move.start[0] - 1 and (
                    move.end[1] == move.start[1] - 1 or move.end[1] == move.start[1] + 1):
                if end_square.isEmpty() is False:
                    if move.end[0] == 0 and end_square.piece.color != start_square.piece.color:
                        return self.promotion(move, check)
                    else:
                        return self.take_piece(move, check)
                else:
                    print("cannot move pawn here.")
                    return False
        else:
            return False

    def promotion(self, move: Move, check: bool) -> bool:
        if move.promotion_kind is None:
            return False
        if check is False:
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

    def game_to_pgn_long(self) -> str:
        moves = self.move_list
        long_pgn = ''
        i = 1
        round = 1
        for move in moves:
            move_start = IndexToColumn[move.start[1]] + IndexToLine[move.start[0]]
            move_end = IndexToColumn[move.end[1]] + IndexToLine[move.end[0]]
            piece = move.piece
            # Display piece moves per round
            if i % 2 != 0 and i > 1:
                round += 1
                long_pgn += ' ' + str(round) + '. '
            elif i == 1:
                long_pgn += '1. '
            else:
                long_pgn += ' '
            if piece.kind != PieceType.PAWN:
                long_pgn += piece.piece_to_str()
            # Display when a piece has been eaten
            if move.eat:
                long_pgn += IndexToColumn[move.start[1]] + 'x' + move_end
            else:
                long_pgn += move_start + move_end
            # Display promotion piece when pawn reaches board's end
            if move.promotion_kind is not None:
                new_piece: Piece = Piece(move.promotion_kind, piece.color)
                long_pgn += '=' + new_piece.piece_to_str()
            if move.is_castled:
                if move.castling == 'QUEEN_CASTLING':
                    long_pgn += 'O-O-O'
                else:
                    long_pgn += 'O-O'
            i += 1
        return long_pgn
    
    def game_to_pgn(self) -> str:
        moves = self.move_list
        copied_board: Board = Board()
        copied_board.init_board()
        long_pgn = ''
        i = 1
        round = 1
        for move in moves:
            move_end = IndexToColumn[move.end[1]] + IndexToLine[move.end[0]]
            piece = move.piece
            # Display piece moves per round
            if i % 2 != 0 and i > 1:
                round += 1
                long_pgn += ' ' + str(round) + '. '
            elif i == 1:
                long_pgn += '1. '
            else:
                long_pgn += ' '
            if piece.kind != PieceType.PAWN:
                long_pgn += piece.piece_to_str()

            # Loop through board to get other piece of same color
            for line in range(8):
                for col in range(8):
                    square = self.board[line][col]
                    if square.isEmpty() is False:
                        # If found same piece on board
                        if square.piece.kind == move.piece.kind and square.piece.color == move.piece.color:
                            # If this piece can go to same end square as its pair:
                            if copied_board.is_move_valid(Move([line, col], [move.end[0], move.end[1]])):
                                if line == move.end[0]:
                                    long_pgn += IndexToColumn[move.start[1]]
                                elif col == move.end[1]:
                                    long_pgn += IndexToLine[move.start[0]]

            # Display when a piece has been eaten
            if move.eat:
                long_pgn += 'x' + move_end
            else:
                long_pgn += move_end
            # Display promotion piece when pawn reaches board's end
            if move.promotion_kind is not None:
                new_piece: Piece = Piece(move.promotion_kind, piece.color)
                long_pgn += '=' + new_piece.piece_to_str()
            if move.is_castled:
                if move.castling == 'QUEEN_CASTLING':
                    long_pgn += 'O-O-O'
                else:
                    long_pgn += 'O-O'
            i += 1

            copied_board.make_move(move)

        return long_pgn