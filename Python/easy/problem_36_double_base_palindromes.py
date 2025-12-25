#!/bin/python3
"""
https://projecteuler.net/problem=36
    "Find the sum of all numbers, less than one million, which are palindromic
    in base 10 and base 2."

https://www.hackerrank.com/contests/projecteuler/challenges/euler036
    Score: 100

pylint
    Your code has been rated at 7.62/10.

Optimization:
    generate the palindromes instead of test all the numbers
"""


def get_digits(n, base):
    digits = []
    while n >= 1:
        digits.append(n % base)
        n //= base
    return digits


def is_palindromic(digits):
    size = len(digits)
    for i in range(1 + size // 2):
        if digits[i] != digits[size - i - 1]:
            return False
    return True


def is_number_palindromic(number, base):
    digits = get_digits(number, base)
    return is_palindromic(digits)


def solve_problem(limit, base):
    sum_of = 0
    for i in range(limit):
        # last digit is 0
        if i % limit == 0:
            continue

        digits = get_digits(i, 10)
        if not is_palindromic(digits):
            continue

        digits = get_digits(i, base)
        if is_palindromic(digits):
            # print(i)
            sum_of += i
    return sum_of


# https://www.hackerrank.com/contests/projecteuler/challenges/euler036
def parse_input():
    (limit, base) = tuple(int(i) for i in input().strip().split(" "))
    print(solve_problem(limit, base))


def problem():
    print(solve_problem(1000000, 2))


def debug_assertions():
    assert is_number_palindromic(7, 8)
    assert is_number_palindromic(7, 10)
    assert is_number_palindromic(585, 10)
    assert is_number_palindromic(585, 2)


def main():
    debug_assertions()

    # parse_input()
    # problem()


if __name__ == "__main__":
    main()
