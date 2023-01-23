#AUTHOR: Smayan Nirantare

from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from constants import *

class SudokuEditUI(QWidget):
    def __init__(self, mainWin=None, board=None):
        super(SudokuEditUI, self).__init__()

        self.mainWin = mainWin
        self.mainWin.setWindowTitle("Sudoku Solver")
        #size of window
        self.screenWidth = COLS * CELL_SIZE
        self.screenHeight = ROWS * CELL_SIZE + RELIEF

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
        self.solveButton = QPushButton("Finish Edit", self)
        self.solveButton.setGeometry(CELL_SIZE*3, (self.screenHeight - RELIEF)+10, CELL_SIZE*3, RELIEF-20)
        self.solveButton.setStyleSheet("background-color: GREEN; color: white")
        self.solveButton.setFont(FONT2)
        self.solveButton.clicked.connect(lambda: self.mainWin.startSudokuSolverUI(self.mainWin.parse(self.cells)))

        #main menu button
        mainMenuButton = QPushButton("New", self)
        mainMenuButton.setGeometry(CELL_SIZE//2, (self.screenHeight - RELIEF)+10, CELL_SIZE*2, RELIEF-20)
        mainMenuButton.setStyleSheet("background-color: ORANGE; color: white")
        mainMenuButton.setFont(FONT2)
        mainMenuButton.clicked.connect(self.mainWin.startStartUpUI)

        #save menu button
        saveButton = QPushButton("Save", self)
        saveButton.setGeometry(CELL_SIZE*6 + CELL_SIZE//2, (self.screenHeight - RELIEF)+10, CELL_SIZE*2, RELIEF-20)
        saveButton.setStyleSheet("background-color: PURPLE; color: white")
        saveButton.setFont(FONT2)
        saveButton.clicked.connect(lambda: self.mainWin.saveBoard(self.mainWin.parse(self.cells)))

        self.mainWin.createGrid(self, self.cells, self.board)