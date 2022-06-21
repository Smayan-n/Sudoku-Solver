#sudoku solver using a recursive backtracking algorithm

class SudokuSolver:
    def __init__(self, board):
        self.board = board

        #for illustration
        self.illustratedBoard = []

    def getSolution(self):
        return self.board

    def getIllustratedBoard(self):
        return self.illustratedBoard

    #main solve function (recursive)
    def solve(self):

        #if no empty cells, the board is solved
        #BASE CASE
        if not self.getEmpty():
            return True
        else:
            #if not solved, get the empty cell
            row, col = self.getEmpty()
        
        #try pluggin in values 1-9 in the empty cell until one is valid
        #RECURSIVE CASE
        for i in range(1, 10):
            if self.isValid(i, row, col):
                #if the value is valid, it is set to the empty cell
                self.board[row][col] = i
                self.illustratedBoard.append((i, row, col))

                #backtracking:
                #if a solution is found, end the program
                if self.solve():
                    return True
                #if no solution is found, bactrack to the previous cell and set it to empty again
                #check for new values than may be valid
                else:
                    self.board[row][col] = 0       

        #return false if the all values tested are invalid - no solution
        return False

    #checks if value in a particular row, col is valid for that col, row and subgrid
    def isValid(self, value, row, col):
        
        #checking the row
        for i in range(9):
            if self.board[row][i] == value and col != i:
                return False
        
        #checking the column
        for i in range(9):
            if self.board[i][col] == value and row != i:
                return False

        #checking the subgrid
        #integer division to calculate the subgrid row and col
        subgrid_row = row // 3 
        subgrid_col = col // 3
        
        #using these values to create a smaller 3x3 2D array to loop through to check if the value is valid
        for i in range(subgrid_row * 3, subgrid_row * 3 + 3):
            for j in range(subgrid_col * 3, subgrid_col * 3 + 3):
                if self.board[i][j] == value and (row, col) != (i, j):
                    return False

        #else its valid so return true
        return True

    #returns (row, col) of empty cell on the board
    def getEmpty(self):

        for row in range(9):
            for col in range(9):
                if self.board[row][col] == 0:
                    return row, col

        #return False if there are no empty cells left
        return False

    #check if whole board is valid
    def boardIsValid(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] != 0:
                    if not self.isValid(self.board[i][j], i, j):
                        return False
        return True
    
    #returns true if the board is solved
    @staticmethod
    def solved(board):
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    return False

        return True


