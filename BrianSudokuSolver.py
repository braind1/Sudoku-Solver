from grid import Grid
from PySide6.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView, QToolBar
from typing import List
from PySide6.QtGui import QAction

# get the game from a text file
with open('sudoku_game.txt', 'r') as sudoku_file:
    # create a new variable as a list of the game (element 0) and the solution (element 1)
    sudoku_game: List[str] = sudoku_file.readlines()

# remove the newline character at the end of each element in the list (left over from readline method)
sudoku_game = list(map(str.strip, sudoku_game))

# create the QApplication to display the sudoku board
sudoku_app = QApplication([])
# create the MainWindow
main_window = QMainWindow()
# resize the window to display large enough for the grid upon launch
main_window.resize(700, 700)
# rename the window
main_window.setWindowTitle('Sudoku Game')
# create the main widget
main_widget = QGraphicsView(main_window)
# add a toolbar to the main widget for the 'next' button
toolbar: QToolBar = QToolBar(main_window)
# add the toolbar to the main window
main_window.addToolBar(toolbar)
# create the button and make it belong to the toolbar
button: QAction = QAction(toolbar)
# set the text for the button
button.setText('Solve')
# add the button to the toolbar
toolbar.addAction(button)
# make the main widget the 'central' widget
main_window.setCentralWidget(main_widget)
# create the object that contains the graphical components of the sudoku
main_scene = QGraphicsScene(main_window)
# tell the widget that the scene exists
main_widget.setScene(main_scene)

# instantiate the only instance of the grid
# simple_grid = Grid(game1, game1_solution)
# solves the full simple grid
# simple_grid.simple_solve2()

# instantiate the more difficult sudoku
# med_grid = Grid(sudoku_game[7], sudoku_game[8])
# apply the level 2 algorithm to the game
# med_grid.lev2_solve()
# med_grid.general_solver()

# instantiate the hard sudoku
# hard_grid = Grid(sudoku_game[10], sudoku_game[11])
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
# tougher_grid.general_solver()
button.triggered.connect(tougher_grid.on_next_button_clicked)

# add the grid to the scene
main_scene.addItem(tougher_grid)

# show the main window
main_window.show()
# execute the app code
sudoku_app.exec()

# TODO: incorporate map, filter, and reduce in places where they are relevant make the code more efficient
