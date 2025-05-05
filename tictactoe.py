import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)
    return X if x_count == o_count else O


def actions(board):
    return {(i, j) for i in range(3) for j in range(3) if board[i][j] == EMPTY}


def result(board, action):
    if action not in actions(board):
        raise Exception("Invalid move")

    new_board = copy.deepcopy(board)
    i, j = action
    new_board[i][j] = player(board)
    return new_board


def winner(board):
    lines = (
        board[0], board[1], board[2], 
        [board[i][0] for i in range(3)], 
        [board[i][1] for i in range(3)],  
        [board[i][2] for i in range(3)],  
        [board[i][i] for i in range(3)],  
        [board[i][2 - i] for i in range(3)]  
    )
    for line in lines:
        if line.count(X) == 3:
            return X
        elif line.count(O) == 3:
            return O
    return None


def terminal(board):
    return winner(board) is not None or all(cell != EMPTY for row in board for cell in row)


def utility(board):
    win = winner(board)
    if win == X:
        return 1
    elif win == O:
        return -1
    else:
        return 0


def minimax(board):
    if terminal(board):
        return None

    turn = player(board)

    def max_value(state):
        if terminal(state):
            return utility(state), None
        v, move = float('-inf'), None
        for action in actions(state):
            min_result, _ = min_value(result(state, action))
            if min_result > v:
                v, move = min_result, action
                if v == 1:
                    break
        return v, move

    def min_value(state):
        if terminal(state):
            return utility(state), None
        v, move = float('inf'), None
        for action in actions(state):
            max_result, _ = max_value(result(state, action))
            if max_result < v:
                v, move = max_result, action
                if v == -1:
                    break
        return v, move

    if turn == X:
        return max_value(board)[1]  
    else:
        return min_value(board)[1]  
