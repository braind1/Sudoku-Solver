# This file contains the entire Cell class

from typing import List
from PySide6.QtWidgets import QGraphicsRectItem, QGraphicsTextItem
from PySide6.QtGui import QFont, QFontMetricsF, QPen
from PySide6 import QtCore, QtGui


class Cell(QGraphicsRectItem):

    # create class variables to represent the row and column indexes in the position list
    COL: int = 0
    ROW: int = 1

    def __init__(self, parent, cell_number: int):
        # initialize the parent class
        super().__init__(parent)
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
        self.shared_houses: List[list] = [self.shared_row, self.shared_column, self.shared_block]
        # create 2 q fonts - 1 for the candidates and 1 for the solutions/givens
        self.candidate_font: QFont = QFont('Old English Text MT', 8)
        self.solution_font: QFont = QFont('Old English Text MT', 16)
        # set the default pen
        self.default_pen: QPen = QtGui.QPen()
        # create 3 q pens - 1 for the givens, 1 for the solutions, and 1 for the border
        self.given_pen: QPen = QtGui.QPen(QtCore.Qt.GlobalColor.darkCyan)
        self.solution_pen: QPen = QtGui.QPen(QtCore.Qt.GlobalColor.green)
        self.line_pen: QPen = QtGui.QPen(QtCore.Qt.GlobalColor.darkYellow, 1)
        self.line_pen.setCosmetic(True)
        # set the pen to the line pen to draw the cell borders in the correct color
        self.setPen(self.line_pen)
        # create a variable for the font metrics
        self._font_metrics = QFontMetricsF(self.candidate_font)
        # get the size of the cell
        self.setRect(0, 0, self._font_metrics.height() * 5, self._font_metrics.height() * 5)
        # create a list of 9 Q Graphics Text Items to display the candidates
        self.display_candidates: List[QGraphicsTextItem] = []
        # create a temporary variable to add the given and solution text items to the grid
        self.temp_text_item: QGraphicsTextItem = QGraphicsTextItem(self)
        # call the function to generate the candidate text items
        self.candidate_text_generate()

    # add the string method to print a basic string with all the information about the instance of a cell
    def __str__(self):
        # add all the attributes of the cell to the string
        return f'p:{self.position}g:{self.given}c:{self.candidates}s:{self.solution}b:{self.block}'

    # define a function to generate candidate text items
    def candidate_text_generate(self):
        # iterate for all 9 candidates
        for candidate in range(1, 10):
            # create the current text item with the string of the candidate, and its parent
            _candidate_text_item: QGraphicsTextItem = QGraphicsTextItem(str(candidate), self)
            # set the font of the text item to have all the attributes of a candidate text item
            _candidate_text_item.setFont(self.candidate_font)
            # map number of the candidate to its position in the cell rectangle item
            _candidate_text_item.setPos(
                ((candidate - 1) % 3) + ((candidate - 1) % 3) * (3 * self._font_metrics.height() / 2) +
                (1 / 4) * self._font_metrics.height(),
                ((candidate - 1) // 3) + ((candidate - 1) // 3) * (3 * self._font_metrics.height() / 2) +
                (1 / 4) * self._font_metrics.height())
            # add the current text item to the list of candidate text items
            self.display_candidates.append(_candidate_text_item)

    @staticmethod
    # create a function that takes one of the positions and simplifies it
    def coord_simplify(a: int) -> int:
        # b will always be a number 0-2, denoting the belt or aisle
        b: int = (a - 1) // 3
        # return the actual belt or aisle number
        return b + 1

    def position_map(self, c: int):
        # map the parameter (c) to the x position of the cell, then assign it to the instance's x position
        self.position[Cell.COL]: int = (c % 9) + 1
        # map the parameter (c) to the y position of the cell, then assign it to the instance's y position
        self.position[Cell.ROW]: int = (c // 9) + 1

    def block_assign(self):
        # add the belt or aisle position to the belt/aisle list for both the x and y positions
        for d in range(len(self.position)):
            # assigns an internal variable to the belt or aisle position
            _aisle_belt = self.coord_simplify(self.position[d])
            # add the belt variable to the belt list
            self._aisle_belt_list.append(int(_aisle_belt))
        # maps the belt and aisle number to the correct block
        self.block = 3 * self._aisle_belt_list[1] + self._aisle_belt_list[0] - 3

    # define a function to set a solution and clear the candidates afterwards
    def set_solution(self, solution: int):
        # set the solution to the solution
        self.solution = solution
        # clear the candidates list
        self.candidates.clear()
        # create a new text item for the solution in the painted grid
        self.paint_text_item(solution, self.solution_pen)

    # define a function that paints the given of a cell
    def set_given(self, given: int):
        if given != 0:
            # set the given and solution to the given
            self.given = given
            self.solution = given
            # clear the candidates list
            self.candidates.clear()
            # paint the given text item
            self.paint_text_item(given, self.given_pen)

    # define a function that paints a given or a solution
    def paint_text_item(self, sol_or_given: int, pen: QPen):
        # create the arbitrary text item with the integer value given
        self.temp_text_item.setPlainText(f'{sol_or_given}')
        # set the font of the text item
        self.temp_text_item.setFont(self.solution_font)
        # choose the correct pen to pain with
        self.temp_text_item.setDefaultTextColor(pen.color())
        # position the text item in the cell
        self.temp_text_item.setPos((self.rect().width() / 2) - (self.temp_text_item.boundingRect().width() / 2),
                                   (self.rect().height() / 2) - (self.temp_text_item.boundingRect().height() / 2))
        # show the newly created text item
        self.temp_text_item.show()
        # hide the candidates of the cell
        list(map(QGraphicsTextItem.hide, self.display_candidates))

    # define a method to remove candidates from the instance of the cell and hide the corresponding candidate text item
    def candidate_remove(self, candidate: int):
        # remove the candidate from the instance of the cell
        self.candidates.remove(candidate)
        # hide the corresponding text item
        self.display_candidates[candidate - 1].hide()
