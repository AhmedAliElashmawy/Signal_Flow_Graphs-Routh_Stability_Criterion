from sympy import sympify, simplify, Mul

class solver:
    def __init__(self, canvas):
        self.__canvas = canvas
        self.__node_list = canvas.adj_list
        self.__paths = []  # To store all paths from input to output
        self.__loops = []  # To store all loops
        self.__input_node = self.__find_input_node()
        self.__output_node = self.__find_output_node()

    def __find_input_node(self):
        # Find the node with no inward edges
        for node in self.__node_list:
            if not node.inward_edges:
                return node
        raise ValueError("No input node found (node with no inward edges).")

    def __find_output_node(self):
        # Find the node with no outward edges
        for node in self.__node_list:
            if not node.outward_edges:
                return node
        raise ValueError("No output node found (node with no outward edges).")

    def __dfs(self, current_node, path, incoming_weight):
        path.append((current_node, incoming_weight))  # Store node with weight of incoming edge

        if current_node == self.__output_node:  # End node
            self.__paths.append(path.copy())
        else:
            for edge in current_node.outward_edges:
                neighbor = edge.target
                if all(n != neighbor for n, _ in path):  # Avoid cycles in path
                    self.__dfs(neighbor, path, edge.weight)

        path.pop()  # Backtrack

    def extract_paths_and_loops(self):
        for node in self.__node_list:
            if node == self.__input_node:  # Input node
                self.__dfs(node, [], 1)
        self.__detect_loops()

    def __detect_loops(self):
        for node in self.__node_list:
            self.__find_loops(node, [])

    def __find_loops(self, current_node, path):
        for edge in current_node.outward_edges:
            neighbor = edge.target
            index = next((i for i, (n, _) in enumerate(path) if n == neighbor), -1)
            if index != -1:
                loop_path = path[index:] + [(neighbor, edge.weight)]
                if not self.__is_duplicate_loop(loop_path):
                    self.__loops.append(loop_path)
            else:
                path.append((neighbor, edge.weight))
                self.__find_loops(neighbor, path)
                path.pop()
    
    
    
    def __is_duplicate_loop(self, new_loop):
        new_ids = [node.id for node, _ in new_loop]
        new_ids_set = set(new_ids)
        new_weight = self.__calculate_path_weight(new_loop, is_loop=True)

        for loop in self.__loops:
            existing_ids = [node.id for node, _ in loop]
            existing_ids_set = set(existing_ids)
            existing_weight = self.__calculate_path_weight(loop, is_loop=True)

            # Compare node ID sets
            if existing_ids_set == new_ids_set:
                # Compare symbolic loop weights
                if new_weight.equals(existing_weight):
                    return True

        return False


    @property
    def paths(self):
        return [
            {"path": [node.id for node, _ in path], "weight": self.__calculate_path_weight(path)}
            for path in self.__paths
        ]

    @property
    def loops(self):
        return [
            {
                "loop": [node.id for node, _ in loop],
                "weight": self.__calculate_path_weight(loop, is_loop=True)
            }
            for loop in self.__loops
        ]

    def __calculate_path_weight(self, path, is_loop=False):
        weights = []

        if is_loop:
            for i in range(1, len(path)):
                _, edge_weight = path[i]
                weights.append(edge_weight)
        else:
            for _, edge_weight in path:
                weights.append(edge_weight)

        # Use symbolic multiplication
        return simplify(Mul(*[sympify(w) for w in weights], evaluate=False))