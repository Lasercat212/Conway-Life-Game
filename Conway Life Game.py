import tkinter as tk
import winsound

class GameOfLife:
    def __init__(self, root, grid_size=28):
        self.root = root
        self.grid_size = grid_size
        self.delay = 600  # milliseconds
        self.grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.buttons = [[None for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.create_grid()
        self.running = True
        self.root.after(self.delay, self.update_grid)
        self.dead_count = 0
        self.born_count = 0
        self.dead_label = tk.Label(self.root, text=f"Dead: {self.dead_count}")
        self.dead_label.grid(row=0, column=self.grid_size, sticky="e")
        self.born_label = tk.Label(self.root, text=f"Born: {self.born_count}")
        self.born_label.grid(row=1, column=self.grid_size, sticky="e")
        self.pause_button = tk.Button(self.root, text="Pause", command=self.pause)
        self.pause_button.grid(row=2, column=self.grid_size, sticky="e")
        self.resume_button = tk.Button(self.root, text="Resume", command=self.resume)
        self.resume_button.grid(row=3, column=self.grid_size, sticky="e")
        self.reset_button = tk.Button(self.root, text="Reset Counters", command=self.reset_counters)
        self.reset_button.grid(row=4, column=self.grid_size, sticky="e")
        self.clear_button = tk.Button(self.root, text="Clear Grid", command=self.clear_grid)
        self.clear_button.grid(row=5, column=self.grid_size, sticky="e")

    def create_grid(self):
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                button = tk.Button(self.root, width=2, height=1, command=lambda r=row, c=col: self.toggle_cell(r, c))
                button.grid(row=row, column=col)
                self.buttons[row][col] = button

    def toggle_cell(self, row, col):
        self.grid[row][col] = 1 - self.grid[row][col]
        self.update_button_color(row, col)

    def update_button_color(self, row, col):
        color = "black" if self.grid[row][col] == 1 else "white"
        self.buttons[row][col].configure(bg=color)

    def count_live_neighbors(self, row, col):
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        count = 0
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < self.grid_size and 0 <= c < self.grid_size:
                count += self.grid[r][c]
        return count

    def update_grid(self):
        if not self.running:
            return
        new_grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        dead_count = 0
        born_count = 0
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                live_neighbors = self.count_live_neighbors(row, col)
                if self.grid[row][col] == 1:
                    if live_neighbors in [2, 3]:
                        new_grid[row][col] = 1
                    else:
                        new_grid[row][col] = 0
                        dead_count += 1
                        winsound.Beep(600, 10)  # 600Hz for 100ms
                else:
                    if live_neighbors == 3:
                        new_grid[row][col] = 1
                        born_count += 1
                        winsound.Beep(800, 10)  # 800Hz for 100ms
        self.grid = new_grid
        self.dead_count += dead_count
        self.born_count += born_count
        self.dead_label.config(text=f"Dead: {self.dead_count}")
        self.born_label.config(text=f"Born: {self.born_count}")
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                self.update_button_color(row, col)
        self.root.after(self.delay, self.update_grid)

    def clear_grid(self):
        self.grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                self.update_button_color(row, col)

    def pause(self):
        self.running = False

    def resume(self):
        self.running = True
        self.update_grid()

    def reset_counters(self):
        self.dead_count = 0
        self.born_count = 0
        self.dead_label.config(text=f"Dead: {self.dead_count}")
        self.born_label.config(text=f"Born: {self.born_count}")

if __name__ == "__main__":
    root = tk.Tk()
    game = GameOfLife(root)
    root.mainloop()