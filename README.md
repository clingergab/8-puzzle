# 8-puzzle
An 8-puzzle solver  
The N-puzzle game consists of a board holding N = m^2 − 1 distinct movable tiles, plus one empty space. There is one tile for each number in the set {0, 1,..., m2 − 1}. In this assignment, we will represent the blank space with the number 0 and focus on the m = 3 case (8-puzzle).

## Goal:
In this combinatorial search problem, the aim is to get from any initial board state to the configuration with all tiles arranged in ascending order {0, 1,..., m^2 − 1}, the goal state. The search space is the set of all possible states reachable from the initial state. Each move consists of swapping the empty space with a component in one of the four directions {‘Up’, ‘Down’, ‘Left’, ‘Right’}. Give each move a cost of one. Thus, the total cost of a path will be equal to the number of moves made.

### Implementation:
bfs (Breadth-First Search)  
dfs (Depth-First Search)  
ast (A-Star Search)  

### To execute:
  **run**: pyhton3 puzzle.py <search_type> <input>  
  e.g. ```$ python3 puzzle.py bfs 0,8,7,6,5,4,3,2,1```
