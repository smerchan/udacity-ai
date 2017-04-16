# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: If two boxes within same row, column, or square can take same pair of values;
   Constraint these pair of values to be assigned to one of the boxes in the pair.
   Using constraint propogation, eliminate these values from other
   peer rows, columns or grid boxes for the pair. This helps in reducing the 
   possible values in other peer boxes. Using naked twin constraint, 
   we have eliminated choices for other boxes. Use the search algorithm again 
   to solve which box within the naked twins pair should be assigned 
   a particular value from the possible pair of values. Repeat the 
   Naked twins rule to and recursive search to find a solution.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: First check if any box in the grid can take only single value. 
   Use constraint propogation to eliminate possible solution and iterate to 
   solve the problem using following steps 
   1. Assign the boxes with single value. 
   2. Eliminate the newly assigned value to a box from its peer row, column and grid boxes
   3. Next check again if any boxes have single value. If so assign the box with single value
   4. Iterate through step 2 - Step 3 till no change in value is detected 
   5. Next check for boxes with least number of options. 
   6. Search for a solution by selecting one value from the possible value for the box with 
      with least choices. 
   7. Iterate through steps 1 - 6 till solution is found

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solution.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Submission
Before submitting your solution to a reviewer, you are required to submit your project to Udacity's Project Assistant, which will provide some initial feedback.  

The setup is simple.  If you have not installed the client tool already, then you may do so with the command `pip install udacity-pa`.  

To submit your code to the project assistant, run `udacity submit` from within the top-level directory of this project.  You will be prompted for a username and password.  If you login using google or facebook, visit [this link](https://project-assistant.udacity.com/auth_tokens/jwt_login for alternate login instructions.

This process will create a zipfile in your top-level directory named sudoku-<id>.zip.  This is the file that you should submit to the Udacity reviews system.

