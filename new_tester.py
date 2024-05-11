from Npuzzle import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import pandas as pd
# from time import time

# global variables
# Define test cases and other constants
GOAL_STATE = '123456780'
PUZZLE_SIZE = 3
TEST_CASES = {
    '123456780': GOAL_STATE,
    '123456078': GOAL_STATE,
    '136502478': GOAL_STATE,
    '136507482': GOAL_STATE,
    '167503482': GOAL_STATE,
    '712485630': GOAL_STATE,
    '072461358': GOAL_STATE,
}
HEURISTIC_METHODS = ['UCS', 'Manhattan', 'Misplaced_tile']

class TestCase:
    def __init__(self, init_state, goal_state, puzzle_size, heuristic_method='UCS'):
        self.heuristic_method = heuristic_method
        self.init_state = init_state
        self.goal_state = goal_state
        self.puzzle_size = puzzle_size
        self.depth_of_tree = 0
        self.nodes_visited_count = 0
        self.nodes_frontier_count = 0
        self.execution_time = 0
        self.result = ''

    def generate_results(self):
        search_obj = Searcher()
        start_time = time()
        path = search_obj.general_search(self.init_state, self.goal_state, self.puzzle_size, self.heuristic_method)
        end_time = time()

        if path == "failure":
            self.result = 'Failure'
            print("\nNo solution found.")
        else:
            self.result = 'Success'
            print("\nSolution found:")

        print(f'TIME TAKEN FOR SEARCH EXECUTION: {(end_time - start_time) * 1000} ms')    

        self.execution_time = (end_time - start_time) * 1000
        self.depth_of_tree = len(path) -1 
        self.nodes_frontier_count = len(search_obj.frontier)
        self.nodes_visited_count = len(search_obj.visited)

    def print_data(self):
        print(f'Data {self.init_state},{self.heuristic_method}==>{self.depth_of_tree},{self.nodes_visited_count},{self.nodes_frontier_count},{self.execution_time}')

class GraphGenerator:
    def __init__(self):
        self.test_case_objects = [TestCase(init_state, goal_state, PUZZLE_SIZE, method) for init_state, goal_state in TEST_CASES.items() for method in HEURISTIC_METHODS]
    
    def generate_graphs(self):
        for test_case_obj in self.test_case_objects:
            test_case_obj.generate_results()
            test_case_obj.print_data()

        with PdfPages('n_puzzle_analysis.pdf') as pdf:
            # Prepare data
            data = {method: {'execution_times': [], 'depths': [], 'visited_counts': [], 'frontier_counts': [], 'outcomes': []} for method in HEURISTIC_METHODS}
            # data[]
            
            for test_case in self.test_case_objects:
                method_data = data[test_case.heuristic_method]
                method_data['execution_times'].append(test_case.execution_time)
                method_data['depths'].append(test_case.depth_of_tree)
                method_data['visited_counts'].append(test_case.nodes_visited_count)
                method_data['frontier_counts'].append(test_case.nodes_frontier_count)
                method_data['outcomes'].append(test_case.result)

            # print(data)
            # Generate plots
            self.plot_graphs(data, pdf)

    def plot_graphs(self, data, pdf):
        max_depth = max(max(test_case.depth_of_tree for test_case in self.test_case_objects), 30)
        depth_ticks = range(0, max_depth + 1, 2)
        
        # Execution Time vs Depth of Solution
        plt.figure(figsize=(10, 5))
        for method, method_data in data.items():
            plt.plot(method_data['depths'], method_data['execution_times'], marker='o', label=method)
        plt.xlabel('Depth of Solution')
        plt.ylabel('Execution Time (ms)')
        plt.title('Execution Time vs Depth of Solution by Heuristic')
        plt.xticks(depth_ticks)
        plt.legend()
        plt.grid(True)
        pdf.savefig()
        plt.close()

        # Nodes Visited vs Depth of Solution
        plt.figure(figsize=(10, 5))
        for method, method_data in data.items():
            plt.plot(method_data['depths'], method_data['visited_counts'], marker='o', label=method)
        plt.xlabel('Depth of Solution')
        plt.ylabel('Nodes Visited')
        plt.title('Nodes Visited vs Depth of Solution by Heuristic')
        plt.xticks(depth_ticks)
        plt.legend()
        plt.grid(True)
        pdf.savefig()
        plt.close()

        # Depth of Solution vs Frontier Nodes
        plt.figure(figsize=(10, 5))
        for method, method_data in data.items():
            plt.plot(method_data['depths'], method_data['frontier_counts'], marker='o', label=method)
        plt.xlabel('Depth of Solution')
        plt.ylabel('Frontier Nodes Count')
        plt.title('Frontier Nodes vs Depth of Solution by Heuristic')
        plt.xticks(depth_ticks)
        plt.legend()
        plt.grid(True)
        pdf.savefig()
        plt.close()


graph_generator_instance = GraphGenerator()
graph_generator_instance.generate_graphs()
