from grid import Grid


game1 = "004300209005009001070060043006002087190007400050083000600000105003508690042910300"
game1_solution = "864371259325849761971265843436192587198657432257483916689734125713528694542916378"

# game 2 is harder, cannot be solved using the basic technique
game2 = "009070035510040206700006001600007093023010000001000500800000049190000058007000600"
game2_solution = "269871435518349276734256981685427193423915867971683524856132749192764358347598612"

# game 3 requires naked pairs and pointing pairs to solve
game3 = "103065000700020000500300000002650030001430600000017205000006050004080060060040010"
game3_solution = "123865497746129583589374126472658931951432678638917245817296354394581762265743819"

# game 4 requires the bi-value graveyard to solve
game4 = "000009030057408010000000075620500001000000000400000067180000000070200340060900000"
game4_solution = "216759834957438612843126975628573491795614283431892567184365729579281346362947158"

# game 5 requires more additional techniques (x-wing and y-wing)
game5 = "000050007030008020002000309000567000906000402000009000703000900050100060100040000"
game5_solution = "849352617637918524512674389421567893976831452385429176763285941254193768198746235"

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
tougher_grid = Grid(game5, game5_solution)
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
