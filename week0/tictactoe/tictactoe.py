"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """

    count_x = 0
    count_o = 0

    for row in board:
        for val in row:
            if val == X:
                count_x += 1
            elif val == O:
                count_o += 1

    # since X goes first, it's only O's turn if there's more of X on the board
    if count_x > count_o:
        return O

    return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.

    """

    actions = set()

    # iterate through every value and count up the empty spaces
    for row in range(3):
        for col in range(3):
            val = board[row][col]
            if val == EMPTY:
                actions.add(tuple([row, col]))

    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    copy_board = copy.deepcopy(board)

    try:
        player_turn = player(board)
        if copy_board[action[0]][action[1]] == EMPTY:
            copy_board[action[0]][action[1]] = player_turn
        else:
            raise Exception("Invalid board action")
    except:
        raise Exception("Invalid board action")

    return copy_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    # mini function to make code less scary looking
    def check_for_var(row, col, var):
        if board[row][col] == var:
            return True
        return False

    # there must be a better way, but I'm choosing to pick my battles considering this is a 3x3 game board
    for var in [X, O]:
        # check top left, then surrounding
        if check_for_var(0, 0, var):
            if check_for_var(0, 1, var) and check_for_var(0, 2, var):
                return var
            if check_for_var(1, 0, var) and check_for_var(2, 0, var):
                return var
            if check_for_var(1, 1, var) and check_for_var(2, 2, var):
                return var
        # check bottom left, then surrounding
        elif check_for_var(2, 0, var):
            if check_for_var(1, 1, var) and check_for_var(0, 2, var):
                return var
            if check_for_var(2, 1, var) and check_for_var(2, 2, var):
                return var
        # check far right col
        elif check_for_var(2, 2, var):
            if check_for_var(1, 2, var) and check_for_var(0, 2, var):
                return var

    return None



def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    if winner(board) != EMPTY:
        return True
    else:
        for row in board:
            if EMPTY in row:
                return False
        return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    win = winner(board)

    if win == "X":
        return 1
    elif win == "O":
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board. None if board is terminal
    """

    # check if the game is over
    if terminal(board):
        return None

    # get the current player
    curr_player = player(board)

    if curr_player == "X":  # maximizing player
        best_score = -2
        best_action = None
        for action in actions(board):
            new_board = result(board, action)
            score = min_value(new_board)
            if score > best_score:
                best_score = score
                best_action = action
        return best_action

    elif curr_player == "O":  # minimizing player
        best_score = 2
        best_action = None
        for action in actions(board):
            new_board = result(board, action)
            score = max_value(new_board)
            if score < best_score:
                best_score = score
                best_action = action
        return best_action


def max_value(board):
    if terminal(board):
        return utility(board)

    v = -2
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v


def min_value(board):
    if terminal(board):
        return utility(board)

    v = 2
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v
