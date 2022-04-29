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
    
    stack_nodes = Stack()                   #khoi tao stack cac node
    start_node = problem.getStartState()    #khoi tao node dau tien
    if problem.isGoalState(start_node): #neu vi tri bat dau la dich den thi tra ve list trong
        return []
    visited_nodes = {}                            #vi tri da luu
    step_cost = 0                          #chi phi
    actions = []                            #hanh dong
    stack_nodes.push((start_node,actions,step_cost))
    while True:
        current_node = stack_nodes.pop() 

        if problem.isGoalState(current_node[0]):    # neu la diem ket thuc thi tra ve hanh dong 
            return current_node[1]
        
        if current_node[0] not in visited_nodes:          #neu node chua duoc di den thi danh dau la 1
            visited_nodes[current_node[0]]  = 1
            for next_node,action,cost in problem.getSuccessors(current_node[0]):
                if  next_node not in visited_nodes:       #neu node tiep theo chua co trong stack thi them vao
                    stack_nodes.push((next_node,current_node[1]+[action],current_node[2]+cost))
        
        if stack_nodes.isEmpty():                   #neu stack trong thi thoat vong lap
            break

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    queue_nodes = Queue()
    start_node = problem.getStartState()
    if problem.isGoalState(start_node):
        return []
    visited_nodes = [] 
    actions = []   
    step_cost = 0
    queue_nodes.push((start_node,actions,step_cost))
    while(True):  
        xy,actions,cost = queue_nodes.pop() 
        visited_nodes.append(xy)   
        if problem.isGoalState(xy):
            return actions
        succ = problem.getSuccessors(xy) # tra ve (next_node,next_action,next_step_cost)
        if succ:
            for item in succ:
                if item[0] not in visited_nodes and item[0] not in (state[0] for state in queue_nodes.list):
                    queue_nodes.push((item[0],actions+[item[1]],cost+item[2]))
        if queue_nodes.isEmpty():
            break
   
def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    queue_nodes = PriorityQueue()
    start_node = problem.getStartState()
    visited_nodes = [] 
    actions = [] 
    step_cost =0
    if problem.isGoalState(start_node):
        return []                   
    queue_nodes.push((start_node,actions),step_cost)

    while(True):
        
        current_node,actions = queue_nodes.pop() 
        visited_nodes.append(current_node)

        if problem.isGoalState(current_node):
            return actions

        succ = problem.getSuccessors(current_node)
        if succ:
            for item in succ:
                if item[0] not in visited_nodes : # neu node chua duoc di qua
                    if (item[0] not in (state[2][0] for state in queue_nodes.heap)): #neu node khong trong trang thai da luu
                        cost = problem.getCostOfActions(actions + [item[1]])
                        queue_nodes.push((item[0],actions + [item[1]]),cost)

                    else:
                        for state in queue_nodes.heap:
                            if state[2][0] == item[0]:
                                prev_cost = problem.getCostOfActions(state[2][1])
                        next_cost = problem.getCostOfActions(actions + [item[1]])
                        if prev_cost > next_cost:
                            queue_nodes.update((item[0],actions + [item[1]]),next_cost)
        if queue_nodes.isEmpty():
            return []
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

 
    queue_nodes = MyPriorityQueueWithFunction(problem,f)
    start_node = problem.getStartState()
    actions = [] 
    visited_node = [] 

    if problem.isGoalState(start_node):
        return []

    queue_nodes.push((start_node,actions),heuristic)

    while(True):
        if queue_nodes.isEmpty():
            return []
        current_node,actions = queue_nodes.pop() 

        if current_node in visited_node:
            continue

        visited_node.append(current_node)

        if problem.isGoalState(current_node):
            return actions

        succ = problem.getSuccessors(current_node)

        if succ:
            for item in succ:
                if item[0] not in visited_node:
                    
                    queue_nodes.push((item[0],actions + [item[1]]),heuristic)


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch