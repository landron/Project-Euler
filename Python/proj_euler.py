"""
    Project Euler problems common functionality
    Version: 2016.01.2

    Reference:
        divisors:   problem_12_smallest_triangular

    pylint --version
        No config file found, using default configuration
        pylint 1.5.2,
        astroid 1.4.3
        Python 3.5.1 (v3.5.1:37a07cee5969, Dec  6 2015, 01:38:48) [MSC v.1900 32 bit (Intel)]
    Your code has been rated at 10.00/10

"""
import math
import itertools

def get_primes_1(limit):
    """get the list of primes until the given limit
            returns the list of them
        it uses the good ol' sieve of Eratosthenes
            not optimized: keep it for reference!
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

def get_primes(limit):
    """get the list of primes until the given limit
            returns the list of them
    """
    return get_primes_2(limit)

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
            the sqrt(number) is enough for the limit of the primes
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

def get_divisors_as_primes(number):
    """get the divisors of a given number as a list of primes and powers"""
    primes = get_primes(1 + math.floor(math.sqrt(number)))
    return get_prime_divisors(number, primes)

def get_divisors(number):
    """get the divisors of a given number as a list of primes and powers"""
    divisors_and_powers = get_divisors_as_primes(number)
    # print(divisors_and_powers)
    divisors1 = []
    for item in divisors_and_powers:
        divisors1.append([item[0]**(i+1) for i in range(item[1])])

    divisors = []
    for i in range(1+len(divisors1)):
        for item in itertools.combinations(divisors1, i):
            for j in list(itertools.product(*item)):
                prod = 1
                for k in j:
                    prod *= k
                divisors.append(prod)

    divisors = sorted(divisors)
    return divisors

def debug_validations():
    """module's assertions"""
    assert [1, 2, 3, 5, 6, 7, 9, 10, 14, 15, 18, 21, 25, 30, 35, 42, 45, 50, 63, 70, 75, 90, \
    105, 126, 150, 175, 210, 225, 315, 350, 450, 525, 630, 1050, 1575, 3150] == get_divisors(3150)
    assert [1, 2, 3, 4, 6, 11, 12, 22, 33, 44, 66, 132] == get_divisors(132)
    assert [1, 2, 3, 4, 6, 8, 9, 12, 16, 18, 24, 36, 48, 72, 144] == get_divisors(144)
    assert [1, 2, 4, 8, 16, 32, 64] == get_divisors(64)
    assert [1, 2, 3, 4, 6, 8, 12, 16, 24, 48] == get_divisors(48)

if __name__ == "__main__":
    debug_validations()
