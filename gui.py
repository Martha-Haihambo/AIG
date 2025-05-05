import tkinter as tk
from tkinter import messagebox
from tictactoe import *

class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.board = initial_state()
        self.create_buttons()

        self.restart_button = tk.Button(self.root, text="Restart", font=("Arial", 16), command=self.restart)
        self.restart_button.grid(row=3, column=0, columnspan=3)

    def create_buttons(self):
        for i in range(3):
            for j in range(3):
                btn = tk.Button(self.root, text="", font=("Arial", 32), width=5, height=2,
                                command=lambda row=i, col=j: self.make_move(row, col))
                btn.grid(row=i, column=j)
                self.buttons[i][j] = btn

    def make_move(self, i, j):
        if terminal(self.board) or self.board[i][j] is not EMPTY:
            return

        self.board[i][j] = O
        self.update_gui()

        if terminal(self.board):
            self.show_result()
            return

        ai_move = minimax(self.board)
        if ai_move:
            x, y = ai_move
            self.board[x][y] = X
            self.update_gui()

        if terminal(self.board):
            self.show_result()

    def update_gui(self):
        for i in range(3):
            for j in range(3):
                mark = self.board[i][j]
                self.buttons[i][j].config(text=mark if mark else "")

    def show_result(self):
        win = winner(self.board)
        if win:
            messagebox.showinfo("Game Over", f"{win} wins!")
        else:
            messagebox.showinfo("Game Over", "It's a tie!")

    def restart(self):
        self.board = initial_state()
        self.update_gui()

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToeGUI(root)
    root.mainloop()
