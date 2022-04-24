#AUTHOR: Smayan Nirantare

from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import time
from sudoku_solver import SudokuSolver
from constants import *

class SudokuSolverUI(QWidget):
    def __init__(self, mainWin=None, board=None):
        super(SudokuSolverUI, self).__init__()

        self.mainWin = mainWin
        self.mainWin.setWindowTitle("Sudoku Solver")
        #size of window
        self.screenWidth = COLS * CELL_SIZE
        self.screenHeight = ROWS * CELL_SIZE + RELIEF


        #illustrating the solving of the board
        self.illustratedSolution = []
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.illustrateBoard)


        #if board is true, load board from file
        if board is not None:
            self.board = board
        #else create new blank board
        else:
            self.board = [[0 for num in range(ROWS)] for j in range(COLS)]

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
                line = QLabel(self)
                line.setGeometry(x, y, COLS * CELL_SIZE, 10)
                line.setStyleSheet("border: 10px solid black")

            for col in range(COLS):
                cell = self.cells[row][col]
                
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

    def preSolve(self):

        #resetting the board
        self.createGrid()
        
        #solving the board
        print(self.board)
        #returns a solved board or false if there is not solution
        self.solutionBoard = self.solve(self.board)
        print(self.solutionBoard)

        #only if there is a solution
        if self.solutionBoard:
            #illustrating the solution by showing the method of solving (backtracking)
            self.index = 0
            self.timer.start(10)

    #loop function
    def illustrateBoard(self):
        #getting each valid number tries for teh row, col
        num, row, col = self.illustratedSolution[self.index]

        #color: green is final number, red indicates invalid number
        if (self.solutionBoard[row][col] == num):
            color = GREEN
        else:
            color = RED

        self.cells[row][col].setStyleSheet("border: 1px solid black; background-color: white; color: " + color)
        self.cells[row][col].setText(str(num))

        #stopping the loop function if the end of the list is reached
        self.index += 1
        if self.index == len(self.illustratedSolution):
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

    
    #main solve function (recursive)
    def solve(self, board):
        #if no empty cells, the board is solved
        #BASE CASE
        if not self.getEmpty(board):
            return True
        else:
            #if not solved, get the empty cell
            row, col = self.getEmpty(board)
        
        #try pluggin in values 1-9 in the empty cell until one is valid
        #RECURSIVE CASE
        for num in range(1, 10):
            if self.isValid(board, num, row, col):
                #if the value is valid, it is set to the empty cell
                board[row][col] = num
                self.illustratedSolution.append((num, row, col))

                #backtracking:
                #if a solution is found, end the program
                if self.solve(board):
                    return True
                #if no solution is found, bactrack to the previous cell and set it to empty again
                #check for new values than may be valid
                else:
                    board[row][col] = 0

        #return false if the all values tested are invalid
        return False


    #checks of value in a particular row, col is valid fro theat col, row and subgrid
    def isValid(self, board, value, row, col):
        
        #checking the row
        for num in range(9):
            if board[row][num] == value and board[row][col] != value:
                return False
        
        #checking the column
        for num in range(9):
            if board[num][col] == value and board[row][col] != value:
                return False

        #checking the subgrid
        #integer division to calculate the subgrid row and col
        subgrid_row = row // 3 
        subgrid_col = col // 3
        
        #using these values to create a smaller 3x3 2D array to loop through to check if the value is valid
        for num in range(subgrid_row * 3, subgrid_row * 3 + 3):
            for j in range(subgrid_col * 3, subgrid_col * 3 + 3):
                if board[num][j] == value and board[row][col] != value:
                    return False

        #else its valid so return true
        return True

    #returns (row, col) of empty cell on the board
    def getEmpty(self, board):

        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    return row, col

        #retursn False if there are no empty cells left
        return False




