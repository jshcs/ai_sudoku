# ai_sudoku

## Introduction
The goal of this project is to develop a [Sudoku](https://en.wikipedia.org/wiki/Sudoku) solving AI agent. The Sudoku puzzles are in the form of a 9\*9 grid and the idea is to place all the numbers from 1 to 9 in such a way that all columns, all rows and all 3\*3 sub-grids contain a single instance of each of the 9 numbers. So, no two squares in the same column, in same row and in the same 3*3 sub-grid can have the same number. A partially solved puzzle is given and the objective is to fill the remaining squares in the grid with the appropriate numbers. Any valid Sudoku puzzle has a unique solution.

## Dependencies
* Python 2.7

## Methodology
Sudoku puzzles can be solved using naive Search-based algorithms. These algorithms search for the goal state, i.e the solution of the puzzle, by going through all the possible combinations of the numbers that can occupy the empty squares. This method may be feasible for easy puzzles, but is not at all good enough to solve tough problems. For example, consider the following puzzle (0 represents an empty square) taken from an [article](http://norvig.com/sudoku.html) written by Peter Norvig:

```
4 0 0|0 0 0|8 0 5
0 3 0|0 0 0|0 0 0
0 0 0|7 0 0|0 0 0
-----+-----+-----
0 2 0|0 0 0|0 6 0
0 0 0|0 8 0|4 0 0
0 0 0|0 1 0|0 0 0
-----+-----+-----
0 0 0|6 0 3|0 7 0
5 0 0|2 0 0|0 0 0
1 0 4|0 0 0|0 0 0
```
This is his comment on using a naive Search-based approach to solve this puzzle:
> First, we could try a brute force approach. Suppose we have a very efficient program that takes only one instruction to evaluate a position, and that we have access to the next-generation computing technology, let's say a 10GHz processor with 1024 cores, and let's say we could afford a million of them, and while we're shopping, let's say we also pick up a time machine and go back 13 billion years to the origin of the universe and start our program running. We can then [compute](http://www.google.com/search?&q=10+GHz+*+1024+*+1+million+*+13+billion+years+%2F+4.6e38+in+percent) that we'd be almost 1% done with this one puzzle by now.

So, using a brute force Search approach is out of question if we wish to develop an AI agent that can solve the maximum number of Sudoku puzzles.

Another alternative is to convert this problem into a [Constraint Satisfaction Problem](https://en.wikipedia.org/wiki/Constraint_satisfaction_problem), and use the constraint relationships to efficiently solve this problem.

## Converting to a Constraint Satisfaction Problem
_Yet to update_

## Running the script
Clone or download the project on your local machine. 
Assume you want to solve the following puzzle:
```
4 0 0|0 0 0|8 0 5
0 3 0|0 0 0|0 0 0
0 0 0|7 0 0|0 0 0
-----+-----+-----
0 2 0|0 0 0|0 6 0
0 0 0|0 8 0|4 0 0
0 0 0|0 1 0|0 0 0
-----+-----+-----
0 0 0|6 0 3|0 7 0
5 0 0|2 0 0|0 0 0
1 0 4|0 0 0|0 0 0
```
There are two ways to provide a Sudoku puzzle as an input and run the script on it:

* __Save the puzzle in a .txt file and pass the filename as an argument while running the script from the terminal__.

Save this puzzle in a .txt file, and let's name it test.txt and place it in the directory containing the sudokusolver.py script.
```
4 0 0 0 0 0 8 0 5 0 3 0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 0 2 0 0 0 0 0 6 0 0 0 0 0 8 0 4 0 0 0 0 0 0 1 0 0 0 0 0 0 0 6 0 3 0 7 0 5 0 0 2 0 0 0 0 0 1 0 4 0 0 0 0 0 0
```
Open the Terminal and navigate to the directory in which test.txt and sudokusolver.py are saved. Run the following command:
```
$ python sudokusolver.py f test.txt
```

* __Pass the puzzle as a string while running the script as follows:__
```
$ python sudokusolver.py r '4 0 0 0 0 0 8 0 5 0 3 0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 0 2 0 0 0 0 0 6 0 0 0 0 0 8 0 4 0 0 0 0 0 0 1 0 0 0 0 0 0 0 6 0 3 0 7 0 5 0 0 2 0 0 0 0 0 1 0 4 0 0 0 0 0 0'
```
