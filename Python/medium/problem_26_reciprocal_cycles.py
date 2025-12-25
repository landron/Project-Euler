#! /usr/bin/python3
"""
https://projecteuler.net/problem=26
    Find the value of d < 1000 for which 1/d contains the longest
    recurring cycle in its decimal fraction part.

    "The infinitely repeated digit sequence is called the repetend."
    There is always a repetend (that can be 0 for 1/8 = 0.125 by example)
    because these are rational numbers.
    "It can be shown that a number is rational if and only if its decimal
    representation is repeating or terminating."
    https://en.wikipedia.org/wiki/Repeating_decimal

    error 1:    no, the length of the repetend is not limited to the number
        of digits, 10

    "For an arbitrary integer n, the length L(n) of the decimal repetend
    of 1/n divides φ(n), where φ is the totient function."
    https://en.wikipedia.org/wiki/Repeating_decimal#Totient_rule
        Totient rule, https://en.wikipedia.org/wiki/Full_reptend_prime

https://www.hackerrank.com/contests/projecteuler/challenges/euler026
     Score: 100.00 (solve_problem_3)

pylint, flake8
"""
from dataclasses import dataclass
import math

###############################################################################


def get_primes(limit):
    # not rounded since we skip 1 & 2
    primes = [i * 2 + 3 for i in range(limit // 2 - 1)]
    limit_of_sieve = 1 + math.floor(math.sqrt(limit))
    for i in range(3, limit_of_sieve, 2):
        if primes[i // 2 - 1]:
            for j in range(i * i, limit, 2 * i):
                primes[j // 2 - 1] = 0
    return [2] + [i for i in primes if i != 0]


def no_digits(number, base=10):
    """get the number of the digits of the given number in the given base"""
    digits = 0
    while number >= 1:
        number //= base
        digits += 1
    return digits


###############################################################################


def get_repetend_length(big_10, number):
    assert big_10 > number

    reminders = set()

    current = big_10 % number
    while current != 0 and current not in reminders:
        reminders.add(current)
        current = (current * 10) % number

    length = len(reminders) if current != 0 else 0
    # print(number, length)
    return length


@dataclass
class Max:
    # pylint: disable=missing-class-docstring
    val: int = 2
    repeating: int = 0


def solve_problem_1(limit):
    """Score: 66.67"""
    maxi = Max()

    big_10 = 10
    for i in range(2, limit):
        if i == big_10:
            big_10 *= 10
        if big_10 % i == 0:
            continue

        repetend_len = get_repetend_length(big_10, i)
        if repetend_len > maxi.repeating:
            maxi.repeating = repetend_len
            maxi.val = i
            # print(maxi.val, maxi.repeating)

    return (maxi.val, maxi.repeating)


def solve_problem_2(limit):
    """
    a little risky, as not these numbers are primes
    Score: 66.67 (3/4)
    """
    maxi = Max()

    primes = get_primes(limit)

    big_10 = 10
    for i in primes:
        if i > big_10:
            big_10 *= 10
        if big_10 % i == 0:
            continue

        repetend_len = get_repetend_length(big_10, i)
        if repetend_len > maxi.repeating:
            maxi.repeating = repetend_len
            maxi.val = i
            # print(maxi.val, maxi.repeating)

    return (maxi.val, maxi.repeating)


def solve_problem_3(limit):
    """
    stop after the first full repetend prime
    I think the function is correct for limits that are powers of 10
    Score: 100.00
    """
    maxi = Max()

    primes = get_primes(limit)
    primes = primes[::-1]

    big_10 = 10 ** no_digits(limit)

    for i in primes:
        if i < big_10 / 10:
            big_10 /= 10
        if big_10 % i == 0:
            continue

        repetend_len = get_repetend_length(big_10, i)
        if repetend_len == i - 1:
            maxi.repeating = repetend_len
            maxi.val = i
            break

    return (maxi.val, maxi.repeating)


def solve_problem(limit):
    # return solve_problem_1(limit)
    return solve_problem_1(limit) if limit < 100 else solve_problem_3(limit)


def solve_problem_get_number_only(limit):
    (number, _) = solve_problem(limit)
    return number


def parse_input():
    """https://www.hackerrank.com/contests/projecteuler/challenges/euler026"""
    cases = int(input().strip())
    for _ in range(cases):
        limit = int(input().strip())
        print(solve_problem_get_number_only(limit))


def problem():
    print(solve_problem(1000))


def debug_assertions():
    assert solve_problem(5) == (3, 1)
    assert solve_problem(10) == (7, 6)
    assert solve_problem(100) == (97, 96)

    assert solve_problem_1(123) == (113, 112)
    assert solve_problem_2(123) == (113, 112)
    assert solve_problem_3(123) == (113, 112)


def main():
    debug_assertions()

    # parse_input()
    # problem()


if __name__ == "__main__":
    main()
