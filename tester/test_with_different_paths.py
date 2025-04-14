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
        self.outward_edges = []
        self.inward_edges = []

    def add_edge(self, neighbor, weight):
        edge = MockEdge(self, neighbor, weight)
        self.outward_edges.append(edge)
        neighbor.inward_edges.append(edge)

def test_multiple_paths():
    # Create nodes
    node_R = MockNode('x1')
    node_A = MockNode('A')
    node_B = MockNode('B')
    node_C = MockNode('C')
    node_D = MockNode('D')
    node_E = MockNode('E')
    node_F = MockNode('F')
    node_G = MockNode('G')
    node_H = MockNode('H')
    node_h = MockNode('x7')

    x, y, z = symbols('x y z')

    # Path 1: x1 → A → B → C → D → x7
    node_R.add_edge(node_A, x)
    node_A.add_edge(node_B, 1)
    node_B.add_edge(node_C, 1)
    node_C.add_edge(node_D, 1)
    node_D.add_edge(node_h, 1)

    # Path 2: x1 → A → E → F → G → x7
    node_A.add_edge(node_E, 1)
    node_E.add_edge(node_F, 1)
    node_F.add_edge(node_G, 1)
    node_G.add_edge(node_h, 1)

    # Loops
    node_B.add_edge(node_C, y)   # Loop 1: B → C
    node_E.add_edge(node_F, 1)
    node_F.add_edge(node_E, z)   # Loop 2: E → F
    node_G.add_edge(node_H, 1)
    node_H.add_edge(node_G, 1)   # Loop 3: G → H

    class MockCanvas:
        @property
        def adj_list(self):
            return [node_R, node_A, node_B, node_C, node_D, node_E, node_F, node_G, node_H, node_h]

    canvas = MockCanvas()
    solver_instance = solver(canvas)
    solver_instance.extract_paths_and_loops()

    filter = SignalFlowAnalyzer()
    filter.solve(solver_instance.loops, solver_instance.paths)


if __name__ == "__main__":
    test_multiple_paths()
