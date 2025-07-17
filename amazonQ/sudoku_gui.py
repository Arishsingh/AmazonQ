import tkinter as tk
from tkinter import messagebox, font

class SudokuGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Game")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f0f0")
        
        self.selected_cell = None
        
        # Sample Sudoku puzzle with 0 as empty cells
        self.puzzle = [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9],
        ]
        
        # To store references to the Entry widgets
        self.cells = [[None for _ in range(9)] for _ in range(9)]
        
        self.create_widgets()
        self.draw_grid()
        self.load_puzzle()
        
    def create_widgets(self):
        # Frame for sudoku grid
        self.grid_frame = tk.Frame(self.root, bg="#f0f0f0", padx=10, pady=10)
        self.grid_frame.pack()

        # Status label
        self.status_label = tk.Label(self.root, text="Fill the board and click 'Check Solution'", 
                                     bg="#f0f0f0", font=("Arial", 12))
        self.status_label.pack(pady=5)
        
        # Control buttons frame
        controls = tk.Frame(self.root, bg="#f0f0f0")
        controls.pack(pady=10)
        
        # Check button
        self.check_button = tk.Button(controls, text="Check Solution", command=self.check_solution,
                                      bg="#4CAF50", fg="white", width=15, activebackground="#45a049")
        self.check_button.grid(row=0, column=0, padx=5)
        
        # Reset button
        self.reset_button = tk.Button(controls, text="Reset Puzzle", command=self.reset_puzzle,
                                      bg="#f44336", fg="white", width=15, activebackground="#d32f2f")
        self.reset_button.grid(row=0, column=1, padx=5)

    def draw_grid(self):
        # Use a bigger font for clarity
        self.font_style = font.Font(family="Arial", size=16, weight="bold")

        for i in range(9):
            for j in range(9):
                # Create Entry widget for each cell
                e = tk.Entry(self.grid_frame, width=2, font=self.font_style,
                             justify="center", borderwidth=2, relief="ridge")
                
                # Position in grid
                e.grid(row=i, column=j, padx=1, pady=1)
                
                # Thicker borders for blocks (3x3)
                if j in [2, 5]:
                    e.grid_configure(padx=(1, 5))
                if i in [2, 5]:
                    e.grid_configure(pady=(1, 5))
                
                # Bind key press for validation
                e.bind("<KeyRelease>", self.validate_input)
                
                self.cells[i][j] = e

    def load_puzzle(self):
        for i in range(9):
            for j in range(9):
                val = self.puzzle[i][j]
                cell = self.cells[i][j]
                if val != 0:
                    cell.insert(0, str(val))
                    cell.config(state="readonly", readonlybackground="#d3d3d3")
                else:
                    cell.delete(0, tk.END)
                    cell.config(state="normal", bg="white")

    def reset_puzzle(self):
        self.status_label.config(text="Puzzle reset. Fill the board and click 'Check Solution'.")
        self.load_puzzle()

    def validate_input(self, event):
        entry = event.widget
        val = entry.get()
        if val == "":
            return
        if len(val) > 1 or val not in "123456789":
            # Remove invalid input
            entry.delete(0, tk.END)
        else:
            # Valid input, keep only one digit 1-9
            entry.delete(1, tk.END)

    def get_board(self):
        board = []
        for i in range(9):
            row = []
            for j in range(9):
                val = self.cells[i][j].get()
                if val == "":
                    row.append(0)
                else:
                    try:
                        row.append(int(val))
                    except ValueError:
                        row.append(0)
            board.append(row)
        return board

    def check_solution(self):
        board = self.get_board()
        
        if not self.is_complete(board):
            self.status_label.config(text="The board is not completely filled.")
            return
        
        if self.is_valid_solution(board):
            self.status_label.config(text="Congratulations! You solved the Sudoku.")
            messagebox.showinfo("Success", "Congratulations! You solved the Sudoku!")
        else:
            self.status_label.config(text="There are errors in the solution. Try again.")
            messagebox.showwarning("Error", "There are errors in the solution. Please check your inputs.")

    def is_complete(self, board):
        for row in board:
            if 0 in row:
                return False
        return True

    def is_valid_solution(self, board):
        # Check rows
        for i in range(9):
            if not self.is_valid_group(board[i]):
                return False
        # Check columns
        for j in range(9):
            col = [board[i][j] for i in range(9)]
            if not self.is_valid_group(col):
                return False
        # Check 3x3 blocks
        for box_row in range(3):
            for box_col in range(3):
                block = []
                for i in range(3):
                    for j in range(3):
                        block.append(board[box_row*3 + i][box_col*3 + j])
                if not self.is_valid_group(block):
                    return False
        return True

    def is_valid_group(self, group):
        nums = [n for n in group if n != 0]
        return len(nums) == len(set(nums))  # no duplicates

if __name__ == "__main__":
    root = tk.Tk()
    game = SudokuGame(root)
    root.mainloop()
