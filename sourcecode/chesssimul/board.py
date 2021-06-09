#from sourcecode.chesssimul.piece import Piece
from piece import *
from square import Square
from piece import Color
from coup import Move

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


    def make_move(self, move: Move):
        print('make move')
        #postion de la pièce avant son déplacement dans l'échiquier
        start_square: Square = self.board[move.start[0]][move.start[1]]
        #Y a t'il une pièce à déplacer
        if not (start_square.isEmpty()):
            #type de la pièce que nous voulons déplacer
            type_piece_start: PieceType = start_square.piece.kind
            print(type_piece_start)
            # Si c'est le cavalier
            if (type_piece_start == PieceType.KNIGHT):
                print("vérification du coup du cavalier")
                self.move_knight(move)
            if (type_piece_start == PieceType.BISHOP):
                print("vérification du coup du fou")
                self.move_bishop(move)



    def move_knight(self, move: Move):
        #postion de la pièce avant son déplacement dans l'échiquier
        start_square: Square = self.board[move.start[0]][move.start[1]]
        #postion de la pièce après son déplacement dans l'échiquier
        end_square: Square = self.board[move.end[0]][move.end[1]]
        if (move.end[0] == move.start[0] + 2 or move.end[0] == move.start[0] - 2):
            if (move.end[1] == move.start[1] + 1 or move.end[1] == move.start[1] - 1):
                if end_square.isEmpty:
                    self.board[move.end[0]][move.end[1]].piece = start_square.piece
                    self.board[move.start[0]][move.start[1]].piece = None
                    print("cavalier déplacé")
                elif not (end_square.isEmpty):
                    if (end_square.piece.color != start_square.piece.color):
                        self.board[move.end[0]][move.end[1]].piece = start_square.piece
                        self.board[move.start[0]][move.start[1]].piece = None
                        print("cavalier déplacé et prise pièce")
                    else:
                        print("impossible de prendre sa propre pièce")

        elif (move.end[1] == move.start[1] + 2 or move.end[1] == move.start[1] - 2):
            if (move.end[0] == move.start[0] + 1 or move.end[0] == move.start[0] - 1):
                if not (end_square.isEmpty):
                    if end_square.isEmpty:
                        self.board[move.end[0]][move.end[1]].piece = start_square.piece
                        self.board[move.start[0]][move.start[1]].piece = None
                        print("cavalier déplacé")
                elif not (end_square.isEmpty):
                    if (end_square.piece.color != start_square.piece.color):
                        self.board[move.end[0]][move.end[1]].piece = start_square.piece
                        self.board[move.start[0]][move.start[1]].piece = None
                        print("cavalier déplacé et prise pièce")
                    else:
                        print("impossible de prendre sa propre pièce")
        else:
            print("Impossible de déplacer le cavalier à cet endroit")


    def move_bishop(self, move: Move):
        
        self.board[6][1].piece = None
        print(range(move.start[0], move.end[0]))
        #postion de la pièce avant son déplacement dans l'échiquier
        start_square: Square = self.board[move.start[0]][move.start[1]]
        #postion de la pièce après son déplacement dans l'échiquier
        end_square: Square = self.board[move.end[0]][move.end[1]]
        #Pion sur le chemin du fou
        for line in range(move.end[0]):
            print("line")
            print(line)
            #if (move.start[0] == line):
                
                
            for col in move.start[1:move.end[1]]:
                print(col)
                if not (self.board[line][col].isEmpty):
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
                       
board: Board = Board()
board.init_board()
print(board.to_unicode())
move = Move([7,2], [6,1])
board.make_move(move)
print(board.to_unicode())
#print(board.board[0][0].piece.kind)
#print(board.board[0][0].piece.color)
#print(board.board[5][5].piece.kind)
#print(board.board[5][5].piece.color)
#print(board.board[4][4].piece.kind)
#print(board.board[4][4].piece.color)