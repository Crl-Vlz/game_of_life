import sys #For parameters
import os #For file checking
import time # for sleep when you run all generations
import threading # for stopping the all generatios running
import datetime #to print the date of the running at the output

# For visualiztion purposes
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends._backend_tk import NavigationToolbar2Tk as Navbar

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

 #Figures
block=np.array([[False,False,False,False],#4x4
                [False,True,True,False],
                [False,True,True,False],
                [False,False,False,False]])
beehive=np.array([[False,False,False,False,False,False],#6x5
                [False,False,True,True,False,False],
                [False,True,False,False,True,False],
                [False,False,True,True,False,False],
                [False,False,False,False,False,False]])
loaf=np.array([[False,False,False,False,False,False],#6x6
                [False,False,True,True,False,False],
                [False,True,False,False,True,False],
                [False,False,True,False,True,False],
                [False,False,False,True,False,False],
                [False,False,False,False,False,False]])
boat=np.array([[False,False,False,False,False],#5x5
                [False,True,True,False,False],
                [False,True,False,True,False],
                [False,False,True,False,False],
                [False,False,False,False,False]])
tub=np.array([[False,False,False,False,False],#5x5
                [False,False,True,False,False],
                [False,True,False,True,False],
                [False,False,True,False,False],
                [False,False,False,False,False]])
blinker=[np.array([[False,False,False],#3x5and5x3
                    [False,True,False],
                    [False,True,False],
                    [False,True,False],
                    [False,False,False]]),
        np.array([[False,False,False,False,False],
                    [False,True,True,True,False],
                    [False,False,False,False,False]])]
toad=[np.array([[False,False,False,False,False,False],#6x6and6x4
                [False,False,False,True,False,False],
                [False,True,False,False,True,False],
                [False,True,False,False,True,False],
                [False,False,True,False,False,False],
                [False,False,False,False,False,False]]),
        np.array([[False,False,False,False,False,False],
                [False,False,True,True,True,False],
                [False,True,True,True,False,False],
                [False,False,False,False,False,False]])]
beacon=[np.array([[False,False,False,False,False,False],#6x6and6x6
                [False,True,True,False,False,False],
                [False,True,True,False,False,False],
                [False,False,False,True,True,False],
                [False,False,False,True,True,False],
                [False,False,False,False,False,False]]),
        np.array([[False,False,False,False,False,False],
                [False,True,True,False,False,False],
                [False,True,False,False,False,False],
                [False,False,False,False,True,False],
                [False,False,False,True,True,False],
                [False,False,False,False,False,False]])]
glider=[np.array([[False,False,False,False,False],#5x5,5x5,5x5and5x5
                [False,False,True,False,False],
                [False,False,False,True,False],
                [False,True,True,True,False],
                [False,False,False,False,False]]),
        np.array([[False,False,False,False,False],
                [False,True,False,True,False],
                [False,False,True,True,False],
                [False,False,True,False,False],
                [False,False,False,False,False]]),
        np.array([[False,False,False,False,False],
                [False,False,False,True,False],
                [False,True,False,True,False],
                [False,False,True,True,False],
                [False,False,False,False,False]]),
        np.array([[False,False,False,False,False],
                [False,True,False,False,False],
                [False,False,True,True,False],
                [False,True,True,False,False],
                [False,False,False,False,False]])]
spaceship=[np.array([[False,False,False,False,False,False,False],#7x6,7x6,7x6and7x6
                [False,True,False,False,True,False,False],
                [False,False,False,False,False,True,False],
                [False,True,False,False,False,True,False],
                [False,False,True,True,True,True,False],
                [False,False,False,False,False,False,False]]),
        np.array([[False,False,False,False,False,False,False],
                [False,False,False,True,True,False,False],
                [False,True,True,False,True,True,False],
                [False,True,True,True,True,False,False],
                [False,False,True,True,False,False,False],
                [False,False,False,False,False,False,False]]),
        np.array([[False,False,False,False,False,False,False],
                [False,False,True,True,True,True,False],
                [False,True,False,False,False,True,False],
                [False,False,False,False,False,True,False],
                [False,True,False,False,True,False,False],
                [False,False,False,False,False,False,False]]),
        np.array([[False,False,False,False,False,False,False],
                [False,False,True,True,False,False,False],
                [False,True,True,True,True,False,False],
                [False,True,True,False,True,True,False],
                [False,False,False,True,True,False,False],
                [False,False,False,False,False,False,False]])]

def countPatterns(universe, limits) -> dict:
    # limits are the exact coordinate, so here we add one cell more to each side, to match with the figures pattern
    min_x, max_x, min_y, max_y = limits[0]-1, limits[1]+1, limits[2]-1, limits[3]+1
    patternCounter = {'Block': 0,'Beehive': 0,'Loaf': 0,'Boat': 0,'Tub': 0,'Blinker': 0,'Toad': 0,
                      'Beacon': 0,'Glider': 0,'Lg Spship': 0, 'Total': 0}

    for i in range(min_x, max_x):
        for j in range(min_y, max_y):
            if i+4 <= max_x+2 and j+4 <= max_y+2 and (universe[i:i+4, j:j+4] == block).all(): 
                patternCounter["Block"] += 1
                patternCounter["Total"] += 1
            elif i+5 <= max_x+2 and j+6 <= max_y+2 and (universe[i:i+5, j:j+6] == beehive).all():
                patternCounter["Beehive"] += 1
                patternCounter["Total"] += 1
            elif i+6 <= max_x+2 and j+6 <= max_y+2 and (universe[i:i+6, j:j+6] == loaf).all():
                patternCounter["Loaf"] += 1
                patternCounter["Total"] += 1
            elif i+5 <= max_x+2 and j+5 <= max_y+2 and (universe[i:i+5, j:j+5] == boat).all():
                patternCounter["Boat"] += 1
                patternCounter["Total"] += 1
            elif i+5 <= max_x+2 and j+5 <= max_y+2 and (universe[i:i+5, j:j+5] == tub).all():
                patternCounter["Tub"] += 1
                patternCounter["Total"] += 1
            elif i+5 <= max_x+2 and j+3 <= max_y+2 and (universe[i:i+5,j:j+3] == blinker[0]).all():
                patternCounter["Blinker"] += 1
                patternCounter["Total"] += 1
            elif i+3 <= max_x+2 and j+5 <= max_y+2 and (universe[i:i+3, j:j+5] == blinker[1]).all():
                patternCounter["Blinker"] += 1
                patternCounter["Total"] += 1
            elif i+6 <= max_x+2 and j+6 <= max_y+2 and (universe[i:i+6, j:j+6] == toad[0]).all():
                patternCounter["Toad"] += 1
                patternCounter["Total"] += 1
            elif i+4 <= max_x+2 and j+6 <= max_y+2 and (universe[i:i+4, j:j+6] == toad[1]).all():
                patternCounter["Toad"] += 1
                patternCounter["Total"] += 1
            elif i+6 <= max_x+2 and j+6 <= max_y+2 and (universe[i:i+6, j:j+6] == beacon[0]).all():
                patternCounter["Beacon"] += 1
                patternCounter["Total"] += 1
            elif i+6 <= max_x+2 and j+6 <= max_y+2 and (universe[i:i+6, j:j+6] == beacon[1]).all():
                patternCounter["Beacon"] += 1
                patternCounter["Total"] += 1
            elif i+5 <= max_x+2 and j+5 <= max_y+2 and (universe[i:i+5, j:j+5] == glider[0]).all():
                patternCounter["Glider"] += 1
                patternCounter["Total"] += 1
            elif i+5 <= max_x+2 and j+5 <= max_y+2 and (universe[i:i+5, j:j+5] == glider[1]).all():
                patternCounter["Glider"] += 1
                patternCounter["Total"] += 1
            elif i+5 <= max_x+2 and j+5 <= max_y+2 and (universe[i:i+5, j:j+5] == glider[2]).all():
                patternCounter["Glider"] += 1
                patternCounter["Total"] += 1
            elif i+5 <= max_x+2 and j+5 <= max_y+2 and (universe[i:i+5, j:j+5] == glider[3]).all():
                patternCounter["Glider"] += 1
                patternCounter["Total"] += 1
            elif i+6 <= max_x+2 and j+7 <= max_y+2 and (universe[i:i+6, j:j+7] == spaceship[0]).all():
                patternCounter["Lg Spship"] += 1
                patternCounter["Total"] += 1
            elif i+6 <= max_x+2 and j+7 <= max_y+2 and (universe[i:i+6, j:j+7] == spaceship[1]).all():
                patternCounter["Lg Spship"] += 1
                patternCounter["Total"] += 1
            elif i+6 <= max_x+2 and j+7 <= max_y+2 and (universe[i:i+6, j:j+7] == spaceship[2]).all():
                patternCounter["Lg Spship"] += 1
                patternCounter["Total"] += 1
            elif i+6 <= max_x+2 and j+7 <= max_y+2 and (universe[i:i+6, j:j+7] == spaceship[3]).all():
                patternCounter["Lg Spship"] += 1
                patternCounter["Total"] += 1
    return patternCounter

# Creates a Universe, and activates 0 or more cells
def create_universe(width: int, height: int, active_cells : list[tuple[int, int]]) -> Universe:
    # one row above and one below, same with columns, to add a padding and keep safe the area to check patterns
    universe = Universe(width+2, height+2) 
    for cell in active_cells:
        universe.change_cell(cell)
    return universe

fig = Figure(figsize=(8,6))
ax = fig.add_subplot(111)

def center_view(universe) -> tuple:
    x_coords = []
    y_coords = []
    for row in universe.cells:
        for cell in row:
            if cell.state:
                x_coords.append(cell.x)
                y_coords.append(cell.y)

    if len(x_coords) > 0 and len(y_coords) > 0:
        return (min(x_coords), max(x_coords), min(y_coords), max(y_coords))
    
    return (0,0,0,0)

def generate_output(patterns) -> None:
    mode = 'a'
    first_lines = ''
    percentilePatterns = dict()
    if generation == 1:
        mode = 'w'
        first_lines = f"Simulation at { datetime.datetime.now().date()}\nUniverse Size: {universe.width} x {universe.height}\n\n"
    total = patterns['Total']
    for key in patterns:
        percentilePatterns[key] = round((patterns[key]/total)*100)
        patterns[key] = f" {str(patterns[key])}"
        patterns[key] += ' ' * (7 - len(patterns[key]))
        percentilePatterns[key] = f" {str(percentilePatterns[key])}"
        percentilePatterns[key] += ' ' * (9 - len(percentilePatterns[key]))
    

    with open("output.txt", mode, encoding="utf-8") as output:
        output.write(f"{first_lines}Iteration: {generation}\n")
        output.write("−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−\n")
        output.write("|            | Count | Percent |\n")
        output.write("−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−\n")
        output.write(f"|Block       |{patterns['Block']}|{percentilePatterns['Block']}|\n")
        output.write(f"|Beehive     |{patterns['Beehive']}|{percentilePatterns['Beehive']}|\n")
        output.write(f"|Loaf        |{patterns['Loaf']}|{percentilePatterns['Loaf']}|\n")
        output.write(f"|Boat        |{patterns['Boat']}|{percentilePatterns['Boat']}|\n")
        output.write(f"|Tub         |{patterns['Tub']}|{percentilePatterns['Tub']}|\n")
        output.write(f"|Blinker     |{patterns['Blinker']}|{percentilePatterns['Blinker']}|\n")
        output.write(f"|Toad        |{patterns['Toad']}|{percentilePatterns['Toad']}|\n")
        output.write(f"|Beacon      |{patterns['Beacon']}|{percentilePatterns['Beacon']}|\n")
        output.write(f"|Glider      |{patterns['Glider']}|{percentilePatterns['Glider']}|\n")
        output.write(f"Lg Spship    |{patterns['Lg Spship']}|{percentilePatterns['Lg Spship']}|\n")
        output.write("−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−\n")
        output.write(f"TOTAL        |{patterns['Total']}|         |\n")
        output.write("−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−\n\n")

def plot_universe(universe, padding: int, grid : bool = True) -> None:
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

    # Calculates the coordinates of the cells at the border
    limits = center_view(universe)

    patterns = countPatterns(cell_states, limits) # count the patterns at every generation
    generate_output(patterns)

    print(generation, ": ", patterns)

    min_x, min_y, max_x, max_y = 0, 0, universe.width, universe.height

    if limits[0] >= padding: min_x =  limits[0] - padding
    if limits[1] <= (universe.width-padding): max_x =  limits[1] + padding

    if limits[2] >= padding: min_y =  limits[2] - padding
    if limits[3] <= (universe.height-padding): max_y =  limits[3] + padding

    ax.set_xlim(round(min_x), round(max_x)) # zoom plot view to the region where cells exist
    ax.set_ylim(round(min_y), round(max_y))
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
            # we add one to the coordinate because we will add a padding of one cell to each side of the universe
            _active_cells.extend(tuple(list(int(x)+1 for x in line.split())) for line in lines[2:]) 
            universe = create_universe(_width, _height, _active_cells)
        else:
            print(".in file not found. Please check file name.")
            exit()

window = tk.Tk()
text = tk.Text(window)
text.insert("1.0", f"Generation {generation} of {_generations}")

padding = 15     # the distance between the border cell and the visible plot ----------------------------------------------------------------

plot_universe(universe, padding)
canvas = FigureCanvasTkAgg(fig, window)
toolbar = Navbar(canvas, window)
toolbar.update()

# TKinter button function
def one_generation_button_click() -> None:
    # GOL variables
    global universe
    global generation
    global _generations
    
    # TK widgets
    global text
    global canvas
        
    if generation <= _generations:
        universe.update_universe()
        generation += 1
        if generation == _generations: 
            button_one_gen.configure(state="disabled")  
        plot_universe(universe, padding)
        canvas.draw()
        text.delete("1.0", "2.0")
        text.insert("1.0", f"Generation {generation} of {_generations}")
        window.update()

def all_generations_button_click():
    global all_gen_loop 
    all_gen_loop = True
    button_stop.configure(state="normal")
    button_all_gens.configure(state="disabled")
    button_one_gen.configure(state="disabled")
    for gen in range(generation, _generations):
        if not all_gen_loop: break
        one_generation_button_click()
        time.sleep(.1)
    button_stop.configure(state="disabled")

def stop_button_click():
    global all_gen_loop
    button_all_gens.configure(state="normal")
    button_one_gen.configure(state="normal")
    all_gen_loop = False
    if all_gen_loop:
        loop_thread = threading.Thread(target=all_generations_button_click)
        loop_thread.start()

all_gen_loop = False

button_one_gen = tk.Button(window, text=f"Run NEXT Generation", command=one_generation_button_click)
button_all_gens = tk.Button(window, text=f"Run ALL Generations", command=all_generations_button_click)
button_stop = tk.Button(window, text=f"STOP All Gen Loop", command=stop_button_click)
button_stop.configure(state="disabled")
text.config(height=1)
text.pack()
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
button_one_gen.pack()
button_all_gens.pack()
button_stop.pack()

window.mainloop()