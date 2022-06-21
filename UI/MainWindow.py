#AUTHOR: Smayan Nirantare

from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys

from StartUpUI import StartUpUI
from SudokuSolverUI import SudokuSolverUI
from SudokuEditUI import SudokuEditUI
from constants import *

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Sudoku Solver")

        self.setGeometry(100, 100, 750, 750)

        self.startStartUpUI()        
    
    def startStartUpUI(self):
        self.startWin = StartUpUI(self)
        self.setCentralWidget(self.startWin)
        self.show()
    
    def startSudokuSolverUI(self, board=None):
        self.solveWin = SudokuSolverUI(self, board)
        self.setCentralWidget(self.solveWin)
        self.show()
    
    def startSudokuEditUI(self, board=None):
        self.editWin = SudokuEditUI(self, board)
        self.setCentralWidget(self.editWin)
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
        
        #start the message box
        msg.exec_()

    #turns the board values into a 2D array of numbers representing the sudoku board
    def parse(self, cells):
        board = []
        for x in cells:
            row = []
            for cell in x:
                if cell.text() != "":
                    row.append(int(cell.text()))
                else:
                    #0 represents an empty cell
                    row.append(0)
            
            board.append(row)
        
        return board

    #creates sudoku board
    def createGrid(self, ui, cells, board):
        x = 0
        y = 0

        for row in range(ROWS):
            #creating the seperating lines on the grid (Horizontal)
            if row % 3 == 0 and row != 8 and row != 0:
                line = QLabel(ui)#lines are made using labels
                line.setGeometry(x, y, COLS * CELL_SIZE, 10)
                line.setStyleSheet("border: 10px solid black")

            for col in range(COLS):
                cell = cells[row][col]
                #setting int validator - allows only integers from 0-9
                cell.setValidator(QIntValidator(0, 9))

                #disable editing only if the ui type is of solverUI
                if str(type(ui)) == "<class 'SudokuSolverUI.SudokuSolverUI'>":
                    cell.setReadOnly(True)
                else:
                    cell.setReadOnly(False)
                
                #filling in numbers from the board
                cell.setText(str(board[row][col]))
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
                    line = QLabel(ui)
                    line.setGeometry(x, y, 10, CELL_SIZE)
                    line.setStyleSheet("border: 10px solid black")

            x = 0
            y += CELL_SIZE

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()