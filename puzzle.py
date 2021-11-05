
from __future__ import division
from __future__ import print_function

import sys
import math
import time
import queue as Q
import os
import resource
import heapq


#### SKELETON CODE ####
## The Class that Represents the Puzzle
class PuzzleState(object):
    """
        The PuzzleState stores a board configuration and implements
        movement instructions to generate valid children.
    """
    def __init__(self, config, n, parent=None, action="Initial", cost=0):
        """
        :param config->List : Represents the n*n board, for e.g. [0,1,2,3,4,5,6,7,8] represents the goal state.
        :param n->int : Size of the board
        :param parent->PuzzleState
        :param action->string
        :param cost->int
        """
        if n*n != len(config) or n < 2:
            raise Exception("The length of config is not correct!")
        if set(config) != set(range(n*n)):
            raise Exception("Config contains invalid/duplicate entries : ", config)

        self.n        = n
        self.cost     = cost
        self.parent   = parent
        self.action   = action
        self.config   = config
        self.children = []

        # Get the index and (row, col) of empty block
        self.blank_index = self.config.index(0)

        self.manhattan_priority_function = 0
        for i in range(0, len(self.config)):
            if i != self.config[i]:
                self.manhattan_priority_function += calculate_manhattan_dist(i, self.config[i], self.n)
        self.manhattan_priority_function


    def display(self):
        """ Display this Puzzle state as a n*n board """
        for i in range(self.n):
            print(self.config[3*i : 3*(i+1)])

    def move_up(self):
        """ 
        Moves the blank tile one row up.
        :return a PuzzleState with the new configuration
        """
        if self.blank_index < self.n:
            return None
        idx = self.blank_index
        config = self.config[:]

        config[idx] = self.config[idx - self.n]
        config[idx - self.n] = 0

        return PuzzleState(config, self.n, parent=self, action="Up", cost=self.cost + 1)
      
    def move_down(self):
        """
        Moves the blank tile one row down.
        :return a PuzzleState with the new configuration
        """
        if self.blank_index > self.n * (self.n - 1) - 1:
            return None
        
        idx = self.blank_index
        config = self.config[:]
        config[idx] = config[idx + self.n]
        config[idx + self.n] = 0

        return PuzzleState(config, self.n, parent=self, action="Down", cost=self.cost + 1)
      
    def move_left(self):
        """
        Moves the blank tile one column to the left.
        :return a PuzzleState with the new configuration
        """
        if self.blank_index % self.n == 0:
            return None

        idx = self.blank_index
        config = self.config[:]
        config[idx] = config[idx - 1]
        config[idx - 1] = 0

        return PuzzleState(config, self.n, parent=self, action="Left", cost=self.cost + 1)

    def move_right(self):
        """
        Moves the blank tile one column to the right.
        :return a PuzzleState with the new configuration
        """
        if self.blank_index % self.n == self.n - 1:
            return None

        idx = self.blank_index
        config = self.config[:]
        config[idx] = config[idx + 1]
        config[idx + 1] = 0

        return PuzzleState(config, self.n, parent=self, action="Right", cost=self.cost + 1)
      
    def expand(self):
        """ Generate the child nodes of this node """
        
        # Node has already been expanded
        if len(self.children) != 0:
            return self.children
        
        # Add child nodes in order of UDLR
        children = [
            self.move_up(),
            self.move_down(),
            self.move_left(),
            self.move_right()]

        # Compose self.children of all non-None children states
        self.children = [state for state in children if state is not None]
        return self.children

    

    def __lt__(self, other):
        return (self.manhattan_priority_function + self.cost) < (self.manhattan_priority_function + other.cost)


# Function that Writes to output.txt

def writeOutput(pathToGoal, costOfPath, nodesExpanded, searchDepth, maxDepth, runTime):
    with open("output.txt", "w") as f:
        f.write("path_to_goal " + str(pathToGoal) + "\n")
        f.write("cost_of_path: " + str(costOfPath) + "\n")
        f.write("nodes_expanded: " + str(nodesExpanded) + "\n")
        f.write("search_depth: " + str(searchDepth) + "\n")
        f.write("max_search_depth: " + str(maxDepth) + "\n")
        f.write("running_time: %.8f" %(runTime) + "\n")
        f.write("Max_ram_usage: %.8f" %(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024) + "\n")

def findPath(state):
    path = []
    while state.parent != None:
        path.append(state.action)
        state = state.parent
    
    return path[::-1]


class BfsFrontier:
    def __init__(self):
        self.queue = Q.Queue()
        self.dict = {}

    def enqueue(self, state):
        self.queue.put(state)
        self.dict[tuple(state.config)] = True

    def dequeue(self):
        if self.queue.empty():
            return None

        state = self.queue.get()
        del self.dict[tuple(state.config)]
        
        return state

    def isEmpty(self):
        return self.queue.empty()

def bfs_search(initial_state):
    """BFS search"""
    start_time  = time.time()
    frontier = BfsFrontier()
    frontier.enqueue(initial_state)
    explored = set()
    nodesExpanded = 0
    maxDepth = 0

    while not frontier.isEmpty():
        state = frontier.dequeue()
        explored.add(tuple(state.config))
        
        if test_goal(state):
            pathToGoal = findPath(state)
            costOfPath = searchDepth = state.cost
            writeOutput(pathToGoal, costOfPath, nodesExpanded, searchDepth, maxDepth, time.time() - start_time)
            return True
        nodesExpanded += 1
        for neighbor in state.expand():
            if tuple(neighbor.config) not in frontier.dict and tuple(neighbor.config) not in explored:
                frontier.enqueue(neighbor)
                if neighbor.cost > maxDepth:
                    maxDepth = neighbor.cost

    return False



class DfsFrontier:
    def __init__(self):
        self.stack = []
        self.dict = {}

    def isEmpty(self):
        return self.stack.count == 0

    def push(self, state):
        self.stack.append(state)
        self.dict[tuple(state.config)] = True

    def pop(self):
        if self.stack.count == 0:
            return None

        state = self.stack.pop()
        del self.dict[tuple(state.config)]
        return state


def dfs_search(initial_state):
    """DFS search"""
    start_time  = time.time()
    frontier = DfsFrontier()
    frontier.push(initial_state)
    explored = set()
    nodesExpanded = 0
    maxDepth = 0

    while not frontier.isEmpty():
        state = frontier.pop()
        explored.add(tuple(state.config))
        
        if test_goal(state):
            pathToGoal = findPath(state)
            costOfPath = searchDepth = state.cost
            writeOutput(pathToGoal, costOfPath, nodesExpanded, searchDepth, maxDepth, time.time() - start_time)
            return True
        nodesExpanded += 1
        for neighbor in state.expand()[::-1]:
            if tuple(neighbor.config) not in frontier.dict and tuple(neighbor.config) not in explored:
                frontier.push(neighbor)
                if neighbor.cost > maxDepth:
                    maxDepth = neighbor.cost

    return False
class ASFrontier:
    def __init__(self):
        self.heap = []
        self.dict = {}
        heapq.heapify(self.heap)

    def heappush(self, state):
        heapq.heappush(self.heap, state)
        self.dict[tuple(state.config)] = True

    def heappop(self):
        state = heapq.heappop(self.heap)
        del self.dict[tuple(state.config)]
        return state

    def isEmpty(self):
        return self.heap.count == 0


def A_star_search(initial_state):
    start_time  = time.time()
    frontier = ASFrontier()
    frontier.heappush(initial_state)
    explored = set()
    nodesExpanded = 0
    maxDepth = 0

    while not frontier.isEmpty():
        state = frontier.heappop()
        explored.add(tuple(state.config))
        
        if test_goal(state):
            pathToGoal = findPath(state)
            costOfPath = searchDepth = state.cost
            with open("output.txt", "w") as f:
                writeOutput(pathToGoal, costOfPath, nodesExpanded, searchDepth, maxDepth, time.time() - start_time)
            return True

        nodesExpanded += 1
        for neighbor in state.expand():
            if test_goal(neighbor):
                pathToGoal = findPath(neighbor)
                costOfPath = searchDepth = neighbor.cost
                writeOutput(pathToGoal, costOfPath, nodesExpanded, searchDepth, maxDepth, time.time() - start_time)
                return True
            elif tuple(neighbor.config) not in frontier.dict and tuple(neighbor.config) not in explored:
                frontier.heappush(neighbor)
                if neighbor.cost > maxDepth:
                    maxDepth = neighbor.cost

    return False


def calculate_total_cost(state):
    """calculate the total estimated cost of a state"""
    total_cost = state.manhattan_priority_function + state.cost
    return total_cost

def calculate_manhattan_dist(idx, value, n):
    """calculate the manhattan distance of a tile"""
    dist = abs(value // n - idx // n) + abs(value % n - idx % n)
    
    return dist


def test_goal(puzzle_state):
    #print(str(puzzle_state.config))
    #print(str(list(range(0, len(puzzle_state.config)))))
    """test the state is the goal state or not"""
    return puzzle_state.config == list(range(0, len(puzzle_state.config)))

# Main Function that reads in Input and Runs corresponding Algorithm
def main():
    search_mode = sys.argv[1].lower()
    begin_state = sys.argv[2].split(",")
    begin_state = list(map(int, begin_state))
    board_size  = int(math.sqrt(len(begin_state)))
    hard_state  = PuzzleState(begin_state, board_size)
    start_time  = time.time()
    if   search_mode == "bfs": bfs_search(hard_state)
    elif search_mode == "dfs": dfs_search(hard_state)
    elif search_mode == "ast": A_star_search(hard_state)
    else: 
        print("Enter valid command arguments !")
        
    end_time = time.time()
    print("Program completed in %.3f second(s)"%(end_time-start_time))

if __name__ == '__main__':
    main()
