import sys #For parameters
import os #For file checking

# For visualiztion purposes
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Class representing a cell in Game of Life, can be alive or dead, has cooordinates
class Cell:
    def __init__(self, coord_x : int, coord_y : int):
        self.x : int = coord_x
        self.y : int = coord_y
        self.state : bool = False
        self.neighbors : int = 0
    def change_state(self):
        self.state = not self.state
    def __repr__(self) -> str:
        value : str = "X" if self.state else "O"
        return f"{value}"

# A 2D array of Cells
class Universe:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.cells = [[Cell(i, j) for i in range(width)] for j in range(height)]
    def __repr__(self) -> str:
        string = ""
        for row in self.cells:
            for cell in row:
                string = string + str(cell)
            string = string + "\n"
        return string
    def change_cell(self, cell : tuple[int, int]): # Toggles state of a specific cell
        self.cells[cell[1]][cell[0]].change_state()
    def update_universe(self) -> None: # Applies rules of Conway's game of life to the universe
        #TODO change to store number of neighbors, and then change state
        # By changing state before we screw up the rules
        for row in self.cells:
            for cell in row:
                neighbors = 0
                # 8 neighbors
                # A neighbor is counted as an active cell
                if cell.x > 0: #Don't check left if first element
                    if self.cells[cell.y][cell.x - 1].state: neighbors = neighbors + 1
                    if cell.y > 0: #Don't check up if first element
                        if self.cells[cell.y - 1][cell.x - 1].state: neighbors = neighbors + 1
                    if cell.y + 1 < self.height: #Don't check down if last element
                        if self.cells[cell.y + 1][cell.x - 1].state: neighbors = neighbors + 1
                if cell.y > 0: #Don't check up if first element
                    if self.cells[cell.y - 1][cell.x].state: neighbors = neighbors + 1
                if cell.y + 1 < self.height: #Don't check down if last element
                    if self.cells[cell.y + 1][cell.x].state: neighbors = neighbors + 1
                if cell.x + 1 < self.width: #Don't check right if last element
                    if self.cells[cell.y][cell.x + 1].state: neighbors = neighbors + 1
                    if cell.y > 0: #Don't check up if first element
                        if self.cells[cell.y - 1][cell.x + 1].state: neighbors = neighbors + 1
                    if cell.y + 1 < self.height: #Don't check down if last element
                        if self.cells[cell.y + 1][cell.x + 1].state: neighbors = neighbors + 1
                cell.neighbors = neighbors
        # Two for loops, one to check neighbors, one to change states
        for row in self.cells:
            for cell in row:
                if cell.state:
                    if cell.neighbors <= 1:
                        cell.change_state()
                    elif cell.neighbors >= 4:
                        cell.change_state()
                else:
                    if cell.neighbors == 3:
                        cell.change_state()
                

# Creates a Universe, and activates 0 or more cells
def create_universe(width: int, height: int, active_cells : list[tuple[int, int]]) -> Universe:
    universe = Universe(width, height)
    for cell in active_cells:
        universe.change_cell(cell)
    return universe

fig = Figure(figsize=(4,4))
ax = fig.add_subplot(111)
def plot_universe(universe, grid : bool = True) -> None:
    ax.cla()
    # Create a new figure and axes

    # Convert the universe's cell states to a numpy array for efficient plotting
    cell_states = np.array([[cell.state for cell in row] for row in universe.cells])

    # Create the plot using Matplotlib's imshow function
    ax.imshow(cell_states, cmap="binary", aspect="equal")  # "binary" colors cells as "X" (black) and "O" (white)

    # Show grid
    if grid:
        num_rows, num_cols = cell_states.shape
        for x in np.arange(-0.5, num_cols + 0.5):  # Include left and right edges for visual clarity
            ax.axvline(x, color='lightgray', linestyle='--', linewidth=0.8)
        for y in np.arange(-0.5, num_rows + 0.5):  # Include top and bottom edges
            ax.axhline(y, color='lightgray', linestyle='--', linewidth=0.8)

    # Set title and show the plot
    ax.set_title("Game of Life")

universe = None
generation = 1
_generations = 0

# This program needs a file as parameter, only the file name is needed, not the folder
if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Pass a file as an argument")
        exit()
    arguments = sys.argv[1:]
    
    first_param = arguments[0]
    
    if type(first_param) == str:
        print(first_param)
        file_path = os.path.join(os.getcwd(),"Inputs",first_param)
        print(file_path)
        if os.path.exists(file_path):
            print("file found")
            file = open(file_path)
            lines = file.readlines()
            if len(lines) < 2:
                print("File format error")
                exit()
            #TODO check the file format, make sure first line are two ints, int, and then a variable number of two ints
            _width, _height = map(int, lines[0].split())
            _generations = int(lines[1])
            _active_cells = []
            _active_cells.extend(tuple(list(int(x) for x in line.split())) for line in lines[2:])
            universe = create_universe(_width, _height, _active_cells)
        else:
            print(".in file not found. Please check file name.")
            exit()

window = tk.Tk()
text = tk.Text(window)
text.insert("1.0", f"Generation {generation} of {_generations}")
plot_universe(universe)
canvas = FigureCanvasTkAgg(fig, window)

# TKinter button function
def next_generation_button_click():
    # GOL variables
    global universe
    global generation
    global _generations
    
    # TK widgets
    global text
    global canvas
    
    universe.update_universe()
    plot_universe(universe)
    canvas.draw()
    generation = generation + 1
    text.delete("1.0", "2.0")
    text.insert("1.0", f"Generation {generation} of {_generations}")


button = tk.Button(window, text=f"Next Generation", command=next_generation_button_click)
text.config(height=1)
text.pack()
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
button.pack()

window.mainloop()