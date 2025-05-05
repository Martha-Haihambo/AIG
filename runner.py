from tictactoe import *

def print_board(board):
    for row in board:
        print([" " if cell is None else cell for cell in row])
    print()

def play_game():
    board = initial_state()
    print("Initial board:")
    print_board(board)

    while not terminal(board):
        move = minimax(board)
        if move:
            print(f"Player {player(board)} chooses {move}")
            board = result(board, move)
            print_board(board)
        else:
            break

    print("Game over.")
    win = winner(board)
    if win:
        print(f"{win} wins!")
    else:
        print("It's a tie!")

if __name__ == "__main__":
    play_game()
