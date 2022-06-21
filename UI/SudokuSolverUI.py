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


        #if board is true, load board from file
        if board is not None:
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

        self.createGrid()

    #creates sudoku board
    def createGrid(self):
        x = 0
        y = 0

        for row in range(ROWS):
            #creating the seperating lines on the grid (Horizontal)
            if row % 3 == 0 and row != 8 and row != 0:
                line = QLabel(self)#lines are made using labels
                line.setGeometry(x, y, COLS * CELL_SIZE, 10)
                line.setStyleSheet("border: 10px solid black")

            for col in range(COLS):
                cell = self.cells[row][col]
                #setting int validator - allows only integers from 0-9
                cell.setValidator(QIntValidator(0, 9))
                
                #filling in numbers from the board
                cell.setText(str(self.board[row][col]))
                if cell.text() == "0":
                    cell.setText("")

                
                #alligns text in label to the center
                cell.setAlignment(QtCore.Qt.AlignCenter)
                cell.setFont(FONT1)

                #determines placement and size of label
                cell.setGeometry(x, y, CELL_SIZE, CELL_SIZE)
                x += CELL_SIZE

                cell.setStyleSheet("border: 1px solid black; background-color: white")

                #creating the seperating lines on the grid (Vertical)
                #this creates 2 seperate lines for each row
                if col % 3 == 2 and col != 8:
                    line = QLabel(self)
                    line.setGeometry(x, y, 10, CELL_SIZE)
                    line.setStyleSheet("border: 10px solid black")

            x = 0
            y += CELL_SIZE

    #Calls solve function
    def preSolve(self):

        #parsing the board into a 2D array before resetting to incorporate any edits made my the user
        self.board = self.parse()
        #resetting the board
        self.createGrid()

        #solver object
        #creating a copy of the initial board for the function to use
        solver = SudokuSolver(copy.deepcopy(self.board))
        #solving the board
        isSolution = solver.solve()
        #getting the solution board
        self.solutionBoard = solver.getSolution()
        self.illustratedBoard = solver.getIllustratedBoard()
        
        #only if there is a solution and the whole board is valid and not solved
        if isSolution and not solver.solved(self.board):        
            #illustrating the solution by showing the method of solving (backtracking)
            self.index = 0
            self.timer.start(50)#delay between each step
        
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
    
  
    #turns the board values into a 2D array of numbers representing the sudoku board
    def parse(self):
        board = []
        for x in self.cells:
            row = []
            for cell in x:
                if cell.text() != "":
                    row.append(int(cell.text()))
                else:
                    #0 represents an empty cell
                    row.append(0)
            
            board.append(row)
        
        return board
