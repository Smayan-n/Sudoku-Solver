#sudoku solver using a recursive backtracking algorithm

class SudokuSolver:
    def __init__(self, board):
        self.board = board

    def getSolution(self):
        return self.board

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

                #backtracking:
                #if a solution is found, end the program
                if self.solve():
                    return True
                #if no solution is found, bactrack to the previous cell and set it to empty again
                #check for new values than may be valid
                else:
                    self.board[row][col] = 0
        

        #return false if the all values tested are invalid
        return False


    #checks of value in a particular row, col is valid fro theat col, row and subgrid
    def isValid(self, value, row, col):
        
        #checking the row
        for i in range(9):
            if self.board[row][i] == value and self.board[row][col] != value:
                return False
        
        #checking the column
        for i in range(9):
            if self.board[i][col] == value and self.board[row][col] != value:
                return False

        #checking the subgrid
        #integer division to calculate the subgrid row and col
        subgrid_row = row // 3 
        subgrid_col = col // 3
        
        #using these values to create a smaller 3x3 2D array to loop through to check if the value is valid
        for i in range(subgrid_row * 3, subgrid_row * 3 + 3):
            for j in range(subgrid_col * 3, subgrid_col * 3 + 3):
                if self.board[i][j] == value and self.board[row][col] != value:
                    return False

        #else its valid so return true
        return True

    #returns (row, col) of empty cell on the board
    def getEmpty(self):

        for row in range(9):
            for col in range(9):
                if self.board[row][col] == 0:
                    return row, col

        #retursn False if there are no empty cells left
        return False

    #prints board in a readable format
    def printBoard(self):

        for i in range(9):
            if i % 3 == 0 and i != 0:
                print("---------------------")

            for j in range(9):
                print(self.board[i][j], end = " ")
                
                #printing vertical lines every 3 columns
                if j % 3 == 2 and j != 8:
                    print("|", end = " ")

            print()

def main():

    #0 == empty cell
    board = [
            [7,8,0,4,0,0,1,2,0],
            [6,0,0,0,7,5,0,0,9],
            [0,0,0,6,0,1,0,7,8],
            [0,0,7,0,4,0,2,6,0],
            [0,0,1,0,5,0,9,3,0],
            [9,0,4,0,6,0,0,0,5],
            [0,7,0,3,0,0,0,1,2],
            [1,2,0,0,0,7,4,0,0],
            [0,4,9,2,0,6,0,0,7]
            ]

    sudoku_solver = SudokuSolver(board)

    sudoku_solver.printBoard()
    #attempts to solve the board and returns true if solution is found, false otherwise
    solution = sudoku_solver.solve()
    print(solution)
    sudoku_solver.printBoard()

if __name__ == '__main__':
    main()