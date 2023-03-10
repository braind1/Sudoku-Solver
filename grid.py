# This file contains the entire grid class
from PySide6.QtWidgets import QGraphicsRectItem
from typing import Callable, List
from cell import Cell


class Grid(QGraphicsRectItem):

    def __init__(self, game, game_solution):
        # initialize the parent class
        super().__init__()
        # create the list of cells
        self.cells: List[Cell] = []
        # create all 81 instances of cell, then add them to the list of cells
        self.cell_generate(game)
        # create the solution as an attribute to check against later
        self.full_solution: List[str] = list(game_solution)
        # populate the lists of shared houses for each cell
        self.cell_shared_house_generate()
        # create a list of the solving techniques the grid has
        self.solve_techniques: List[Callable] = [self.single_cand_solve,
                                                 self.full_grid_lone_candidates,
                                                 self.naked_pair_full_grid,
                                                 self.pointing_pairs_full_grid,
                                                 self.bi_value_graveyard]
        # create a variable to track the number of times a solving technique was used
        self.num_iterations: int = 0

    def cell_generate(self, game: str):
        # iterate for all 81 cells
        for cells in range(len(game)):
            # create a temporary variable to represent the current cell being instantiated
            _current_cell: Cell = Cell(self, cells)
            # append the list with an instance of the Cell class
            self.cells.append(_current_cell)
            # position the cell in the grid
            _current_cell.setPos((_current_cell.position[1] - 1) * _current_cell.rect().width(), (_current_cell.position[0] - 1) * _current_cell.rect().height())
            # set the given attribute to the corresponding digit in the given problem
            _current_cell.given = int(game[cells])
            # if the given isn't 0, the cell should have no candidates
            if _current_cell.given != 0:
                # set the candidates list to an empty list
                _current_cell.candidates.clear()
                # set the solution for the cell to the given
                _current_cell.solution = _current_cell.given
        # determine the size of the grid based on the height and width of the cells
        self.setRect(0, 0, self.cells[0].rect().width() * 9, self.cells[0].rect().height() * 9)

    # define a function that populates the shared house lists immediately after cell generation
    def cell_shared_house_generate(self):
        # iterate the shared house generation for every cell in the list of cells
        for cell in self.cells:
            self.full_attribute_find(cell)

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
                cell_of_interest.shared_houses[attr].append(self.cells[test_cell])

    # define a function that finds all 3 shared attributes (row, column, and block)
    def full_attribute_find(self, cell_of_interest: Cell):
        # repeat for all 3 shared attributes
        for attr in range(len(cell_of_interest.shared_houses)):
            # call the function to append the appropriate list (attr) when given the cell of interest
            self.single_shared_attribute_find(cell_of_interest, attr)

    # define a function that calls candidate check and is passed the list of cells with a shared attribute
    def row_candidate_modify(self, cell_of_interest: Cell, attr: int):
        # repeat candidate check for all cells in the shared list
        for test_cell_index in range(len(cell_of_interest.shared_houses[attr])):
            # calls the candidate check function with the nth element of the appropriate list (attr)
            self.candidate_check(cell_of_interest, cell_of_interest.shared_houses[attr][test_cell_index])

    # create a function that modifies the candidates list of a cell based on all 3 attributes
    def full_candidate_modify(self, cell_of_interest: Cell):
        # repeat the row modify for all 3 attributes
        for attr in range(len(cell_of_interest.shared_houses)):
            # calls the row modify function for cell of interest and all the attributes
            self.row_candidate_modify(cell_of_interest, attr)

    # create a function that calls the full candidate modify function for all cells in the grid
    def full_grid_candidates(self):
        # repeat for all 81 cells in the grid
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
        for test_cell_index in range(len(cell_of_interest.shared_houses[attr])):
            # check if the test cell is the cell of interest
            if cell_of_interest.shared_houses[attr][test_cell_index] is not cell_of_interest:
                # add the candidates to the temporary list as long as the test cell isn't the cell of interest
                _temp_lone_candidate_list.extend(cell_of_interest.shared_houses[attr][test_cell_index].candidates)
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
        for attr in range(len(cell_of_interest.shared_houses)):
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

    @staticmethod
    # define a function that makes a list of all the candidates lists in a shared house
    def shared_house_candidates_list(cell_of_interest: Cell, attr: int) -> List[list]:
        # initialize a temporary empty list
        _shared_house_candidates: List[List[int]] = []
        # iterate over all test cells in the specific shared house
        for test_cell in cell_of_interest.shared_houses[attr]:
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
        for test_cell in cell_of_interest.shared_houses[attr]:
            # checks if the test cell isn't the cell of interest and the test cell isn't the naked pair
            if test_cell is not cell_of_interest and test_cell.candidates != cell_of_interest.candidates:
                # sets the test cell's candidates to the remaining candidates after removing the cell of interest's candidates
                test_cell.candidates = list(set(test_cell.candidates).difference(cell_of_interest.candidates))
                # order the candidates in case the set takes them out of order
                test_cell.candidates.sort()

    # define a function that repeats the naked pair check for all shared houses
    def naked_pair_full_house(self, cell_of_interest: Cell):
        # repeat the function for all shared houses
        for attr in range(len(cell_of_interest.shared_houses)):
            # call the naked pair find for the specific house
            self.naked_pair_in_shared_house(cell_of_interest, attr)

    # define a function that does the full naked pair search for all cells in the grid
    def naked_pair_full_grid(self):
        # iterate for all cells in the grid
        for cell in self.cells:
            # call the naked pair function for its full house
            self.naked_pair_full_house(cell)

    @staticmethod
    # define a function that generates the 2 lists necessary for the pointing pairs algorithm (works for all 4 cases)
    # the outer and inner house ints are the indexes of the shared attribute in the cell's shared house list
    # the return lists contain the all the candidates in both houses, and the candidates in the outer but not the inner house
    def pointing_pairs_base_list(cell_of_interest: Cell, outside_house: int, inside_house: int) -> (
            List[int], List[int]):
        # define 2 temporary lists of candidates to determine if a candidate is a pointing pair
        _2_shared_houses_candidates_list: List[int] = []
        _only_outer_house_candidates_list: List[int] = []
        # iterate over all cells in the outer shared house
        for test_cell in cell_of_interest.shared_houses[outside_house]:
            # check if the cell is also in the second shared house
            if test_cell in cell_of_interest.shared_houses[inside_house]:
                # if it is, add all the test cell's candidates to the list of candidates in both houses
                _2_shared_houses_candidates_list.extend(test_cell.candidates)
            else:
                # otherwise, add all the test cell's candidates to the list of candidates only in the outer house
                _only_outer_house_candidates_list.extend(test_cell.candidates)
        # return both lists for usage
        return _2_shared_houses_candidates_list, _only_outer_house_candidates_list

    # define the base case of the pointing pairs technique that operates on the 2 lists and can be used for all 4 variations
    def pointing_pairs_base(self, cell_of_interest: Cell, outside_house: int, inside_house: int):
        # obtain the necessary lists to find the pointing pairs
        _both_houses_candidates_list, _single_house_candidates_list = \
            self.pointing_pairs_base_list(cell_of_interest, outside_house, inside_house)
        # iterate for all candidates in the cell of interest
        for candidate in cell_of_interest.candidates:
            if _both_houses_candidates_list.count(candidate) > 1 and candidate not in _single_house_candidates_list:
                # call the removal function
                self.pointing_pairs_removal(cell_of_interest, outside_house, inside_house, candidate)

    @staticmethod
    # define a function to remove pointing pairs from the cells in the inner house but not the outer house
    def pointing_pairs_removal(cell_of_interest: Cell, outside_house: int, inside_house: int, candidate: int):
        # define a temporary lists to help remove the candidate from the correct cells
        _both_shared_houses_cells_list: List[Cell] = []
        # iterate over all cells in the outer shared house
        for test_cell in cell_of_interest.shared_houses[outside_house]:
            # check if the cell is also in the second shared house
            if test_cell in cell_of_interest.shared_houses[inside_house]:
                # if it is, add the test cell to the list of cells in both houses
                _both_shared_houses_cells_list.append(test_cell)
        # iteratively remove the candidate from cells in the inside house not in both houses
        for test_cell in cell_of_interest.shared_houses[inside_house]:
            # check if the test cell is in both shared houses
            if test_cell not in _both_shared_houses_cells_list and candidate in test_cell.candidates:
                # if the test cell is only in the inside house, remove the candidate from the test cell's candidates list
                test_cell.candidates.remove(candidate)

    # define a function that maps an iterable with each variation of pointing pair, and executes the algorithm
    def pointing_pairs_full_cell(self, cell_of_interest: Cell):
        # iterate for the 4 variations
        for variation in range(4):
            # calculate the mapped outside house
            _outside_house = int((5 / 6) * (variation ** 3) - (7 / 2) * (variation ** 2) + (8 / 3) * variation + 2)
            # calculate the mapped inside house
            _inside_house = int((-1 / 6) * (variation ** 3) + (1 / 2) * (variation ** 2) + (2 / 3) * variation)
            # call the base function for the cell of interest and the mapped outer and inner houses
            self.pointing_pairs_base(cell_of_interest, _outside_house, _inside_house)

    # define a function that iterates all versions of the pointing pairs technique for all cells
    def pointing_pairs_full_grid(self):
        # iterate for all cells in the grid
        for cell in self.cells:
            # call the pointing pairs function
            self.pointing_pairs_full_cell(cell)

    # define a function that finds the number of unsolved cells in the grid
    def unsolved_in_grid(self):
        # initialize the number of unsolved to 0
        _unsolved_cells_in_grid: int = 0
        # iterate for all cells in the grid
        for cell in self.cells:
            # add all the cells with candidates
            if len(cell.candidates) > 0:
                # increase the number of unsolved cells by 1
                _unsolved_cells_in_grid += 1
        # return the number of unsolved cells
        return _unsolved_cells_in_grid

    # define the outer driver for the BUG algorithm
    def bi_value_graveyard(self):
        # get the total grid candidates and total unsolved cells
        _grid_candidates = self.candidates_in_grid()
        _grid_unsolved = self.unsolved_in_grid()
        # check the 2 necessary conditions for the algorithm
        # grid candidates will always be odd (2^n + 1), and will always have the maximum number of unsolved cells
        # max number of unsolved cells works out to be the grid candidates integer division by 2
        if _grid_candidates % 2 == 1 and _grid_candidates // 2 == _grid_unsolved:
            # iterate for all cells
            for cell in self.cells:
                # only pass the function the cell that has 3 candidates
                if len(cell.candidates) == 3:
                    # call the bug finder function with the cell and the shared row (any shared house will work)
                    # TODO - optimize the house chosen
                    self.bvg_finder(cell, 0)
                    # end the loop after the bug cell has been found
                    break

    @staticmethod
    # define the main bi value graveyard finder function
    def bvg_finder(cell_of_interest: Cell, house: int):
        # initialize the list of candidates in the shared house
        _shared_house_candidates: List[int] = []
        # generate the list of all candidates in the shared house
        for test_cell in cell_of_interest.shared_houses[house]:
            # extend the list of shared candidates with test cell's candidates
            _shared_house_candidates.extend(test_cell.candidates)
        # create a list of only 1 instance of each candidate in the shared house
        _shared_house_unique_candidates = list(set(_shared_house_candidates))
        # initialize the list of candidate counts
        _candidate_counts: List[int] = []
        # iteratively check each candidate in the unique candidates list
        for candidate in _shared_house_unique_candidates:
            # count the number of times a candidate appears in the shared house
            _single_candidate_count = _shared_house_candidates.count(candidate)
            # append the candidate counts list with the count of each candidate
            _candidate_counts.append(_single_candidate_count)
        # get the index of the bvg solution from the candidates count list
        _bvg_solution_index = _candidate_counts.index(3)
        # set the cell of interest's solution to the solution index in the unique candidates list
        cell_of_interest.set_solution(_shared_house_unique_candidates[_bvg_solution_index])

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
            # increment the number of iterations performed
            self.num_iterations += 1
            # tell the user what function was used during the current iteration of solving
            print(f'The technique used during iteration {self.num_iterations} was:', functions[0],
                  'Total candidate count is now:', self.candidates_in_grid())
            # print the current solution
            self.solution_print()
            # print the given solution
            self.solve_check()
            # update the number of candidates for the previous and current iterations
            _previous_number_candidates = _number_candidates
            _number_candidates = self.candidates_in_grid()
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
        # create a variable for the current number of candidates in the grid
        _number_candidates: int = self.candidates_in_grid()
        # create a variable for the number of candidates in the grid in the previous iteration
        _previous_number_candidates: int = 729
        # iterate while the solving technique reduces the number of candidates
        while _previous_number_candidates > _number_candidates > 0:
            # iterate for all solving techniques
            for function_index in range(len(self.solve_techniques)):
                # give the max function iterations all functions up to the function index
                self.max_function_iterations(self.solve_techniques[:function_index + 1])
                # once the sudoku is solved, break out of the loop
                if self.solve_check():
                    break
            # update the number of candidates for the previous and current iterations
            _previous_number_candidates = _number_candidates
            _number_candidates = self.candidates_in_grid()
