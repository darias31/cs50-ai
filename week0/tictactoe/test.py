from tictactoe import winner, terminal, utility, player, actions, result, minimax

EMPTY = None

boards = [
    [["X",  "O",  "X"], 
     ["X",  "X",  "O"], 
     ["X",  "O",  "O"]],
     [["X",  "O",  "X"], 
     ["O",  "X",  "X"], 
     ["O",  "O",  "O"]],
     [[EMPTY,  "O",  "X"], 
     [EMPTY,  "X",  "O"], 
     ["X",  "O",  EMPTY]],
]


for board in boards:
    print(terminal(board))
