#!/bin/python3
"""
https://projecteuler.net/problem=67
    https://www.hackerrank.com/contests/projecteuler/challenges/euler067
https://projecteuler.net/problem=18
    https://www.hackerrank.com/contests/projecteuler/challenges/euler018

tag_knapsack, tag_dynamic
"""

import sys
import time

TRIANGLE_SIMPLE = """
3
7 4
2 4 6
8 5 9 3
"""

"""
    1313:   sum max by line
    1064:   max sum straight solution
    1074:   the solution
"""
TRIANGLE = """
75
95 64
17 47 82
18 35 87 10
20 04 82 47 65
19 01 23 75 03 34
88 02 77 73 07 63 67
99 65 04 28 06 16 70 92
41 41 26 56 83 40 80 70 33
41 48 72 33 47 32 37 16 94 29
53 71 44 65 25 43 91 52 97 51 14
70 11 33 28 77 73 17 78 39 68 17 57
91 71 52 38 17 14 91 43 58 50 27 29 48
63 66 04 68 89 53 67 30 73 16 69 87 40 31
04 62 98 27 23 09 70 98 73 93 38 53 60 04 23
"""


def find_max_each_line(mat):
    n = len(mat)
    max = [0] * n

    max[0] = mat[0][0]
    for i in range(1, n):
        a = sorted(mat[i], reverse=True)
        max[i] = a[0]
    return max


def find_max_from(mat, line, max_by_line, current, max):
    assert current.sum <= max_by_line[0]

    n = len(mat)
    assert line > 0

    if line == n:
        if current.sum > max.sum:
            max.sum = current.sum
            max.positions = current.positions[:]
            print(current.positions, current.sum)
    else:
        assert line <= n
        pos = current.positions[line - 1]

        # max_by_line used here
        if current.sum + max_by_line[line] < max.sum:
            # print("Dropped: ", current.positions)
            return

        current.positions[line] = pos
        current.sum += mat[line][pos]
        find_max_from(mat, line + 1, max_by_line, current, max)
        current.sum -= mat[line][pos]

        pos += 1
        current.positions[line] = pos
        current.sum += mat[line][pos]
        find_max_from(mat, line + 1, max_by_line, current, max)
        current.sum -= mat[line][pos]

        if 0:
            if line < 60 and line < max.stats.line:
                print(line, int(time.clock() - max.stats.time_start))
                max.stats.line = line


def solve_triangle_direct(mat):
    n = len(mat)

    """
        100 sized triangle
            34'' for line 52 first incrementation:  too slow
    """
    max_by_line = find_max_each_line(mat)
    max_rest = [0] * n
    for i in range(n):
        max_rest[i] = sum(max_by_line[i:])
    # print(max_rest)
    # return

    # find a first candidate
    max = lambda: None
    max.positions = [0] * n
    max.sum = mat[0][0]
    for i in range(1, n):
        curr = max.positions[i - 1]
        if mat[i][curr + 1] > mat[i][curr]:
            curr = curr + 1
        max.sum += mat[i][curr]
        max.positions[i] = curr
    print(max.positions, max.sum)

    max.stats = lambda: None
    max.stats.line = n
    max.stats.time_start = time.clock()

    # now try to improve it
    curr = lambda: None
    curr.positions = [0] * n
    curr.sum = mat[0][0]
    find_max_from(mat, 1, max_rest, curr, max)

    # print(max.positions, max.sum)
    s = 0
    for i in range(n):
        s += mat[i][max.positions[i]]
    assert s == max.sum

    return max.sum


# the fantastic solution:  calculate partial maximal sums from bottom to the top
def solve_triangle_reverse(mat):
    n = len(mat)

    max_partial = mat[n - 1]
    for i in range(n - 1):
        for j in range(n - i - 1):
            max_partial[j] = max(max_partial[j], max_partial[j + 1])
            max_partial[j] += mat[n - i - 2][j]
        # print(max_partial)
    return max_partial[0]


def solve_triangle(mat):
    # return solve_triangle_direct(mat)
    return solve_triangle_reverse(mat)


def parse_triangle(triangle):
    mat = []
    for l in triangle.strip().splitlines():
        c = [int(i) for i in l.strip().split(" ")]
        mat.append(c)
    max = solve_triangle(mat)
    print(max)


def parse_triangle_file(triangle_file):
    f = open(triangle_file, "r")
    triangle = f.read()
    # print(triangle)
    parse_triangle(triangle)


# https://www.hackerrank.com/contests/projecteuler/challenges/euler018
def parse_triangle_input():
    T = int(input().strip())
    for _ in range(T):
        N = int(input().strip())
        mat = []
        for _ in range(N):
            c = [int(i) for i in input().strip().split(" ")]
            mat.append(c)
        max = solve_triangle(mat)
        print(max)


def main():
    # parse_triangle(TRIANGLE_SIMPLE)
    # parse_triangle(TRIANGLE)
    parse_triangle_file("p067_triangle.txt")
    # parse_triangle_input()


if __name__ == "__main__":
    main()
