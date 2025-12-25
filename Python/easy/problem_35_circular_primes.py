#!/bin/python3
"""
tag_primes

https://projecteuler.net/problem=35
    How many circular primes are there below one million?

https://www.hackerrank.com/contests/projecteuler/challenges/euler035
    Score: 100.00

pylint 1.5.5
    Your code has been rated at 8.41/10
"""

import math

####################################################


def get_primes(limit):
    # not rounded since we skip 1 & 2
    primes = [i * 2 + 3 for i in range(limit // 2 - 1)]
    limit_of_sieve = 1 + math.floor(math.sqrt(limit))
    for i in range(3, limit_of_sieve, 2):
        if primes[i // 2 - 1]:
            for j in range(i * i, limit, 2 * i):
                primes[j // 2 - 1] = 0
    return [2] + [i for i in primes if i != 0]


####################################################


def no_digits(number, base=10):
    digits = 0
    while number >= 1:
        number //= base
        digits += 1
    return digits


def get_digits(number, base=10):
    digits = []
    while number >= 1:
        digits.append(number % base)
        number //= base
    return digits


def get_digits_r(number, base=10):
    digits = get_digits(number, base)
    return digits[::-1]


####################################################


def get_rotation(digits, pos):
    number = 0
    for i in range(pos, len(digits)):
        number *= 10
        number += digits[i]
    for i in range(pos):
        number *= 10
        number += digits[i]
    return number


def solve_problem_primes(primes, limit):
    primes_set = set(primes)

    circular_primes = []
    for i in primes:
        if i >= limit:
            break
        digits = get_digits_r(i)
        is_circular_prime = True
        for j in range(1, len(digits)):
            rotation = get_rotation(digits, j)
            # print(i, rotation)
            if not rotation in primes_set:
                is_circular_prime = False
                break
        if is_circular_prime:
            circular_primes.append(i)

    return circular_primes


def solve_problem(limit):
    primes = get_primes(10 ** no_digits(limit - 1))
    return solve_problem_primes(primes, limit)


# https://www.hackerrank.com/contests/projecteuler/challenges/euler035
def parse_input():
    limit = int(input().strip())
    circular_primes = solve_problem(limit)
    print(sum(circular_primes))


def problem():
    circular_primes = solve_problem(1000000)
    print(len(circular_primes))


def debug_assertions():
    primes = get_primes(1000)
    assert len(solve_problem_primes(primes, 50)) == 9
    assert len(solve_problem_primes(primes, 100)) == 13
    assert sum(solve_problem_primes(primes, 100)) == 446
    assert len(solve_problem_primes(primes, 1000)) == 25


def main():
    debug_assertions()

    # parse_input()
    # problem()


if __name__ == "__main__":
    main()
