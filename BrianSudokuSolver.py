from typing import List


class Cell:
    def __init__(self, cell_number: int):
        # the x, y position of the cell
        self.position: List[int] = [0, 0]
        # reassigns the position based on the cell number
        self.position_map(cell_number)
        # any given number of the puzzle, otherwise, defaults to 0
        self.given: int = 0
        # list of the potential solutions (candidates) for the cell
        self.candidates: List[int] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        # the solution to the cell (derived from candidates list)
        self.solution: int = 0
        # an internal list used to convert position to block
        # aisle is associated with x position, belt is associated with y position
        self._aisle_belt_list: List[int] = []
        # the block that the cell belongs to
        self.block: int = 0
        # call the block assignment function to reassign the block number
        self.block_assign()

    @staticmethod
    # create a function that takes one of the positions and simplifies it
    def coord_simplify(a: int) -> int:
        # b will always be a number 0-2, denoting the belt or aisle
        b: int = (a - 1) // 3
        # return the actual belt or aisle number
        return b + 1

    def position_map(self, c: int):
        # map the parameter (c) to the x position of the cell, then assign it to the instance's x position
        self.position[0]: int = (c % 9) + 1
        # map the parameter (c) to the y position of the cell, then assign it to the instance's y position
        self.position[1]: int = (c // 9) + 1

    def block_assign(self):
        # add the belt or aisle position to the belt/aisle list for both the x and y positions
        for d in range(len(self.position)):
            # assigns an internal variable to the belt or aisle position
            _aisle_belt = self.coord_simplify(self.position[d])
            # add the belt variable to the belt list
            self._aisle_belt_list.append(int(_aisle_belt))
        # print(f'{self._aisle_belt_list}')

        # maps the belt and aisle number to the correct block
        self.block = 3 * self._aisle_belt_list[1] + self._aisle_belt_list[0] - 3
        # print(f'{self.block}')


class Grid:
    def __init__(self, game, game_solution):
        # create the list of cells
        self.cells: List[Cell] = []
        # create all 81 instances of cell, then add them to the list of cells
        self.cell_generate(game)
        # create a temporary list for all the cells in the same row as the passed cell
        self._current_row: List[Cell] = []
        # create a temporary list for all the cells in the same column as the passed cell
        self._current_column: List[Cell] = []
        # create a temporary list for all the cells in the same block as the passed cell
        self._current_block: List[Cell] = []
        # create a list of the temporary lists so the function can iterate over all 3 lists
        self._shared_row_column_block: List[list] = [self._current_row, self._current_column, self._current_block]
        # create the solution as an attribute to check against later
        self.full_solution: List[str] = list(game_solution)

    def cell_generate(self, game: str):
        # iterate for all 81 cells
        for e in range(81):
            # append the list with an instance of the Cell class
            self.cells.append(Cell(e))
            # set the given attribute to the corresponding digit in the given problem
            self.cells[e].given = int(game[e])
            # if the given isn't 0, the cell should have no candidates
            if self.cells[e].given != 0:
                # set the candidates list to an empty list
                self.cells[e].candidates.clear()
                # set the solution for the cell to the given
                self.cells[e].solution = self.cells[e].given

    # create a function that removes givens and solutions of test cell from the candidates list of cell of interest
    # takes the cell numbers (starting at 0) as arguments cell of interest and test cell
    def candidate_check(self, cell_of_interest: int, test_cell: Cell):
        # executes if the given is currently in the candidates list, ie given != 0
        if test_cell.given in self.cells[cell_of_interest].candidates:
            # removes the given of b from the candidates list of a
            self.cells[cell_of_interest].candidates.remove(test_cell.given)

        # executes if cell b has a solution, and it is in the candidates list
        if test_cell.solution in self.cells[cell_of_interest].candidates:
            # removes the solution of b from the candidates list of a
            self.cells[cell_of_interest].candidates.remove(test_cell.solution)

    # create a function that can reference the single attribute (attr) of a list given any instance of the class (cell instance)
    def attribute_test(self, cell_instance: int, attr: int) -> int:
        # create a list of the cell attributes to test corresponding to the row, column, and block
        _attribute_test_list = [self.cells[cell_instance].position[1], self.cells[cell_instance].position[0], self.cells[cell_instance].block]
        # returns the single attribute element that was passed
        return _attribute_test_list[attr]

    # Create a function that checks all 81 cells for 1 shared attribute, then appends the associated list.
    # Will be passed the index of the cell of interest and the index of the attribute it is checking for (attr)
    def single_shared_attribute_find(self, cell_of_interest: int, attr: int):
        # clear the temporary list associated with the attr
        self._shared_row_column_block[attr].clear()
        # checks all 81 instances of cell
        for f in range(len(self.cells)):
            # if the attribute (b) of the cell of interest (a) matches the attribute (b) of the test cell (f)
            if self.attribute_test(cell_of_interest, attr) == self.attribute_test(f, attr):
                # append the corresponding attribute list (b) with test cell (f)
                self._shared_row_column_block[attr].append(self.cells[f])

    # define a function that finds all 3 shared attributes (row, column, and block)
    def full_attribute_find(self, cell_of_interest: int):
        # repeat for all 3 shared attributes
        for attr in range(len(self._shared_row_column_block)):
            # call the function to append the appropriate list (attr) when given the cell of interest
            self.single_shared_attribute_find(cell_of_interest, attr)

    # define a function that calls candidate check and is passed the list of cells with a shared attribute
    def row_candidate_modify(self, cell_of_interest: int, attr: int):
        # repeat candidate check for all cells in the shared list
        for n in range(len(self._shared_row_column_block[attr])):
            # calls the candidate check function with the nth element of the appropriate list (attr)
            self.candidate_check(cell_of_interest, self._shared_row_column_block[attr][n])

    # create a function that modifies the candidates list of a cell based on all 3 attributes
    def full_candidate_modify(self, cell_of_interest: int):
        # call the function to find all the cells that have shared attributes
        self.full_attribute_find(cell_of_interest)
        # repeat the row modify for all 3 attributes
        for attr in range(len(self._shared_row_column_block)):
            # calls the row modify function for cell of interest and all the attributes
            self.row_candidate_modify(cell_of_interest, attr)

    # create a function that calls the full candidate modify function for all cells in the grid
    def full_grid_candidates(self):
        # repeat for all 81 cells in the grid
        for cell_index in range(len(self.cells)):
            # call the full candidate modify on the ath cell of the grid
            self.full_candidate_modify(cell_index)

    # define a function that promotes a candidate to a solution
    def solution_promote(self):
        # iterates over all 81 cells
        for i in range(len(self.cells)):
            # check if there is only one candidate
            if len(self.cells[i].candidates) == 1:
                # promote the single candidate to a solution
                self.cells[i].solution = self.cells[i].candidates[0]
                # clear the candidates list once the single candidate is a solution
                self.cells[i].candidates.clear()

    # define a function that prints the solved sudoku as a single string
    def solution_print(self):
        # create an empty string to add the solutions to
        solution_string = ''
        # iterate for all 81 cells
        for n in range(len(self.cells)):
            # concatenate the solution string with the nth Cell's solution
            solution_string += str(self.cells[n].solution)
        print(solution_string)

    # define a function that finds the number of unsolved cells
    def number_unsolved(self) -> int:
        num_unsolved = 0
        for a in range(len(self.cells)):
            if len(self.cells[a].candidates) > 0:
                num_unsolved += 1
        return num_unsolved

    # define a function to solve the sudoku
    def simple_solve(self):
        while self.number_unsolved() > 0:
            self.full_grid_candidates()
            self.solution_promote()
        self.solution_print()
        print(self.solve_check())

    # define a function that checks whether the solved solution is the same as the given solution
    def solve_check(self) -> bool:
        num_matches = 0
        for a in range(len(self.cells)):
            if self.cells[a].solution == int(self.full_solution[a]):
                num_matches += 1
        if num_matches == 81:
            return True
        else:
            return False

    # define a function that takes an instance of a cell, a single candidate index, and a test cell and checks if the candidate is in the test cell
    def lone_candidate(self, cell_of_interest: int, candidate_index: int, test_cell: Cell):
        # checks if the candidate of the cell of interest is in the test cell's candidate list
        if self.cells[cell_of_interest].candidates[candidate_index] in test_cell.candidates:
            # if the candidate is in the test cell's candidate, return true
            return True
        else:
            return False

    # define a function that repeats the lone candidate search for all candidates in the test cell given
    def lone_candidate_full(self, cell_of_interest: int, test_cell: Cell):
        # iterates the lone candidate search for all the candidates of the test cell
        for candidate in range(len(self.cells[cell_of_interest].candidates)):
            # assigns a boolean variable that is true if the candidate is not a lone candidate
            is_lone_candidate: bool = self.lone_candidate(cell_of_interest, candidate, test_cell)
            # checks if the lone candidate was found
            if not is_lone_candidate:
                # if the candidate was not found, the candidate is a lone candidate and should
                self.cells[cell_of_interest].candidates = [self.cells[cell_of_interest].candidates[candidate]]
            # if the candidate was found, continue the search


game1 = "004300209005009001070060043006002087190007400050083000600000105003508690042910300"
game1_solution = "864371259325849761971265843436192587198657432257483916689734125713528694542916378"

# game 2 is harder, cannot be solved using the basic technique
game2 = "009070035510040206700006001600007093023010000001000500800000049190000058007000600"

# instantiate the only instance of the grid
grid = Grid(game1, game1_solution)
# print(grid.cells[5].position, grid.cells[5].block, grid.cells[5].given)
# grid.candidate_check(0, grid.cells[2])
# print(grid.cells[0].candidates)
# print(grid.attribute_test(2, 0))
# grid.single_shared_attribute_find(0, 0)
# grid.row_candidate_modify(0, 0)
# grid.full_candidate_modify(1)
# grid.full_grid_candidates()
# grid.solution_promote()
# grid.solution_print()
# print(grid.cells[0].solution)
# print(grid.cells[1].candidates)
grid.simple_solve()
# print(type(grid.cells[0].solution))
# print(grid.full_solution)
# print(type(grid.full_solution[0]))
# grid.solve_check()
