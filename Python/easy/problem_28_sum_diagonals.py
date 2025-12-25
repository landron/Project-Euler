#!/bin/python3
"""
https://projecteuler.net/problem=28

https://www.hackerrank.com/contests/projecteuler/challenges/euler028
    done

Formula calculation (mostly in the subway):
- 1 + sum_of_odd(n*n+3*(n-1)*(n-1)+3) =>
    sum_of_natural conversion, where 2*new_n+1 = old_n (old_n being odd)
- 1 + 16*sum(n*n) + 4*sum(n) + 4*n =>
- 1 + 2/3 * (8*n^3 + 15*n^2 + 13*n)
    knowing that sum(n*n) = n(n+1)(2n+1)/6 and sum(n)=n(n+1)/2

Your code has been rated at 8.59/10 (previous run: 8.59/10, +0.00)
"""


def problem_solve_formula(size):
    assert size % 2 == 1

    n = (size - 1) // 2
    return 1 + 2 * (8 * n * n * n + 15 * n * n + 13 * n) // 3


def calculate_sum(tab):
    size = len(tab)
    sum_ = 0
    for i in range(size):
        sum_ += tab[i][i]
        if size - i - 1 != i:
            sum_ += tab[i][size - i - 1]
    return sum_


def problem_solve_brute(size):
    assert size % 2 == 1

    tab = size * [[]]
    for i in range(size):
        tab[i] = size * [0]

    i = j = size // 2
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
        while j > size - i - 1:
            j -= 1
            val += 1
            tab[i][j] = val
        while i > j:
            i -= 1
            val += 1
            tab[i][j] = val
        while j < size - i - 1:
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


def problem_solve(size):
    # return problem_solve_brute(size)
    return problem_solve_formula(size)


# https://www.hackerrank.com/contests/projecteuler/challenges/euler028
def parse_input_hackerrank():
    cases = int(input().strip())
    for _ in range(cases):
        size = int(input().strip())

        res = problem_solve(size)
        # hackerrank condition
        res = res % (10**9 + 7)
        print(res)


def problem():
    print(problem_solve(1001))


def debug_assertions():
    assert problem_solve_brute(3) == 25
    assert problem_solve_brute(5) == 101
    assert problem_solve_formula(3) == 25
    assert problem_solve_formula(5) == 101


def main():
    debug_assertions()

    # parse_input_hackerrank()
    problem()


if __name__ == "__main__":
    main()
