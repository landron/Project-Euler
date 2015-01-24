"""
    Project Euler problems common functionality

    pylint.bat --version
        No config file found, using default configuration
        pylint 1.4.0,
        astroid 1.3.2, common 0.63.2
        Python 3.4.2 (v3.4.2:ab2c023a9432, Oct  6 2014, 22:15:05) [MSC v.1600 32 bit (Intel)]
    Your code has been rated at 10.00/10

"""
import math

def get_primes(limit):
    """get the list of primes until the given limit
            returns the list of them
        it uses the good ol' sieve of Eratosthenes, ! there are better solutions
    """

    # initialization
    #   ? one step initialization
    primes = [0 for i in range(limit)]
    for i in range(3, limit, 2):
        primes[i] = i
    primes[2] = 2

    limit_of_sieve = limit
    # You only need to start crossing out multiples at p^2, because any
    # smaller multiple of p has a prime divisor less than p and has already
    # been crossed out as a multipleof that.
    limit_of_sieve = 1 + math.floor(math.sqrt(limit))

    # sieve of Eratosthenes
    for i in range(3, limit_of_sieve, 2):
        if primes[i]:
            for j in range(i*i, limit, 2*i):
                primes[j] = 0

    # eliminate zeros
    primes = [i for i in primes if i != 0]

    return primes
