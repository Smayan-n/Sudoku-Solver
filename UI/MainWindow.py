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
            for line in lines:
                #splits the line into a list of strings
                board.append(list(line))

            #converting the strings to ints in array
            board = [[int(x) for x in row] for row in board]

            self.startSudokuSolverUI(board)
            
        except:
            pass
    
    #saves board in a file
    def saveBoard(self, board):
        try:
            file_dialog = QFileDialog()
            savePath = file_dialog.getSaveFileName(self, "Save Maze", "", "Text files (*.txt)")[0]

            #convert array into string of numbers
            string = ""
            for row in board:
                for val in row:
                    string += str(val)
                
                string += "\n"

            print(string)
            with open(savePath, "w") as f:
                f.write(string)
            
        except:
            pass

    #warning message function
    def showWarning(self, warning):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
  
        # setting Message box window title
        msg.setWindowTitle("Warning")
        
        # setting message for Message Box
        msg.setText(warning)
        
        # declaring buttons on Message Box
        msg.setStandardButtons(QMessageBox.Ok)
        
        # start the app
        msg.exec_()


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()