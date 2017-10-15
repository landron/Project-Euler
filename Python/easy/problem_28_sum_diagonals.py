#!/bin/python3
'''
    https://projecteuler.net/problem=28

    https://www.hackerrank.com/contests/projecteuler/challenges/euler028
        score:  25/100
        todo_hackerrank : I bet there is a formula
'''

def calculate_sum(tab):
    size = len(tab)
    sum_ = 0
    for i in range(size):
        sum_ += tab[i][i]
        if size-i-1 != i:
            sum_ += tab[i][size-i-1]
    return sum_

def problem_solve(size):
    assert size%2 == 1

    tab = size * [[]]
    for i in range(size):
        tab[i] = size * [0]

    i = j = size//2
    val = 1
    tab[i][j] = val
    while True:
        j += 1
        if j == size:
            break
        val += 1
        tab[i][j] = val

        while i < j:
            i += 1
            val += 1
            tab[i][j] = val
        while j > size-i-1:
            j -= 1
            val += 1
            tab[i][j] = val
        while i > j:
            i -= 1
            val += 1
            tab[i][j] = val
        while j < size-i-1:
            j += 1
            val += 1
            tab[i][j] = val

        # for l in range(size):
        #     print(tab[l])
        # print()

    # for i in range(size):
    #     print(tab[i])
    # print()

    return calculate_sum(tab)

# https://www.hackerrank.com/contests/projecteuler/challenges/euler028
def parse_input():
    T = int(input().strip())
    for _ in range(T):
        N = int(input().strip())
        print(problem_solve(N))

def problem():
    print(problem_solve(1001))

def debug_assertions():
    assert problem_solve(3) == 25
    assert problem_solve(5) == 101

def main():
    debug_assertions()

    # parse_input()
    problem()

if __name__ == "__main__":
    main()
