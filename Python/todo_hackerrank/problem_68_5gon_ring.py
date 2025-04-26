"""
https://projecteuler.net/problem=68
Magic 5-gon Ring

todo_hackerrank: 6/22
TODO: parse_input can be optimized knowing the sum of the line
"""

from dataclasses import dataclass
import time

from project_euler.proj_euler import get_combinatorics_start, combine_numbers

GET_PERMUTATIONS = True


@dataclass
class NGon:
    """n-gon ring"""

    axis_no: int = 3

    def get_nodes_no(self):
        """number of nodes of the graph"""
        return self.axis_no * 2

    def get_min_sum(self):
        """minimal sum to start with"""
        return self.get_nodes_no() + 1 + 2

    def get_max_sum(self):
        """maximal sum to start with: rough estimation"""
        count = self.get_nodes_no()
        # (count, count-1, count-4) : first arrangement
        return count + count - 2 + count - 3

    def start_nb(self):
        """best number to start with"""
        return self.axis_no + 1


def check_solution(externals, rest, matched_sum):
    """is the permutation a solution ?
    externals: external nodes of the graph
    """
    axis_no = len(externals)
    sum0 = externals[0] + rest[0] + rest[1]
    if matched_sum and sum0 != matched_sum:
        return False
    for i in range(axis_no - 2):
        if sum0 != externals[i + 1] + rest[i + 1] + rest[i + 2]:
            return False
    return sum0 == externals[axis_no - 1] + rest[axis_no - 1] + rest[0]


def combine_solution(externals, rest):
    """combine the lists into a solution"""
    axis_no = len(externals)
    solution = [externals[0], rest[0], rest[1]]
    for i in range(axis_no - 2):
        solution.extend([externals[i + 1], rest[i + 1], rest[i + 2]])
    solution.extend([externals[axis_no - 1], rest[axis_no - 1], rest[0]])
    return solution


def solve_configuration_with(externals, matched_sum):
    """solve the given configuration of external nodes, with the matched sum on each
    segment"""
    axis_no = len(externals)
    remaining = sorted(
        [x for x in range(1, 2 * axis_no + 1) if x not in externals], reverse=True
    )
    all_solutions = []
    perm = get_combinatorics_start(not GET_PERMUTATIONS, axis_no, axis_no)
    while True:
        current = [remaining[i] for i in perm.current()]
        if check_solution(externals, current, matched_sum):
            # print(current)
            solution = combine_numbers(combine_solution(externals, current))
            if not matched_sum:
                return solution
            all_solutions += [solution]
        if not perm.next():
            break
    return all_solutions


def solve_configuration(externals):
    """solve the given configuration of external nodes (if possible)"""
    return solve_configuration_with(externals, 0)


def solve():
    """https://projecteuler.net/problem=68"""
    start = time.time()

    result = solve_configuration([6, 10, 9, 8, 7])

    duration = time.time() - start
    if duration >= 1:
        print(f"Result {result} in {duration:.2f} seconds")
    else:
        print(result)


def parse_input():
    """
    read input and solve the problem as defined on HackerRank
    https://www.hackerrank.com/contests/projecteuler/challenges/euler068

    Results: 16/22 Terminated due to timeout

    see 5 16:
        21049436378715110
        24105101817673934
        2594936378711015
        2951051817673439
    """

    def already_seen(perm):
        return perm[0] != sorted(perm)[0]

    axis_no, matchSum = map(int, input().split())
    # print(axis_no, matchSum)
    perm = get_combinatorics_start(not GET_PERMUTATIONS, 2 * axis_no, axis_no)
    all_solutions = []
    while True:
        current = [x + 1 for x in perm.current()]
        if not already_seen(current):
            # print(current)
            solutions = solve_configuration_with(current, matchSum)
            if solutions:
                all_solutions += solutions
        if not perm.next():
            break
    # all_solutions.sort()
    all_solutions = sorted(map(str, all_solutions))
    for i in all_solutions:
        print(i)


def debug_validations():
    """assertions"""
    assert NGon().get_min_sum() == 9
    assert NGon().get_max_sum() == 13
    assert NGon().start_nb() == 4
    assert NGon(5).get_min_sum() == 13
    assert NGon(5).get_max_sum() == 25
    assert NGon(5).start_nb() == 6

    assert check_solution([4, 6, 5], [3, 2, 1], 0)
    assert solve_configuration([4, 6, 5]) == 432621513


def main():
    """main"""
    debug_validations()

    # solve()
    # parse_input()


if __name__ == "__main__":
    main()
