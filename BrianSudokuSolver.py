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

# instantiate the tougher sudoku
tougher_grid = Grid(sudoku_game[13], sudoku_game[14])
# call in general solver
button.triggered.connect(tougher_grid.on_next_button_clicked)

# add the grid to the scene
main_scene.addItem(tougher_grid)

# show the main window
main_window.show()
# execute the app code
sudoku_app.exec()

