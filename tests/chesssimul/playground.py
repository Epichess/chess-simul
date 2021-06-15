from sourcecode.chesssimul.board import *

board = Board()
board.init_board()

print(board.board[7][6].piece)
board.make_move(Move((7, 6), (5, 5)))

print(board)

board.make_move(Move((0, 6), (2, 7)))

print(board)

board.make_move(Move((5, 5), (6, 7)))

print(board)

board.make_move(Move((5, 5), (4, 7)))

print(board)

board.make_move(Move((2, 7), (3, 5)))

print(board)

board.make_move(Move((4, 7), (3, 5)))

print(board)
