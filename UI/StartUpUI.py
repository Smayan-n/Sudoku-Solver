
from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from constants import *

#UI that is displayed at the start of the program
class StartUpUI(QWidget):
    def __init__(self, mainWin=None):
        super(StartUpUI, self).__init__(mainWin)

        self.mainWin = mainWin
        self.mainWin.setFixedSize(800, 750)

        self.initUI()

    def initUI(self):

        #main vertical layout of the start screen
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

        #labels
        info_lbl = QLabel("Welcome to the Sudoku Solver!")
        info_lbl.wordWrap()
        info_lbl.setFont(FONT2)
        info_lbl.setAlignment(QtCore.Qt.AlignCenter)

        maze_lbl = QLabel("Choose an action")
        maze_lbl.setFont(FONT2)
        maze_lbl.setAlignment(QtCore.Qt.AlignCenter)

        #two buttons that let user choose to createMaze a maze or load a maze
        self.loadBtn = QPushButton("Load sudoku", self)
        self.loadBtn.setFont(FONT2)
        self.loadBtn.setFixedHeight(150)
        self.createBtn = QPushButton("Create new sudoku", self)
        self.createBtn.setFont(FONT2)
        self.createBtn.setFixedHeight(150)

        self.layout.addWidget(info_lbl)
        self.layout.addWidget(maze_lbl)
        self.layout.addWidget(self.loadBtn)
        self.layout.addWidget(self.createBtn)

       