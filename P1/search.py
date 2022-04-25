# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
from util import Stack
from util import Queue
from util import PriorityQueue
class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()

def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    
    Coordinate = Stack()

    visited_list = [] 
    path = [] 

   
    if problem.isGoalState(problem.getStartState()):
        return []

    
    Coordinate.push((problem.getStartState(),[]))

    while(True):

        
        if Coordinate.isEmpty():
            return []

       
        xy,path = Coordinate.pop() 
        visited_list.append(xy)

        
        if problem.isGoalState(xy):
            return path

        
        succ = problem.getSuccessors(xy)

       
        if succ:
            for item in succ:
                if item[0] not in visited_list:
                    newPath = path + [item[1]] # Calculate new path
                    Coordinate.push((item[0],newPath))

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    
    coordinate = Queue()

    visited_list = [] 
    path = [] 

   
    if problem.isGoalState(problem.getStartState()):
        return []

   
    coordinate.push((problem.getStartState(),[]))

    while(True):

        
        if coordinate.isEmpty():
            return []

        
        xy,path = coordinate.pop() 
        visited_list.append(xy)

       
        if problem.isGoalState(xy):
            return path

        succ = problem.getSuccessors(xy)

       
        if succ:
            for item in succ:
                if item[0] not in visited_list and item[0] not in (state[0] for state in coordinate.list):
                    newPath = path + [item[1]] # Calculate new path
                    coordinate.push((item[0],newPath))

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

   
    coordinate = PriorityQueue()

    visited_list = [] 
    path = [] 

   
    if problem.isGoalState(problem.getStartState()):
        return []

                                         
    coordinate.push((problem.getStartState(),[]),0)

    while(True):

       
        if coordinate.isEmpty():
            return []

       
        xy,path = coordinate.pop() # Take position and path
        visited_list.append(xy)

    
        if problem.isGoalState(xy):
            return path

        
        succ = problem.getSuccessors(xy)

       
        if succ:
            for item in succ:
                if item[0] not in visited_list and (item[0] not in (state[2][0] for state in coordinate.heap)):
                    newPath = path + [item[1]]
                    pri = problem.getCostOfActions(newPath)

                    coordinate.push((item[0],newPath),pri)

                
                elif item[0] not in visited_list and (item[0] in (state[2][0] for state in coordinate.heap)):
                    for state in coordinate.heap:
                        if state[2][0] == item[0]:
                            oldPri = problem.getCostOfActions(state[2][1])

                    newPri = problem.getCostOfActions(path + [item[1]])

                    if oldPri > newPri:
                        newPath = path + [item[1]]
                        coordinate.update((item[0],newPath),newPri)

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


class MyPriorityQueueWithFunction(PriorityQueue):
    """
    Implements a priority queue with the same push/pop signature of the
    Queue and the Stack classes. This is designed for drop-in replacement for
    those two classes. The caller has to provide a priority function, which
    extracts each item's priority.
    """
    def  __init__(self, problem, priorityFunction):
        "priorityFunction (item) -> priority"
        self.priorityFunction = priorityFunction      # store the priority function
        PriorityQueue.__init__(self)        # super-class initializer
        self.problem = problem
    def push(self, item, heuristic):
        "Adds an item to the queue with priority from the priority function"
        PriorityQueue.push(self, item, self.priorityFunction(self.problem,item,heuristic))

# Calculate f(n) = g(n) + h(n) #
def f(problem,state,heuristic):

    return problem.getCostOfActions(state[1]) + heuristic(state[0],problem)

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    # queueXY: ((x,y),[path]) #
    queueXY = MyPriorityQueueWithFunction(problem,f)

    path = [] # Every state keeps it's path from the starting state
    visited = [] # Visited states


    # Check if initial state is goal state #
    if problem.isGoalState(problem.getStartState()):
        return []

    # Add initial state. Path is an empty list #
    element = (problem.getStartState(),[])

    queueXY.push(element,heuristic)

    while(True):

        # Terminate condition: can't find solution #
        if queueXY.isEmpty():
            return []

        # Get informations of current state #
        xy,path = queueXY.pop() # Take position and path

        # State is already been visited. A path with lower cost has previously
        # been found. Overpass this state
        if xy in visited:
            continue

        visited.append(xy)

        # Terminate condition: reach goal #
        if problem.isGoalState(xy):
            return path

        # Get successors of current state #
        succ = problem.getSuccessors(xy)

        # Add new states in queue and fix their path #
        if succ:
            for item in succ:
                if item[0] not in visited:

                    # Like previous algorithms: we should check in this point if successor
                    # is a goal state so as to follow lectures code

                    newPath = path + [item[1]] # Fix new path
                    element = (item[0],newPath)
                    queueXY.push(element,heuristic)


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch