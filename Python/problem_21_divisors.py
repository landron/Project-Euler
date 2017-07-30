#!/bin/python3
'''    
    https://projecteuler.net/problem=21
        https://www.hackerrank.com/contests/projecteuler/challenges/euler021
'''

import sys
import math

####################################################
# switch between project euler and hackerrank
import proj_euler
import itertools

########################################################################################################################

def get_primes_2(limit):
    """minor optimization version of the previous"""
    # not rounded since we skip 1 & 2
    primes = [i*2+3 for i in range(limit//2-1)]
    limit_of_sieve = 1+math.floor(math.sqrt(limit))
    for i in range(3, limit_of_sieve, 2):
        if primes[i//2-1]:
            for j in range(i*i, limit, 2*i):
                primes[j//2-1] = 0
    return [2]+[i for i in primes if i != 0]


def __get_power(number, prime):
    """gets the maximal power of the prime that divides the number"""
    if number%prime != 0:
        return (number, 0)
    power = 1
    divisor = prime*prime
    while number%divisor == 0:
        divisor *= prime
        power += 1
    return (number//int(divisor/prime), power)

def get_prime_divisors(number, primes):
    """get the prime divisors of a given number
            the sqrt(number) is enough for the limit of the primes because
                we consider the remainder, a last "big" prime number
    """
    assert number > 1
    assert primes
    limit = 1 + math.floor(math.sqrt(number))
    divisors = []
    for prime in primes:
        if limit < prime:
            break
        (number, power) = __get_power(number, prime)
        if power != 0:
            divisors.append((prime, power))
        if number == 1:
            break
    if number != 1:
        #   a prime number
        divisors.append((number, 1))
    return divisors

def proj_euler_get_primes(limit):
    """get the list of primes until the given limit
            returns the list of them
    """
    return get_primes_2(limit)

def get_divisors_as_primes(number, primes=None):
    """get the divisors of a given number as a list of primes and powers"""
    if not primes:
        primes = get_primes(1 + math.floor(math.sqrt(number)))
    return get_prime_divisors(number, primes)

def proj_euler_get_divisors(number, primes=None):
    """get all the divisors of a given number"""
    divisors_and_powers = get_divisors_as_primes(number, primes)

    divisors_expanded = []
    for item in divisors_and_powers:
        divisors_expanded.append([item[0]**(i+1) for i in range(item[1])])

    divisors = []
    for i in range(1+len(divisors_expanded)):
        for item in itertools.combinations(divisors_expanded, i):
            for j in list(itertools.product(*item)):
                prod = 1
                for k in j:
                    prod *= k
                divisors.append(prod)

    divisors = sorted(divisors)
    return divisors

########################################################################################################################

def get_proper_divisor(n, primes, get_divisors_func):
    divs = get_divisors_func(n, primes)

    assert len(divs) >= 2
    if len(divs) == 2:
        return 0
    # eliminate the number itself
    divs[-1] = 0
    return sum(divs)

def sum_of_amicable(primes, n, get_divisors_func):
    sum = 0
    for i in range(4, n):
        proper_divisor_1 = get_proper_divisor(i, primes, get_divisors_func)
        if proper_divisor_1 == 0:   # prime number
            continue
        if proper_divisor_1 == i:   # amicable to itself number = perfect number
            continue
        proper_divisor_2 = get_proper_divisor(proper_divisor_1, primes, get_divisors_func)
        if proper_divisor_2 != i:
            continue

        # print(i, proper_divisor_1)
        sum += i    # only our number, not the other one
    return sum

def debug_assertions(primes):
    assert get_proper_divisor(220, primes) == 284 
    assert get_proper_divisor(284, primes) == 220

def project_euler_test():
    n = 10000
    # n is too much
    primes = proj_euler.get_primes(n)

    # debug_assertions(primes)

    sum = sum_of_amicable(primes, n, proj_euler.get_divisors)
    print(sum)

'''
    https://www.hackerrank.com/contests/projecteuler/challenges/euler021/:  33.33 / 100
'''
def WIP_parse_input():
    T = int(input().strip())

    primes = None
    limit = 0
    for _ in range(T):
        N = int(input().strip())
        if N > limit:
            limit = N
            primes = proj_euler_get_primes(limit)
        sum = sum_of_amicable(primes, N, proj_euler_get_divisors)
        print(sum)

def main():
    project_euler_test()
    # WIP_parse_input()

if __name__ == "__main__":
    main()
