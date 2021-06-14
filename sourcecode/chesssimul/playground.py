from board import *

board: Board = Board()
board.init_board()
print(board.to_unicode())
board.move('e2e4')

# fou
# move = Move([7,2], [7,1])

# cavalier
move = Move([7, 6], [5, 6])

print(board.make_move(move))

board.setEnPassantTargetSquare()
print(board.to_unicode())
print(board.to_fen())
print(board.board[0][0].piece.kind)
print(board.board[0][0].piece.color)
print(board.board[4][4].piece.kind)
print(board.board[4][4].piece.color)
