import sys #For parameters
import os #For file checking

class Cell:
    def __init__(self, coord_x : int, coord_y : int):
        self.x : int = coord_x
        self.y : int = coord_y
        self.state : bool = False
    def change_state(self):
        self.state = not self.state
    def __repr__(self) -> str:
        value : str = "X" if self.state else "O"
        return f"{value}"

class Universe:
    def __init__(self, width: int, height: int):
        self.cells = [[Cell(i, j) for i in range(height)] for j in range(width)]
    def __repr__(self) -> str:
        string = ""
        for row in self.cells:
            for cell in row:
                string = string + str(cell)
            string = string + "\n"
        return string
    def change_cell(self, cell : tuple[int, int]):
        self.cells[cell[0]][cell[1]].change_state()

def create_universe(width: int, height: int, active_cells : list[tuple[int, int]] = []) -> Universe:
    universe = Universe(width, height)
    for cell in active_cells:
        universe.change_cell(cell)
    return universe

universe = None

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
            universe = create_universe(20, 20)
        else:
            print(".in file not found. Please check file name.")
            exit()

print(universe)