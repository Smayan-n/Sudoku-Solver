#AUTHOR: Smayan Nirantare

from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys

from StartUpUI import StartUpUI
from SudokuSolverUI import SudokuSolverUI

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Sudoku Solver")

        self.setGeometry(100, 100, 750, 750)

        self.startStartUpUI()        
    
    def startStartUpUI(self):
        self.startWin = StartUpUI(self)
        self.setCentralWidget(self.startWin)
        self.startWin.loadBtn.clicked.connect(lambda: self.loadBoard())
        self.startWin.createBtn.clicked.connect(lambda: self.startSudokuSolverUI())
        self.show()
    
    def startSudokuSolverUI(self, board=None):
        self.solveWin = SudokuSolverUI(self, board)
        self.setCentralWidget(self.solveWin)
        self.show()
    

        #loads the board from the file and parses it into a 2D array
    def loadBoard(self):

        try:
            file_dialog = QFileDialog()
            boardFilePath = file_dialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt)")[0]

            with open(boardFilePath, "r") as f:
                contents = f.read()

            board = []
            #splits string into a list of strings representing each row
            lines = contents.splitlines()
            print(lines)
            for line in lines:
                #splits the line into a list of strings
                board.append(list(line))
                print(board)

            #converting the strings to ints in array
            board = [[int(x) for x in row] for row in board]

            self.startSudokuSolverUI(board)
            
        except:
            pass


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()