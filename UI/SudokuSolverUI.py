#AUTHOR: Smayan Nirantare

from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import copy
from constants import *
from SudokuSolver import SudokuSolver

class SudokuSolverUI(QWidget):
    def __init__(self, mainWin=None, board=None):
        super(SudokuSolverUI, self).__init__()

        self.mainWin = mainWin
        self.mainWin.setWindowTitle("Sudoku Solver")
        #size of window
        self.screenWidth = COLS * CELL_SIZE
        self.screenHeight = ROWS * CELL_SIZE + RELIEF

        #illustrating the solving of the board
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.illustrateSolution)


        #if board is true use the one passed in
        if board:
            self.board = board
        #else create new blank board
        else:
            self.board = [[0 for i in range(ROWS)] for j in range(COLS)]


        self.initUI()        
    
    def initUI(self):

        self.mainWin.setFixedSize(self.screenWidth, self.screenHeight)

        #2D array of Entries to represent the sudoku board
        self.cells = [[QLineEdit(self) for num in range(COLS)] for j in range(ROWS)]

        #solve button
        self.solveButton = QPushButton("Solve", self)
        self.solveButton.setGeometry(CELL_SIZE*3, (self.screenHeight - RELIEF)+10, CELL_SIZE*3, RELIEF-20)
        self.solveButton.setStyleSheet("background-color: GREEN; color: white")
        self.solveButton.setFont(FONT2)
        self.solveButton.clicked.connect(self.preSolve)

        #main menu button
        mainMenuButton = QPushButton("New", self)
        mainMenuButton.setGeometry(CELL_SIZE//2, (self.screenHeight - RELIEF)+10, CELL_SIZE*2, RELIEF-20)
        mainMenuButton.setStyleSheet("background-color: ORANGE; color: white")
        mainMenuButton.setFont(FONT2)
        mainMenuButton.clicked.connect(self.mainWin.startStartUpUI)

        #edit menu button
        editButton = QPushButton("Edit", self)
        editButton.setGeometry(CELL_SIZE*6 + CELL_SIZE//2, (self.screenHeight - RELIEF)+10, CELL_SIZE*2, RELIEF-20)
        editButton.setStyleSheet("background-color: AQUA; color: black")
        editButton.setFont(FONT2)
        editButton.clicked.connect(lambda: self.mainWin.startSudokuEditUI(self.board))

        self.mainWin.createGrid(self, self.cells, self.board)

    
    #Calls solve function
    def preSolve(self):

        #parsing the board into a 2D array before resetting to incorporate any edits made my the user
        self.board = self.mainWin.parse(self.cells)
        #resetting the board
        self.mainWin.createGrid(self, self.cells, self.board)
        
        #solver object
        #creating a copy of the initial board for the class to use
        solver = SudokuSolver(copy.deepcopy(self.board))
        #solving the board if it is valid
        if solver.boardIsValid():
            isSolution = solver.solve()
            #getting the solution board
            self.solutionBoard = solver.getSolution()
            self.illustratedBoard = solver.getIllustratedBoard()
        else:
            self.mainWin.showWarning("Invalid board")
            return

        
        #only if there is a solution and the whole board is not solved
        if isSolution and not SudokuSolver.solved(self.board):        
            #illustrating the solution by showing the method of solving (backtracking)
            self.index = 0
            self.timer.start(45)#delay between each step
        else:
            self.mainWin.showWarning("No Solution!" if not isSolution else "Already Solved!")

    #loop function
    def illustrateSolution(self):
        #getting each valid number tries for the row, col
        num, row, col = self.illustratedBoard[self.index]

        #color: green is final number, red indicates invalid number
        if (self.solutionBoard[row][col] == num):
            color = GREEN
        else:
            color = RED

        #set style and color
        self.cells[row][col].setStyleSheet("border: 1px solid black; background-color: white; color: " + color)
        self.cells[row][col].setText(str(num))

        #stopping the loop function if the end of the list is reached
        self.index += 1
        if self.index == len(self.illustratedBoard):
            self.timer.stop()
            self.index = 0
    

