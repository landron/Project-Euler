#!/bin/python3
'''
    tag_primes

    https://projecteuler.net/problem=27
        "Find the product of the coefficients for the quadratic expression that produces
         the maximum number of primes for consecutive values of n, starting with n=0."

    https://www.hackerrank.com/contests/projecteuler/challenges/euler027
        Score: 100.00

    pylint
        Your code has been rated at 8.10/10
'''

import math

####################################################

def get_primes(limit):
    # not rounded since we skip 1 & 2
    primes = [i*2+3 for i in range(limit//2-1)]
    limit_of_sieve = 1+math.floor(math.sqrt(limit))
    for i in range(3, limit_of_sieve, 2):
        if primes[i//2-1]:
            for j in range(i*i, limit, 2*i):
                primes[j//2-1] = 0
    return [2]+[i for i in primes if i != 0]

####################################################

def primes_no(coef_a, coef_b, primes_set, primes_limit):
    i = 0
    while True:
        val = i*i + i*coef_a + coef_b
        if val < 0:
            val = -val
        elif val == 0:
            break

        if val > primes_limit:
            # print("New primes limit: ", primes_limit)
            primes_limit = 1+val
            primes_set = set(get_primes(primes_limit))
        if not val in primes_set:
            break

        i += 1
    return (i, primes_limit, primes_set)

def primes_no_just(coef_a, coef_b, primes_set, primes_limit):
    (nb_max, primes_limit, primes_set) = primes_no(coef_a, coef_b, primes_set, primes_limit)
    return nb_max

def solve_problem(limit_coef):

    coef_max_a = 0
    coef_max_b = 0
    (nb_max, primes_limit, primes_set) = primes_no(coef_max_a, coef_max_b, None, 0)

    for a in range(-limit_coef+1, limit_coef):
        for b in range(-limit_coef, limit_coef+1):
            (nb, primes_limit, primes_set) = primes_no(a, b, primes_set, primes_limit)
            if nb > nb_max:
                nb_max = nb
                coef_max_a = a
                coef_max_b = b
                # print("New max: ", nb_max, coef_max_a, coef_max_b)

    return (coef_max_a, coef_max_b)

# https://www.hackerrank.com/contests/projecteuler/challenges/euler027
def parse_input():
    coef_limit = int(input().strip())
    (coef_max_a, coef_max_b) = solve_problem(coef_limit)
    print(coef_max_a, coef_max_b)

def problem():
    (coef_max_a, coef_max_b) = solve_problem(1000)
    print(coef_max_a*coef_max_b)

def debug_assertions():
    primes = set(get_primes(10000))

    assert primes_no_just(-7, -7, primes, 10000) == 8
    assert primes_no_just(-17, 89, primes, 10000) == 25
    assert primes_no_just(-15, 97, primes, 10000) == 48
    assert primes_no_just(1, 41, primes, 10000) == 40
    assert primes_no_just(-61, 971, primes, 10000) == 71
    assert primes_no_just(-79, 1601, primes, 10000) == 80

def main():
    debug_assertions()

    # parse_input()
    # problem()

if __name__ == "__main__":
    main()
