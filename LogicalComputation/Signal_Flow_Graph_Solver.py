from sympy import sympify, simplify, Mul, Integer

class SignalFlowAnalyzer:
    def __init__(self):
        self.__untouching_loops = {}
        self.__untouching_loops_paths = {}
        self.paths_gain = {}
        self.loops_gain = {}
        self.untouching_loops_number = 0

    def __filter(self, loops, paths):
        loops_sets = []
        paths_sets = []

        self.paths_gain = {idx: path['weight'] for idx, path in enumerate(paths)}
        self.loops_gain = {tuple(loop['loop']): loop['weight'] for loop in loops}

        for loop_description in loops:
            loops_sets.append(set(loop_description['loop']))

        for idx, path_description in enumerate(paths):
            path_nodes = path_description['path']
            paths_sets.append(set(path_nodes))

            self.__untouching_loops_paths[idx] = {}
            self.__untouching_loops_paths[idx][0] = [
                [loop['loop']] for loop in loops if set(loop['loop']).isdisjoint(set(path_nodes))
            ]

        self.__untouching_loops[0] = [[loop['loop']] for loop in loops]

        loops_number = 1

        while True:
            self.__untouching_loops[loops_number] = []
            current_level = self.__untouching_loops[loops_number - 1]

            for i in range(len(self.__untouching_loops[0])):
                for j in range(i + 1, len(current_level)):
                    loop_a = self.__untouching_loops[0][i]
                    loop_b = current_level[j]

                    loop_a_union = set().union(*loop_a)
                    loop_b_union = set().union(*loop_b)

                    if loop_a_union.isdisjoint(loop_b_union):
                        combined = loop_a + loop_b
                        if combined not in self.__untouching_loops[loops_number]:
                            self.__untouching_loops[loops_number].append(combined)

            if not self.__untouching_loops[loops_number]:
                break

            loops_number += 1

        max_level = loops_number  # Avoids accessing the last empty level
        self.untouching_loops_number = max_level

        for idx, path_description in enumerate(paths):
            path_set = set(path_description['path'])
            for level in range(1, max_level):
                self.__untouching_loops_paths[idx][level] = []
                for loop_combo in self.__untouching_loops[level]:
                    loop_union = set().union(*loop_combo)
                    if path_set.isdisjoint(loop_union):
                        self.__untouching_loops_paths[idx][level].append(loop_combo)

    def __calculate_delta(self):
        delta = Integer(1)
        sign = -1
        for loops_keys in self.__untouching_loops:
            all_loops = self.__untouching_loops[loops_keys]
            summation = Integer(0)
            for non_touching_loops in all_loops:
                multiplication_of_loops = Integer(1)
                for loop in non_touching_loops:
                    loop_gain = self.loops_gain[tuple(loop)]
                    multiplication_of_loops *= loop_gain
                summation += multiplication_of_loops
            delta += sign * summation
            sign *= -1
        return delta

    def __calculate_sigma_paths_mul_delta(self):
        numerator_summation = 0
        deltas = []
        for path_idx in self.__untouching_loops_paths:
            loops_info = self.__untouching_loops_paths[path_idx]
            delta = Integer(1)
            sign = -1
            for loops_keys in loops_info:
                all_loops = loops_info[loops_keys]
                summation = Integer(0)
                for non_touching_loops in all_loops:
                    multiplication_of_loops = Integer(1)
                    for loop in non_touching_loops:
                        loop_gain = self.loops_gain[tuple(loop)]
                        multiplication_of_loops *= loop_gain
                    summation += multiplication_of_loops
                delta += sign * summation
                sign *= -1
            deltas.append(delta)
            numerator_summation += delta * self.paths_gain[path_idx]

        return numerator_summation, deltas

    def solve(self, loops, paths):
        self.__filter(loops, paths)
        delta = self.__calculate_delta()
        numerator, deltas = self.__calculate_sigma_paths_mul_delta()
        print("num: " + str(numerator))
        print("delta: " + str(delta))
        result = numerator / delta
        print("result: " + str(result))
        return delta, deltas, self.__untouching_loops, result
