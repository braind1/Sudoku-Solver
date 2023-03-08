from grid import Grid
from typing import List

# get the game from a text file
with open('sudoku_game.txt', 'r') as sudoku_file:
    # create a new variable as a list of the game (element 0) and the solution (element 1)
    sudoku_game: List[str] = sudoku_file.readlines()

# remove the newline character at the end of each element in the list (left over from readline method)
sudoku_game = list(map(str.strip, sudoku_game))


# instantiate the only instance of the grid
# simple_grid = Grid(game1, game1_solution)
# solves the full simple grid
# simple_grid.simple_solve2()

# instantiate the more difficult sudoku
# med_grid = Grid(game2, game2_solution)
# apply the level 2 algorithm to the game
# med_grid.lev2_solve()
# med_grid.general_solver()

# instantiate the hard sudoku
# hard_grid = Grid(game3, game3_solution)
# call in general solver
# hard_grid.general_solver()
# hard_grid.solve_techniques[0]()
# hard_grid.solution_print()

# instantiate the tough sudoku
# tough_grid = Grid(game4, game4_solution)
# call in general solver
# tough_grid.general_solver()

# instantiate the tougher sudoku
tougher_grid = Grid(sudoku_game[1], sudoku_game[2])
# call in general solver
tougher_grid.general_solver()

# TODO: incorporate map, filter, and reduce in places where they are relevant make the code more efficient
# if printing each iteration, need to utilize signals and slots
# every time a solving algorithm is called, produce a signal
# the grid will need to be/have? a slot that is connected to the signal that the solver produces
# when the signal is received, update the grid with the current solution
# might look something like self.printed_grid.connect(self.current_solution_print) to connect the signal and slot
# once the grid is defined, can use the layout function to format the grid in the output window
# remember once we have an instance of the printed grid, to use printed_grid.show() and grid.exec() to actually execute and display the grid
# table printing seems like a reasonable and somewhat simple option for printing the grid
# cell will be derived from QGrpahicsObject so that it inherits painting methods
