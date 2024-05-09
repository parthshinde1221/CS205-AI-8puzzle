# import copy as cp

# class Node:
#     def __init__(self):
#         pass
#     def get_location(self):
#         pass
#     def move_up(self):
#         pass
#     def move_down(self):
#         pass
#     def move_right(self):
#         pass
#     def move_left(self):
#         pass


# class Problem:
#     def __init__(self,init_state,goal_state):
#         self.init_state = init_state
#         self.goal_state = goal_state




# def create_board(n):
#     x = []
#     for i in range(n):
#         y = []
#         for j in range(n):
#             y.append(input('Enter value:\n'))
#         x.append(y)
#     return x


import heapq
from random import randrange
from time import time


# FRONTIER.append(2)
# GOAL_STATE = '123456780'

class Node:
    '''
    The Node here is the board state itself it represented in a string format
    '''
    def __init__(self, state, parent=None, action=None, path_cost=0):
        # state of the Node i.e current state of the board
        self.state = state 
        # parent of the particular board i.e the previous state of the board(previous Node in the tree)
        self.parent = parent
        # action that can happen on the board according to its current state
        self.action = action
        # cost of the board to arrive at its current state
        self.path_cost = path_cost

    def __lt__(self, other):
        return self.path_cost < other.path_cost


# swap function to swap the indexes of the '0' or blank tile with the nearby tiles
def swap(state, x1, y1, x2, y2, n):
    state_list = list(state)
    index1, index2 = x1 * n + y1, x2 * n + y2
    state_list[index1], state_list[index2] = state_list[index2], state_list[index1]
    return ''.join(state_list)


# find the blank_tile i.e '0'
def find_blank(state, n):
    index = state.index('0')
    return index // n, index % n

def find_2D_index(state,tile,n):
    index = state.index(tile)
    return index // n, index % n

# find the possible moves that can be made by the blank tile in the current state of the board
def possible_moves(state, n):
    blank_x, blank_y = find_blank(state, n)
    moves = []
    directions = {
        'up': (-1, 0),
        'down': (1, 0),
        'left': (0, -1),
        'right': (0, 1)
    }
    for direction, (dx, dy) in directions.items():
        new_x, new_y = blank_x + dx, blank_y + dy
        if 0 <= new_x < n and 0 <= new_y < n:
            new_state = swap(state, blank_x, blank_y, new_x, new_y, n)
            moves.append((new_state, direction))
    return moves

# To check if the goal state has reached
def goal_test(state, n):
    return state == ''.join(str(i) for i in range(1, n*n)) + '0'

# retrace the path taken to reach the goal state
def reconstruct_path(node):
    path = []
    while node:
        path.append(node.state)
        node = node.parent
    return path[::-1]

# heurstic function used to take an informed decision
def heursitic_cost(curr_state,goal_state,n,distance_metric='UCS'):
    # print('')
    if distance_metric=='Manhattan':
        # print('Helloo')
        '''
        In this the heurstic h(x) is equal to the sum of all the Manhanttan distance calculations
        for each of the tile to reach the goal state.
        '''

        cost = 0
        for i in range(n*n):

            if curr_state[i]=='0':
                continue

            x_curr,y_curr = find_2D_index(curr_state,curr_state[i],n)
            x_goal,y_goal = find_2D_index(goal_state,curr_state[i],n)
            # print(x_curr,x_goal,y_curr,y_goal)
            cost += abs(x_curr -  x_goal) + abs(y_curr - y_goal)
        
        # print(cost)
        return cost
    
    elif distance_metric=='Misplaced_tile':
        '''
        In this heurstic the h(x) is the is the number of non-blank tiles not in 
        their goal position
        '''

        cost = 0
        for i in range(n*n):
            if curr_state[i] != '0' and curr_state[i] != goal_state[i]:
                cost += 1
        
        # print(cost)

        return cost
    else:
        '''
        UCS  --> Uniform Cost Search h(x)=0
        g(x) --> The cost of each step is defined as 1 (but its cumulative) 
                the cost will increase with the number of steps it takes to reach the node   
        '''
        # print('*')
        return 0

            

# general search function --> according to the function given in the  
class Searcher:
    def __init__(self):
        self.frontier = []
        self.visited = set()
        # self.result = ''
    
    # def general_search(self,initial_state,goal_state,n,distance_metric):
    #     initial_node = Node(initial_state)
    #     # frontier = []
    #     heapq.heappush(self.frontier, (initial_node.path_cost, initial_node))
    #     # visited = set()

    #     # goal_state = ''.join([i for i in range()])
        
    #     while self.frontier:
    #         current_cost, current_node = heapq.heappop(self.frontier)
    #         if goal_test(current_node.state, n):
    #             # print(f"No of nodes:{len(self.frontier)}")
    #             return reconstruct_path(current_node)

    #         self.visited.add(current_node.state)
    #         for state, action in possible_moves(current_node.state, n):
    #             if state not in self.visited:
    #                 child_node = Node(state, current_node, action, current_node.path_cost + 1 + heursitic_cost(current_node.state,goal_state,n,distance_metric=distance_metric))
    #                 heapq.heappush(self.frontier, (child_node.path_cost, child_node))
    #                 self.visited.add(state)

    def general_search(self, initial_state, goal_state, n, distance_metric):

        # MAKE-NODE(problem.INITIAL-STATE)
        initial_node = Node(initial_state)
        
        # nodes = MAKE-QUEUE(MAKE-NODE(problem.INITIAL-STATE))
        heapq.heappush(self.frontier, (initial_node.path_cost, initial_node)) # Priority queue used here
        
        # loop do
        while self.frontier:
            
            # node = REMOVE-FRONT(nodes)
            current_cost, current_node = heapq.heappop(self.frontier)
            
            # if problem.GOAL-TEST(node.STATE) succeeds then return node
            if goal_test(current_node.state, n):  # Check if the current node is the goal state
                return reconstruct_path(current_node)  # Retrace path to this node if it's the goal
            
            # nodes = QUEUEING-FUNCTION(nodes, EXPAND(node, problem.OPERATORS))
            self.visited.add(current_node.state)  # Mark this node as visited
            for state, action in possible_moves(current_node.state, n):  # EXPAND(node, problem.OPERATORS)
                if state not in self.visited:
                    # Calculate total cost and create a new child node
                    child_node = Node(state, current_node, action, current_node.path_cost + 1 + heursitic_cost(current_node.state, goal_state, n, distance_metric=distance_metric))
                    
                    if current_node.path_cost == child_node.path_cost:
                        continue

                    heapq.heappush(self.frontier, (child_node.path_cost, child_node))  # Queueing function based on cost
                    self.visited.add(state)

        
        # if EMPTY(nodes) then return "failure" 
        # as it would come out of the while loop as soon as nodes i.e frontier becomes 0
        return "failure"
        
        
    

    # print(f"No of nodes:{len(frontier)}")
    # print(f"No of nodes:{len(visited)}")

        # return "failure"


# print the retraced path of the solution
def print_path(path, n):
    for index,state in enumerate(path):
        print(f'Depth of tree solver-->{index}:Board state given below')
        print("\n".join(state[i:i+n] for i in range(0, len(state), n)).replace('0','_'))
        print()

# Main function
def main():
    n = int(input("Enter the puzzle size (e.g., 3 for 8-puzzle, 4 for 15-puzzle): "))
    eg_input = ''.join([str(i) for i in range(n*n)]).strip()
    goal_state = ''.join([str(i) for i in range(1,n*n)]).strip() + '0'
    distance_metric_dict = {
                            '1':'UCS',
                            '2':'Manhattan',
                            '3':'Misplaced_tile'
                            }
    initial_state = input(f"Enter the initial state as a string in a row-major format (e.g., '{eg_input}' for {n}x{n} puzzle): ")
    cost_function_used = input(f"Enter heurstic cost function to be used:- \n 1:UCS  \n 2:Manhattan \n 3:Misplaced Tile\n")

    print('\nThis is your intial state of the board\n')
    print("\n".join(initial_state[i:i+n] for i in range(0, len(initial_state), n)).replace('0','_'))
    print('\nThis is your goal state of the board\n')
    print("\n".join(goal_state[i:i+n] for i in range(0, len(goal_state), n)).replace('0','_'))


    if len(initial_state) != n*n or set(initial_state) != set(str(i) for i in range(n*n)):
        print("Invalid state. Please ensure you enter exactly n*n characters with unique digits from 0 to (n*n)-1.")
        return

    print('\n---SEARCHER INTIALISED---\n')
    # print("FINDING PATH")
    # while True:
    #     print('.')
    search_obj = Searcher()
    start_time = time()
    path = search_obj.general_search(initial_state,goal_state,n,distance_metric_dict[cost_function_used])
    end_time = time()

    if path == "failure":
        print("\nNo solution found.")
    else:
        print("\nSolution found:")
        print_path(path, n)

    print(f'TIME TAKEN FOR EXCUETION:- {(end_time-start_time) * 1000} ms')

if __name__ == "__main__":
    main()


    

