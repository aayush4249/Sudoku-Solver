# Sudoku-Solver

A sudoku solver I made that builds a constraint satisfaction problem and then implements the AC3 algorithm to solve the puzzle. To implement the CSP I used a list to hold all variables on the sudoku board. I used a grid system and so each cell has an index ranging from A1 to I8. Additionally I stored the data in a dictionary for easy retrieval when implementing AC3. Note that this algorithm only solves valid sudoku puzzles.

The program takes input in one line, empty slots are represented as 0's.

Ex: 000400190030000860007083500000008600805100000020000350081040000000070000040250000

This is considered a valid puzzle so the program will correctly solve the puzzle and output:

![Example Of Valid Solved Puzzle](https://github.com/aayush4249/Sudoku-Solver/blob/master/Valid.jpg)



In the case of an invalid puzzle the program will let the user know the puzzle is not valid and hence cannot be solved:

![Example of Unsolveable Invalid Puzzle](https://github.com/aayush4249/Sudoku-Solver/blob/master/Invalid.jpg)

