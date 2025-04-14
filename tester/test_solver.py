import sys
import os

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(parent_dir)

from sympy import symbols
from LogicalComputation.untouchingFilter import SignalFlowAnalyzer
from LogicalComputation.solver import solver



class MockEdge:
    def __init__(self, source, target, weight):
        self.source = source
        self.target = target
        self.weight = weight


class MockNode:
    def __init__(self, node_id):
        self.id = node_id
        self.outward_edges = []  # List of MockEdge objects going out of this node
        self.inward_edges = []  # List of MockEdge objects coming into this node

    def add_edge(self, neighbor, weight):
        edge = MockEdge(self, neighbor, weight)  # Create a MockEdge object
        self.outward_edges.append(edge)  # Add the edge to outward_edges
        neighbor.inward_edges.append(edge)  # Add the edge to the neighbor's inward_edges

def test_solver():
    # Create mock nodes
    node_R = MockNode('x1')
    node_A = MockNode('A')
    node_B = MockNode('B')
    node_C = MockNode('C')
    node_h = MockNode('x7')

    x, y,t = symbols('x y t')

    node_R.add_edge(node_A, x)
    node_A.add_edge(node_B, 3)
    node_B.add_edge(node_C, 2)
    node_B.add_edge(node_A, -y)
    node_A.add_edge(node_C, 6)
    node_C.add_edge(node_B, 4)
    node_C.add_edge(node_h, 1)
    node_C.add_edge(node_A, y)


    class MockCanvas:
        @property
        def adj_list(self):
            return [node_R, node_A, node_B, node_C, node_h]


    canvas = MockCanvas()
    solver_instance = solver(canvas)


    solver_instance.extract_paths_and_loops()

    filter = SignalFlowAnalyzer()
    filter.solve(solver_instance.loops, solver_instance.paths)

    print("Paths:")
    print(solver_instance.paths)
    for path in solver_instance.paths:
        path_str = " -> ".join(node for node in path["path"])
        print(f"Path: {path_str}, Weight: {path['weight']}")

    print("\nLoops:")
    print(solver_instance.loops)
    for loop in solver_instance.loops:
        loop_str = " -> ".join(node for node in loop["loop"])
        print(f"Loop: {loop_str}, Weight: {loop['weight']}")


if __name__ == "__main__":
    test_solver()