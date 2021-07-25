from board import Board
from move import Move
from piece import *

board = Board()

board.init_board()

print(board)

#blanc
print(board.make_move(Move((6, 0), (5, 0))))
print(board.make_move(Move((1, 0), (3, 0))))

#blanc
print(board.make_move(Move((5, 0), (4, 0))))
print(board.make_move(Move((0, 1), (2, 0))))

#blanc
print(board.make_move(Move((6, 7), (4, 7))))
print(board.make_move(Move((2, 0), (3, 2))))

#blanc
print(board.make_move(Move((7, 7), (5, 7))))
print(board.make_move(Move((3, 2), (4, 0))))

#blanc
print(board.make_move(Move((6, 2), (5, 2))))
print(board.make_move(Move((4, 0), (5, 2))))

#blanc
print(board.make_move(Move((7, 0), (5, 0))))

board.board[5][2].piece = None
board.board[5][3].piece = str_to_piece['n']
board.board[6][3].piece = None

print(board.make_move(Move((1, 7), (2, 7))))

#blanc
# déplacement de la tour pour prendre le cavalier qui met en échec le roi blanc
#print(board.make_move(Move((5, 7), (5, 3))))
print(board.make_move(Move((7, 4), (6, 3))))
print(board.to_unicode())

board.board[4][3].piece = str_to_piece['b']
board.board[4][3].piece.color = Color.BLACK

print(board.to_unicode())
print(board.make_move(Move((4, 3), (5, 2))))
print(board.to_unicode())

#print(board.make_move(Move((6, 3), (6, 2))))
print(board.make_move(Move((6, 3), (5, 3))))
print(board.to_unicode())