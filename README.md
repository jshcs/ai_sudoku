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

The three fundamental components of a Constraint Satisfaction Problem(CSP) are:
* Variables
* Constraint relationships between the variables
* Domain of the variables

In the case of Sudoku, every square is treated as a variable. Note that the terms square and variable will be used interchangeably in this text, and they shall hold the same meaning throughout. For understanding how to convert it to a CSP, it doesn't matter whether the square is empty or not. Every square(or variable) is connected to other squares(or variables) by constraint relationships. Consider the following example:
```
  1 2 3 4 5 6 7 8 9
  _________________
1|A x x x x x x x x
2|x x x
3|x x x
4|x
5|x
6|x
7|x
8|x
9|x
```

Square **A** is connected by a constraint relationship which each square denoted by **x**. These include all the squares in the same *row* as **A**, all the squares in the same *column* as **A**, and all the squares in the same *3*\**3 sub-grid* which contains **A**. The constraint relationship between **A** and every square **x** is drawn from the rules of Sudoku. To understand how these constraint relationships are drawn, the understanding of domain is necessary.

Informally, the domain of a variable in a CSP is a list of all the values that the variable can have according to the rules of the game. Since every square can take any number from 1 to 9, the domain of every square(or variable) is assumed to be [1,2,3,4,5,6,7,8,9]. Here, we are not yet considering the different constraints between the variables which will reduce the size of the domain of each variable, since the square would not be able to take some values from 1 to 9 due to the constraints implied on it by other squares.

I will also like to introduce an additional concept of _neighborhood_ to make things easier to explain. The neighborhood of a variable is a set of all the variables which are connected to the variable by a constraint relationship. So, this includes all the variables(or squares) which are in the same row, the variables that are in the same column and the variables that are in the same 3\*3 sub-grid as the variable in question. Note that the variables are not repeated in the list. For the above mentioned example, the neighborhood of **A** contains all the variables denoted by **x**.

So, what is this constraint relationship? Let's recap the basic rule of this game:
* No two squares in the same row, same column and the same 3\*3 sub-grid can have the same value. Alternatively, no square **x** in the neighborhood of a particular square **A** can have the same value that **A** has.

Thus, _for every value in the domain of **A**, there has to be some value in the domains of each of the variables in its neighborhood such that the above rule is satisfied_. And remember, this is a two-way street! Consider a situation(hypothetical!) in which a variable **A** has only one neighbor **B**. Let's assume that the domain of **A** is [1,2] and that of **B** is [2]. To satisfy the above mentioned constraint, we need to check that the constraint relation is satisfied for each of the values in the domain of **A** and then for each value in the domain of **B**.
* Assume that **A** takes the value 1. Since **B** has the value 2, the constraint rule is not violated.
* Now assume that **A** takes the value 2. Now, **B** also has the value 2, and so the constraint rule is violated as two variables in the neighborhood of each cannot take the same value. And so, 2 is not a valid value for **A**.

> _For every value in the domain of **A**, there has to be **some** value in the domains of each of the variables in its neighborhood such that the above rule is satisfied_.

* Since the constraint relationship is a two-way street, each value in the domain of **B** must also satisfy the constraint relationship. And since **B** has only one value in its domain, we need to check only for 2. Recalling the constraint relationship, the rule is not violated if **A** takes 1. And thus, 2 is a valid value for **B**.

How to use this rule and the knowledge of the domain of the variables to our advantage? Assume the following hypothetical scenario:

```
  1 2 3 4 5 6 7 8 9
  _________________
1|A x x 4 x x 9 x x
2|7 x x
3|x 1 x
4|x
5|x
6|3
7|x
8|x
9|x
```

Ideally, the domain of **A** should be [1,2,3,4,5,6,7,8,9]. But since (1,4)=4, (1,7)=7, (3,2)=1, (2,1)=7 and (6,1)=3, and these lie in the neighborhood of **A**, and also as we need to select a value for **A** that does not conflict with the rule mentioned above, **A** cannot take either of the following values [1,3,4,7,9]. Thus, given this knowledge about the values in the neighborhood of **A**, the domain of **A** effectively reduces to [2,5,6,8]. Note that (1,4) denotes the value in the 4<sup>th</sup> column of the 1<sup>st</sup> row, and likewise for others.

_Hence, by converting the problem to a CSP and using the knowledge of the domains of the variables in the neighborhood of a particular variable, we can reduce the size of the domain of that variable_.

This approach is used to reduce the size of the domains of all the empty squares in the puzzle. Although, just a naive implementation of this _domain reduction_ approach may not solve the puzzle entirely, search methods like Backtracking can be used to find the solution for the puzzle. The search algorithms become tractable for solving a **majority** of the puzzles since we significantly reduce the size of the search space by using the constraint relationships.

## Further improvements in the efficiency of the algorithm
Unfortunately, some puzzles are tough nuts to crack!! How to use additional knowledge to make the above mentioned _domain-reduction->search_ approach more tractable for solving **almost** all the puzzles?

* __Minimum Remaining Values(MRV) heuristic__ - Firstly, what is a heuristic? Informally, assume that you are using an algorithm to perform some task. In this case, a heuristic is a domain specific information which makes the algorithm more efficient. In the domain-reduction->search approach(_from now on, I will use the term search to refer to the domain-reduction->search approach discussed in the earlier section, and not the naive search algorithm!_), the values are assigned to the variables one variable at a time. So, once a value is assigned to a variable, we need to select another variable to which a value will be assigned. We can use the MRV heuristic to select this variable. The idea is to select a variable whose domain is the least in size. This helps to detect the failures soon and backtrack before going deeper in the search tree.

* __Forward Checking__ - Whenever a value is assigned to a variable, that value is removed from the domains of all the variables in the neighborhood of that variable. This has two advantages: Firstly, it further reduces the size of the search space since after every assignment to a variable, the size of the domains of other variables in the neighborhood of that variable are reduced. Secondly, this helps to detect the failures early and the algorithm can backtrack sooner.

* __Constraint Propagation__ - I like to think of Constraint Propagation as _Recursive Forward Checking!_ Consider the following scenario:

```
  1 2 3   4   5 6 7 8 9
  _____________________
1|4 x x [1,4] x x x x x
2|x x x   x   x x x x x
3|x x x   x
4|x     [1,2]
5|x
6|x
7|x
8|x
9|x
```

Assume that (1,1) was assigned the value 4. Using the idea of Forward Checking, the domain of (1,4) can be reduced to [1], since it cannot take the value 4 as (1,1) has already taken that value(_Neighborhood!_).

```
  1 2 3   4   5 6 7 8 9
  _____________________
1|4 x x   1   x x x x x
2|x x x   x   x x x x x
3|x x x   x
4|x     [1,2]
5|x
6|x
7|x
8|x
9|x
```

But now the domain of (1,4) is reduced to 1, while that of (4,4) is [1,2]. Since (4,4)=1 won't satisfy the constraint relationship between (1,4) and (4,4)(_Neighborhood!_), the domain of (4,4) can be reduced to [2].

```
  1 2 3 4 5 6 7 8 9
  _________________
1|4 x x 1 x x x x x
2|x x x x x x x x x
3|x x x x
4|x     2
5|x
6|x
7|x
8|x
9|x
```

Thus, instead of just reducing the domain of just (1,4) after assigning the value to (1,1) as implied by Forward Checking, we can also reduce the domain of (4,4) which is in the neighborhood of (1,4) and then recursively reduce the domains of all the neighbors of (4,4) and so on. This idea of recursively reducing the domains after each assignment operation significantly reduces the size of the search space and the _search_ algorithm can reach the solution state in lesser time!

So, let us go back to the Sudoku puzzle we discussed earlier:

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

Finding the solution using just naive Backtracking would have been impossible! But, using the approaches discussed above, the algorithm solved this puzzle in **less than 2 seconds!!**

```
[4] [1] [7] [3] [6] [9] [8] [2] [5]
[6] [3] [2] [1] [5] [8] [9] [4] [7]
[9] [5] [8] [7] [2] [4] [3] [1] [6]
[8] [2] [5] [4] [3] [7] [1] [6] [9]
[7] [9] [1] [5] [8] [6] [4] [3] [2]
[3] [4] [6] [9] [1] [2] [7] [5] [8]
[2] [8] [9] [6] [4] [3] [5] [7] [1]
[5] [7] [3] [2] [9] [1] [6] [8] [4]
[1] [6] [4] [8] [7] [5] [2] [9] [3]

Duration(seconds): 1.89293384552
```



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

* __Pass the puzzle as a string while running the script as follows__:

```
$ python sudokusolver.py r '4 0 0 0 0 0 8 0 5 0 3 0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 0 2 0 0 0 0 0 6 0 0 0 0 0 8 0 4 0 0 0 0 0 0 1 0 0 0 0 0 0 0 6 0 3 0 7 0 5 0 0 2 0 0 0 0 0 1 0 4 0 0 0 0 0 0'
```

## References:
1. Russell and Norvig. _Artificial Intelligence: A Modern Approach, 2<sup>nd</sup> edition_.
