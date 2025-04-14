from LogicalComputation.solver import solver
from sympy import symbols
from LogicalComputation.untouchingFilter import SignalFlowAnalyzer


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


def test_solver_with_three_untouching_loops():
    # Create mock nodes
    node_R = MockNode('x1')
    node_A = MockNode('A')
    node_B = MockNode('B')
    node_C = MockNode('C')
    node_D = MockNode('D')
    node_E = MockNode('E')
    node_F = MockNode('F')
    node_G = MockNode('G')
    node_h = MockNode('x7')

    x, y, t = symbols('x y t')

    # Path from R to h
    node_R.add_edge(node_A, x)
    node_A.add_edge(node_B, 1)
    node_B.add_edge(node_C, 1)
    node_C.add_edge(node_D, 1)
    node_D.add_edge(node_E, 1)
    node_E.add_edge(node_F, 1)
    node_F.add_edge(node_G, 1)
    node_G.add_edge(node_h, 1)

    # Loop 1: A → B → A
    node_B.add_edge(node_A, y)

    # Loop 2: C → D → C
    node_D.add_edge(node_C, t)

    # Loop 3: E → F → E
    node_F.add_edge(node_E, x)

    class MockCanvas:
        @property
        def adj_list(self):
            return [node_R, node_A, node_B, node_C, node_D, node_E, node_F, node_G, node_h]

    canvas = MockCanvas()
    solver_instance = solver(canvas)

    solver_instance.extract_paths_and_loops()

    filter = SignalFlowAnalyzer()
    filter.solve(solver_instance.loops, solver_instance.paths)

if __name__ == "__main__":
    print("\n---\n")
    test_solver_with_three_untouching_loops()
