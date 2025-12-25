#!/bin/python3
"""
https://projecteuler.net/problem=34
    "Find the sum of all numbers which are equal to the sum of the factorial of their digits."

    It very much reassembles to https://projecteuler.net/problem=30,
    only here we use factorials, no power.

https://www.hackerrank.com/contests/projecteuler/challenges/euler034
    Score: 100.

pylint
    Your code has been rated at 8.15/10 .
"""

from array import array


def no_digits(n):
    digits = 0
    while n >= 1:
        n //= 10
        digits += 1
    return digits


def get_digits(n):
    digits = []
    while n >= 1:
        digits.append(n % 10)
        n //= 10
    return digits


def max_digits():
    term_9 = 9 * 8 * 7 * 6 * 5 * 4 * 3 * 2

    factor = 2
    digits = no_digits(factor * term_9)
    while digits >= factor:
        digits = no_digits(factor * term_9)
        factor += 1
    return factor - 1


def is_curious(factorials, number):
    digits = get_digits(number)
    partial = 0
    for j in digits:
        partial += factorials[j]
    return partial == number


def solve_problem_to(factorials, limit, to_print=False):
    sum_curious_numbers = 0
    for i in range(10, 1 + limit):
        if is_curious(factorials, i):
            if to_print:
                print(i)
            sum_curious_numbers += i
        elif to_print and i % 10000 == 0:
            print(i)
    return sum_curious_numbers


def solve_problem():
    factorials = array("I")
    factorials.append(1)
    for i in range(1, 10):
        factorials.append(i * factorials[i - 1])

    max_nb = max_digits() * factorials[9]
    # print(max_nb)

    return solve_problem_to(factorials, max_nb)


def is_hackerrank(factorials, number):
    digits = get_digits(number)
    partial = 0
    for j in digits:
        partial += factorials[j]
    return partial % number == 0


def solve_hackerrank(limit, to_print=False):
    factorials = array("I")
    factorials.append(1)
    for i in range(1, 10):
        factorials.append(i * factorials[i - 1])

    sum_curious_numbers = 0
    for i in range(10, 1 + limit):
        if is_hackerrank(factorials, i):
            if to_print:
                print(i)
            sum_curious_numbers += i
        elif to_print and i % 10000 == 0:
            print(i)

    return sum_curious_numbers


# https://www.hackerrank.com/contests/projecteuler/challenges/euler034
def parse_input():
    limit = int(input().strip())
    # print(solve_hackerrank(limit, True))
    print(solve_hackerrank(limit))


def problem():
    print(solve_problem())


def debug_assertions():
    assert max_digits() == 7

    factorials = array("I")
    factorials.append(1)
    for i in range(1, 10):
        factorials.append(i * factorials[i - 1])

    assert is_curious(factorials, 145)
    assert is_curious(factorials, 40585)

    # solve_problem_to(factorials, 3000000, True)


def main():
    debug_assertions()

    # parse_input()
    # problem()


if __name__ == "__main__":
    main()
