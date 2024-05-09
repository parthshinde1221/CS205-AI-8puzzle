from Npuzzle import *
import matplotlib as plt
from matplotlib.backends.backend_pdf import PdfPages

# global variables
# Add or generate test_cases in this format for n-puzzle problems
GOAL_STATE = '123456780'
PUZZLE_SIZE = 3
TEST_CASES ={
                '123456780':GOAL_STATE,
                '123456078':GOAL_STATE,
                '136502478':GOAL_STATE,
                '136507482':GOAL_STATE,
                '167503482':GOAL_STATE,
                '712485630':GOAL_STATE,
                '072461358':GOAL_STATE
}
HEURISTIC_METHODS = ['UCS','Manhattan','Misplaced_tile']


class test_case:
    def __init__(self,init_state,goal_state,puzzle_size,heurstic_method='UCS'): 
        # methods can be 'UCS,Manhattan,Misplaced_tile'
        self.heurstic_method = heurstic_method
        self.init_state = init_state
        self.goal_state = goal_state
        self.puzzle_size = puzzle_size

        # members to populated
        self.depth_of_tree = 0
        self.nodes_visited_count = 0
        self.nodes_frontier_count = 0
        self.excuetion_time = 0
        # Success or Failure
        self.result = ''

    def generate_results(self):
        search_obj = Searcher()
        start_time = time()
        path = search_obj.general_search(self.init_state,self.goal_state,self.puzzle_size,self.heurstic_method)
        end_time = time()

        if path == "failure":
            self.result = 'Failure'
            print("\nNo solution found.")
        else:
            self.result = 'Sucess'
            print("\nSolution found:")
            # print_path(path, self.n)

        print(f'TIME TAKEN FOR SEARCH EXCUETION:- {(end_time-start_time) * 1000} ms')    

        self.excuetion_time = (end_time-start_time) * 1000
        self.depth_of_tree = len(path)
        self.nodes_frontier_count = len(search_obj.frontier)
        self.nodes_visited_count = len(search_obj.visited)

    def print_data(self):
        print(f'Data {self.init_state},{self.heurstic_method}==>{self.depth_of_tree},{self.nodes_visited_count},{self.nodes_frontier_count},{self.excuetion_time}')
    

        

class graph_generator:
    def __init__(self):
        self.test_case_objects = [test_case(test_case_init_state,test_case_goal_state,puzzle_size=PUZZLE_SIZE,heurstic_method=method) for test_case_init_state,test_case_goal_state in TEST_CASES.items() for method in HEURISTIC_METHODS]
    
    def generate_graphs(self):
        a = [test_case_obj.generate_results() for test_case_obj in self.test_case_objects]
        b = [test_case_obj.print_data() for test_case_obj in self.test_case_objects]
        
        with PdfPages('n_puzzle_analysis.pdf') as pdf:
        # DEPTH OF SOLN VS TIME
            data = {method: {'execution_times': [], 'depths': [], 'visited_counts': [], 'frontier_counts': [], 'outcomes': []}
                    for method in HEURISTIC_METHODS}

            for test_case in self.test_case_objects:
                method_data = data[test_case.heurstic_method]
                method_data['execution_times'].append(test_case.excuetion_time)
                method_data['depths'].append(test_case.depth_of_tree)
                method_data['visited_counts'].append(test_case.nodes_visited_count)
                method_data['frontier_counts'].append(test_case.nodes_frontier_count)
                method_data['outcomes'].append(test_case.result)

            # Execution Time vs Depth of Solution
            plt.figure(figsize=(10, 5))
            for method, method_data in data.items():
                plt.plot(method_data['depths'], method_data['execution_times'], marker='o', label=method)
            plt.xlabel('Depth of Solution')
            plt.ylabel('Execution Time (ms)')
            plt.title('Execution Time vs Depth of Solution by Heuristic')
            plt.legend()
            plt.grid(True)
            pdf.savefig()
            # plt.close()
            # plt.show()

            # Nodes Visited vs Depth of Solution
            plt.figure(figsize=(10, 5))
            for method, method_data in data.items():
                plt.plot(method_data['depths'], method_data['visited_counts'], marker='o', label=method)
            plt.xlabel('Depth of Solution')
            plt.ylabel('Nodes Visited')
            plt.title('Nodes Visited vs Depth of Solution by Heuristic')
            plt.legend()
            plt.grid(True)
            pdf.savefig()
            # plt.close()
            # plt.show()

            # plt.show()
    

        # DEPTH OF SOLN VS NODES EXPLORED(VISITED)


        # DEPTH OF SOLN VS FRONTIER NODES(CHOSEN PATH)


        # NO OF SOLUTION WIHT FAILURE/SUCCESS VS TIME


graph_generator().generate_graphs()


        

    

