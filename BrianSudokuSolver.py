from typing import Callable, List


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
        # create a list of cells in the same row
        self.shared_row: List[Cell] = []
        # create a list of cells in the same column
        self.shared_column: List[Cell] = []
        # create a list of cells in the same block
        self.shared_block: List[Cell] = []
        # create a list of those shared lists
        self.shared_house: List[list] = [self.shared_row, self.shared_column, self.shared_block]

    # add the string method to print a basic string with all the information about the instance of a cell
    def __str__(self):
        # add all the attributes of the cell to the string
        return f'p:{self.position}g:{self.given}c:{self.candidates}s:{self.solution}b:{self.block}'

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

    # define a function to set a solution and clear the candidates afterwards
    def set_solution(self, solution: int):
        # set the solution to the solution
        self.solution = solution
        # clear the candidates list
        self.candidates.clear()


class Grid:
    def __init__(self, game, game_solution):
        # create the list of cells
        self.cells: List[Cell] = []
        # create all 81 instances of cell, then add them to the list of cells
        self.cell_generate(game)
        # create the solution as an attribute to check against later
        self.full_solution: List[str] = list(game_solution)
        # populate the lists of shared houses for each cell
        # self.cell_shared_house_generate()
        # create a list of the solving techniques the grid has
        self.solve_techniques: List[Callable] = [self.single_cand_solve,
                                                 self.full_grid_lone_candidates,
                                                 self.naked_pair_full_grid]
        # create a variable to track the number of times a solving technique was used
        self.num_iterations: int = 0

    def cell_generate(self, game: str):
        # iterate for all 81 cells
        for cells in range(len(game)):
            # append the list with an instance of the Cell class
            self.cells.append(Cell(cells))
            # set the given attribute to the corresponding digit in the given problem
            self.cells[cells].given = int(game[cells])
            # if the given isn't 0, the cell should have no candidates
            if self.cells[cells].given != 0:
                # set the candidates list to an empty list
                self.cells[cells].candidates.clear()
                # set the solution for the cell to the given
                self.cells[cells].solution = self.cells[cells].given

    # define a function that populates the shared house lists immediately after cell generation
    def cell_shared_house_generate(self):
        # iterate the shared house generate for every cell in the list of cells
        map(Grid.full_attribute_find, self.cells)
        # TODO: make the map work

    @staticmethod
    # create a function that removes givens and solutions of test cell from the candidates list of cell of interest
    # takes the instance of the cells as arguments cell of interest and test cell
    def candidate_check(cell_of_interest: Cell, test_cell: Cell):
        # executes if the given is currently in the candidates list, ie given != 0
        if test_cell.given in cell_of_interest.candidates:
            # removes the given of b from the candidates list of a
            cell_of_interest.candidates.remove(test_cell.given)

        # executes if cell b has a solution, and it is in the candidates list
        if test_cell.solution in cell_of_interest.candidates:
            # removes the solution of b from the candidates list of a
            cell_of_interest.candidates.remove(test_cell.solution)

    @staticmethod
    # create a function that can reference the single attribute (attr) of a list given any instance of the class (cell instance)
    def attribute_test(cell_instance: Cell, attr: int) -> int:
        # create a list of the cell attributes to test corresponding to the row, column, and block
        _attribute_test_list = [cell_instance.position[1], cell_instance.position[0], cell_instance.block]
        # returns the single attribute element that was passed
        return _attribute_test_list[attr]

    # Create a function that checks all 81 cells for 1 shared attribute, then appends the associated list.
    # Will be passed the index of the cell of interest and the index of the attribute it is checking for (attr)
    def single_shared_attribute_find(self, cell_of_interest: Cell, attr: int):
        # checks all 81 instances of cell
        for test_cell in range(len(self.cells)):
            # if the attribute (b) of the cell of interest (a) matches the attribute (b) of the test cell (f)
            if self.attribute_test(cell_of_interest, attr) == self.attribute_test(self.cells[test_cell], attr):
                # append the corresponding attribute list (b) with test cell (f)
                cell_of_interest.shared_house[attr].append(self.cells[test_cell])

    # define a function that finds all 3 shared attributes (row, column, and block)
    def full_attribute_find(self, cell_of_interest: Cell):
        # repeat for all 3 shared attributes
        # map(self.single_shared_attribute_find, cell_of_interest.shared_house)
        for attr in range(len(cell_of_interest.shared_house)):
            # call the function to append the appropriate list (attr) when given the cell of interest
            self.single_shared_attribute_find(cell_of_interest, attr)

    # define a function that calls candidate check and is passed the list of cells with a shared attribute
    def row_candidate_modify(self, cell_of_interest: Cell, attr: int):
        # repeat candidate check for all cells in the shared list
        # map(self.candidate_check, cell_of_interest.shared_house[attr])
        for test_cell_index in range(len(cell_of_interest.shared_house[attr])):
            # calls the candidate check function with the nth element of the appropriate list (attr)
            self.candidate_check(cell_of_interest, cell_of_interest.shared_house[attr][test_cell_index])

    # create a function that modifies the candidates list of a cell based on all 3 attributes
    def full_candidate_modify(self, cell_of_interest: Cell):
        # call the function to find all the cells that have shared attributes
        # TODO - want to populate the shared houses list after cell generation, not after everytime a cell is passed
        self.full_attribute_find(cell_of_interest)
        # repeat the row modify for all 3 attributes
        for attr in range(len(cell_of_interest.shared_house)):
            # calls the row modify function for cell of interest and all the attributes
            self.row_candidate_modify(cell_of_interest, attr)

    # create a function that calls the full candidate modify function for all cells in the grid
    def full_grid_candidates(self):
        # repeat for all 81 cells in the grid
        # map(self.full_candidate_modify, self.cells) - TODO: attempted to use the map function to replace the loop, didn't work
        for cell_index in range(len(self.cells)):
            # call the full candidate modify on the ath cell of the grid
            self.full_candidate_modify(self.cells[cell_index])

    # define a function that promotes a candidate to a solution
    def solution_promote(self):
        # iterates over all 81 cells
        for cell in range(len(self.cells)):
            # check if there is only one candidate
            if len(self.cells[cell].candidates) == 1:
                # promote the single candidate to a solution
                self.cells[cell].set_solution(self.cells[cell].candidates[0])

    # define a function that finds all the simple candidates and promotes them
    def single_cand_solve(self):
        # call the function to find the single candidates
        self.full_grid_candidates()
        # call the promotion function
        self.solution_promote()

    # define a function that prints the solved sudoku as a single string
    def solution_print(self):
        # create an empty string to add the solutions to
        solution_string = '  '
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
        # create a temporary variable to represent the previous number of unsolved cells
        _current_unsolved: List[int] = [81, self.number_unsolved()]
        # initialize the unsolved index to 1
        _current_unsolved_index = 1
        # while cells are still unsolved
        while _current_unsolved[_current_unsolved_index] != _current_unsolved[_current_unsolved_index - 1]:
            # apply the basic solving technique
            self.single_cand_solve()
            # append the current unsolved list to know whether to continue the loop
            _current_unsolved.append(self.number_unsolved())
            # iterate the index being checked for
            _current_unsolved_index += 1
            # print the resultant board
            self.solution_print()
        # at the end, check whether the solved solution matches the given solution, and print the output
        print(self.solve_check())

    # define a function that checks whether the solved solution is the same as the given solution
    def solve_check(self) -> bool:
        num_matches = 0
        for a in range(len(self.cells)):
            if self.cells[a].solution == int(self.full_solution[a]):
                num_matches += 1
        if num_matches == 81:
            print(f"s:{''.join(self.full_solution)}", 'True')
            return True
        else:
            print(f"s:{''.join(self.full_solution)}", 'False')
            return False

    @staticmethod
    # iterate for all cells in the shared attribute(house), add all candidates in the house to a temporary list (except the cell of interest's candidates)
    def temp_lone_candidate_list(cell_of_interest: Cell, attr: int) -> List[int]:
        # create a temporary list of all candidates in the shared house (without adding the candidates from the cell of interest)
        _temp_lone_candidate_list: List[int] = []
        # iterate for all test cells in the shared house
        for test_cell_index in range(len(cell_of_interest.shared_house[attr])):
            # check if the test cell is the cell of interest
            if cell_of_interest.shared_house[attr][test_cell_index] is not cell_of_interest:
                # add the candidates to the temporary list as long as the test cell isn't the cell of interest
                _temp_lone_candidate_list.extend(cell_of_interest.shared_house[attr][test_cell_index].candidates)
        # return the temporary list of candidates to search through
        return _temp_lone_candidate_list

    # define a function that iterates over all the candidates in the cell of interest, and checks them against the temporary candidates list
    def potential_lone_candidate_search(self, cell_of_interest: Cell, attr: int):
        # assign the result of the temporary lone candidate list to another local temporary list
        _temp_house_candidates: List[int] = self.temp_lone_candidate_list(cell_of_interest, attr)
        # iterate over all the candidates in the cell of interest
        for candidate in cell_of_interest.candidates:
            # check if the candidate is in the house's candidate list
            if candidate not in _temp_house_candidates:
                # if the candidate is not found elsewhere in the house, the candidate is the solution to the cell of interest
                cell_of_interest.set_solution(candidate)

    # define a function that calls the potential lone candidate search for all attributes in the house
    def full_cell_lone_candidate_search(self, cell_of_interest: Cell):
        # iterate over every attribute in the house
        for attr in range(len(cell_of_interest.shared_house)):
            # search for the lone candidates
            self.potential_lone_candidate_search(cell_of_interest, attr)

    # define a function that finds the lone candidates of every cell
    def full_grid_lone_candidates(self):
        # iterate for all cells in the grid
        for cell in self.cells:
            # apply the full lone candidate method to the cell
            self.full_cell_lone_candidate_search(cell)
            # update the candidates list of all cells in the grid
            self.full_grid_candidates()

    # define the level 2 solver that incorporates the lone candidate algorithm into the simple solver
    def lev2_solve(self):
        # create a temporary variable to represent the previous number of unsolved cells
        _current_unsolved_lev2: List[int] = [81, self.number_unsolved()]
        # initialize the unsolved index to 1
        _current_unsolved_index = 1
        # while cells are still unsolved
        while _current_unsolved_lev2[_current_unsolved_index] != _current_unsolved_lev2[_current_unsolved_index - 1]:
            # call the simple solve algorithm as many times as it works
            self.simple_solve()
            # then move onto the lone candidate search
            # self.grid_lone_candidate_search(0)
            self.full_grid_lone_candidates()
            # append the current unsolved list to know whether to continue the loop
            _current_unsolved_lev2.append(self.number_unsolved())
            # iterate the index being checked for
            _current_unsolved_index += 1
            # print the resultant board
            self.solution_print()
        # at the end, check whether the solved solution matches the given solution, and print the output
        print(self.solve_check())

    @staticmethod
    # define a function that makes a list of all the candidates lists in a shared house
    def shared_house_candidates_list(cell_of_interest: Cell, attr: int) -> List[list]:
        # initialize a temporary empty list
        _shared_house_candidates: List[List[int]] = []
        # iterate over all test cells in the specific shared house
        for test_cell in cell_of_interest.shared_house[attr]:
            # check if the test cell is the cell of interest
            if test_cell is not cell_of_interest:
                # if the test cell isn't the cell of interest, add its list of candidates to the temporary list of candidate lists
                _shared_house_candidates.append(test_cell.candidates)
        # return the list of candidates lists
        return _shared_house_candidates

    # define a function that checks if the cell of interest's candidate list is in the temporary list of candidate lists
    def naked_pair_in_shared_house(self, cell_of_interest: Cell, attr: int):
        # create the temporary list of candidate lists in the specific shared house
        _temp_shared_house_candidates = self.shared_house_candidates_list(cell_of_interest, attr)
        # check if the cell of interest has 2 candidates and its candidates list is in the temporary list of candidates lists
        # TODO - does the logic work for the 3 candidate version?
        if len(cell_of_interest.candidates) == 2 and cell_of_interest.candidates in _temp_shared_house_candidates:
            # remove the candidates from all cells containing those candidates except the other cell with the same candidates list
            # TODO - does this function make sense and work correctly?
            self.naked_pair_candidate_removal(cell_of_interest, attr)
        elif len(cell_of_interest.candidates) == 3 and _temp_shared_house_candidates.count(
                cell_of_interest.candidates) == 2:
            # removes the candidates from all cells containing those candidates except the 2 other cells with the same candidates lists
            self.naked_pair_candidate_removal(cell_of_interest, attr)

    @staticmethod
    # define a function that removes the cell of interest's candidates from all cells in the shared house
    def naked_pair_candidate_removal(cell_of_interest: Cell, attr: int):
        # iterates for all test cells in the shared house
        for test_cell in cell_of_interest.shared_house[attr]:
            # checks if the test cell isn't the cell of interest and the test cell isn't the naked pair
            if test_cell is not cell_of_interest and test_cell.candidates != cell_of_interest.candidates:
                # sets the test cell's candidates to the remaining candidates after removing the cell of interest's candidates
                test_cell.candidates = list(set(test_cell.candidates).difference(cell_of_interest.candidates))
                # order the candidates in case the set takes them out of order
                test_cell.candidates.sort()

    # define a function that repeats the naked pair check for all shared houses
    def naked_pair_full_house(self, cell_of_interest: Cell):
        # repeat the function for all shared houses
        for attr in range(len(cell_of_interest.shared_house)):
            # call the naked pair find for the specific house
            self.naked_pair_in_shared_house(cell_of_interest, attr)

    # define a function that does the full naked pair search for all cells in the grid
    def naked_pair_full_grid(self):
        # iterate for all cells in the grid
        for cell in self.cells:
            # call the naked pair function for its full house
            self.naked_pair_full_house(cell)
        # TODO: also should work with a map
        # map(self.naked_pair_full_house, self.cells)

    # define a function that performs a function for the maximum number of times it reduces the candidates in the grid
    def max_function_iterations(self, functions: List[Callable]):
        # create a variable for the current number of candidates in the grid
        _number_candidates: int = self.candidates_in_grid()
        # create a variable for the number of candidates in the grid in the previous iteration
        _previous_number_candidates: int = 729
        # iterate while the solving technique reduces the number of candidates
        while _previous_number_candidates > _number_candidates:
            # call the function passed
            functions[0]()
            # tell the user what function was used during the current iteration of solving
            print('The technique used during this iteration was:', functions[0])
            # print the current solution
            self.solution_print()
            # print the given solution
            self.solve_check()
            # update the number of candidates for the previous and current iterations
            _previous_number_candidates = _number_candidates
            _number_candidates = self.candidates_in_grid()
            # increment the number of iterations performed
            self.num_iterations += 1
        # check if there is only function being passed
        if len(functions) > 1 and _number_candidates > 0:
            # call the recursion with the remaining functions
            self.max_function_iterations(functions[1:])

    # define a function that finds the total number of candidates in the grid
    def candidates_in_grid(self) -> int:
        # initialize the number of candidates to 0
        _total_grid_candidates: int = 0
        # iterate for all cells in the grid
        for cell in self.cells:
            # add the number of candidates in each cell
            _total_grid_candidates += len(cell.candidates)
        # return the total count
        return _total_grid_candidates

    # define a function that gives the max function iteration an incrementing list of solving techniques
    def general_solver(self):
        # iterate for all solving techniques
        for function_index in range(len(self.solve_techniques)):
            # give the max function iterations all functions up to the function index
            self.max_function_iterations(self.solve_techniques[:function_index + 1])
            # print the current solution
            # self.solution_print()
            # once the sudoku is solved, break out of the loop
            if self.solve_check():
                break

    # def simple_solve2(self):
        # self.max_function_iterations(self.solve_techniques[0])
        # print(self.solve_check())
        # print(f'Solving took {self.num_iterations} iterations')


game1 = "004300209005009001070060043006002087190007400050083000600000105003508690042910300"
game1_solution = "864371259325849761971265843436192587198657432257483916689734125713528694542916378"

# game 2 is harder, cannot be solved using the basic technique
game2 = "009070035510040206700006001600007093023010000001000500800000049190000058007000600"
game2_solution = "269871435518349276734256981685427193423915867971683524856132749192764358347598612"

# game 3 requires naked pairs and pointing pairs to solve
game3 = "103065000700020000500300000002650030001430600000017205000006050004080060060040010"
game3_solution = "103065000706120503500370106472650031051432600630017245017296050004581060065743010"

# instantiate the only instance of the grid
# simple_grid = Grid(game1, game1_solution)
# solves the full simple grid
# simple_grid.simple_solve2()

# instantiate the more difficult sudoku
med_grid = Grid(game2, game2_solution)
# apply the level 2 algorithm to the game
# med_grid.lev2_solve()
# med_grid.general_solver()

# instantiate the hard sudoku
hard_grid = Grid(game3, game3_solution)
# call in general solver
hard_grid.general_solver()

# TODO: incorporate map, filter, and reduce in places where they are relevant make the code more efficient
