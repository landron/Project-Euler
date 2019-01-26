"""
    Project Euler problems common functionality
        primes, divisors
    Version: 2018.12.30

    Reference:
        divisors:   problem_12_smallest_triangular

    pylint, flake8

    Functions:
        get_primes
        get_divisors (needs all the primes section)
        get_digits
        permutation

    \todo better organize it (namespace ?) & simplify use (see permutations)
"""
import math
import itertools

__version__ = "1.0.1"

####################################################
# primes


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


def get_primes_limits(limit_inf, limit_sup):
    """get the prime numbers in an interval (but used ?)"""
    primes = [i for i in range(limit_inf, limit_sup)]
    # print(primes)
    limit_of_sieve = 1+math.floor(math.sqrt(limit_sup))

    for i in range(3, limit_of_sieve, 2):
        remainder = limit_inf % i
        inf = limit_inf-remainder+i if remainder != 0 else limit_inf-remainder
        for j in range(inf, limit_sup, i):
            if j != i:
                primes[j-limit_inf] = 0
    remainder = limit_inf % 2
    inf = limit_inf-remainder+2 if remainder != 0 else limit_inf-remainder
    for j in range(inf, limit_sup, 2):
        if j != 2:
            primes[j-limit_inf] = 0
    if limit_inf <= 1:
        primes[1-limit_inf] = 0

    primes = [i for i in primes if i != 0]

    return primes


def get_primes(limit):
    """get the list of primes until the given limit
            returns the list of them
    """
    return get_primes_2(limit)


def get_primes_for_divisors_of(limit):
    """
        Get the list of primes until the greatest possible
        divisor of the given limit.

        Returns the list of these prime numbers.

        ATTENTION: this does not include all the prime numbers smaller
            than the given limit!
    """
    return get_primes(1 + math.floor(math.sqrt(limit)))


def isprime(n):  # pylint: disable=invalid-name
    """Returns True if n is prime.

        Reference
            "a variant of the classic O(sqrt(N)) algorithm. It uses the fact
            that a prime (except 2 and 3) is of form 6k - 1 or 6k + 1 and
            looks only at divisors of this form"
            https://stackoverflow.com/questions/1801391/what-is-the-best-algorithm-for-checking-if-a-number-is-prime

        Next:
            - AKS primality test (Agrawal–Kayal–Saxena primality test)
            - Miller-Rabin test
    """
    assert n > 0
    if n < 4:
        return n != 1
    if n % 2 == 0:
        return False
    if n % 3 == 0:
        return False

    i = 5
    w = 2  # pylint: disable=invalid-name

    # while i * i <= n:
    limit = 1+math.floor(math.sqrt(n))
    while i < limit:
        if n % i == 0:
            return False

        i += w
        w = 6 - w  # pylint: disable=invalid-name

    return True


def __get_power(number, prime):
    """gets the maximal power of the prime that divides the number"""
    if number % prime:
        return (number, 0)
    power = 1
    divisor = prime*prime
    while number % divisor == 0:
        divisor *= prime
        power += 1
    return number//(divisor//prime), power


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
        number, power = __get_power(number, prime)
        if power != 0:
            divisors.append((prime, power))
        if number == 1:
            break
    if number != 1:
        #   a prime number
        divisors.append((number, 1))
    return divisors


def get_divisors_as_primes(number, primes=None):
    """get the divisors of a given number as a list of primes and powers"""
    if not primes:
        primes = get_primes_for_divisors_of(number)
    return get_prime_divisors(number, primes)


def get_divisors(number, primes=None):
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

####################################################
# combinatorics


def get_permutation_next(indexes, taken, limit):
    '''
        Number (N, K) = N! / (N-K)!
    '''
    assert indexes
    max_i = len(indexes)-1
    assert indexes[max_i] < limit

    i = max_i

    # propagate the value change
    taken[indexes[i]] = False
    indexes[i] += 1

    while indexes[i] == limit or taken[indexes[i]]:
        if indexes[i] == limit:
            if i == 0:
                return False
            i -= 1
            # available now
            taken[indexes[i]] = False
        indexes[i] += 1

    taken[indexes[i]] = True

    # give proper values to the remaining

    next_free = 0
    for j in range(i+1, max_i+1):
        while taken[next_free]:
            next_free += 1
            assert next_free != limit
        taken[next_free] = True
        indexes[j] = next_free

    # print(indexes, taken)

    return True


def get_permutation_start(indexes, taken, limit, subset=0):
    '''
        initialisation; taken = used indexes (each index appears one time only)

        limit, subset = (usually known as) N, K
    '''
    if subset == 0:
        subset = limit

    # not like this: it will create another list
    # taken = [False] * limit
    for i in range(limit):
        taken.append(False)

    for i in range(subset):
        indexes.append(i)
        taken[i] = True

####################################################
# generic


def number_of_digits(number, base=10):
    """get the number of the digits of the given number in the given base"""
    digits = 0
    while number >= 1:
        number //= base
        digits += 1
    return digits


def get_digits(number, base=10):
    '''
        get the digits of the given number in the given base

        Return
            the result is in reversed order
    '''
    digits = []
    while number >= 1:
        digits.append(number % base)
        number //= base
    return digits


def get_number(digits, revert=False):
    """get the number from the digits"""
    number = 0
    size = len(digits)
    for i in range(size):
        number *= 10
        number += digits[i] if not revert else digits[size-i-1]
    return number

####################################################


def debug_get_permutations(limit, subset_limit=0, print_it=False):
    """
        debug function to test permutations
        \todo: simplify the usage of this API
    """
    # pylint: disable=invalid-name

    N = limit
    K = subset_limit

    a = []
    temp = []
    get_permutation_start(a, temp, N, K)
    if print_it:
        print(a)

    cnt = 1
    while get_permutation_next(a, temp, N):
        if print_it:
            print(a)
        cnt += 1

    return cnt


def debug_validations():
    ''' module's assertions'''
    assert [1, 2, 3, 5, 6, 7, 9, 10, 14, 15, 18, 21, 25, 30, 35, 42, 45, 50,
            63, 70, 75, 90, 105, 126, 150, 175, 210, 225, 315, 350, 450, 525,
            630, 1050, 1575, 3150] == get_divisors(3150)
    assert [1, 2, 3, 4, 6, 11, 12, 22, 33, 44, 66, 132] == get_divisors(132)
    assert [1, 2, 3, 4, 6, 8, 9, 12, 16, 18, 24, 36, 48, 72, 144] == \
        get_divisors(144)
    assert [1, 2, 4, 8, 16, 32, 64] == get_divisors(64)
    assert [1, 2, 3, 4, 6, 8, 12, 16, 24, 48] == get_divisors(48)
    assert get_divisors(21) == [1, 3, 7, 21]

    assert number_of_digits(7) == 1
    assert number_of_digits(7567) == 4
    assert get_digits(1037567) == [7, 6, 5, 7, 3, 0, 1]
    assert get_digits(7567, 8) == [7, 1, 6, 6, 1]

    assert debug_get_permutations(2) == 2
    assert debug_get_permutations(3) == 6
    assert debug_get_permutations(4) == 24

    assert debug_get_permutations(3, 2) == 6
    assert debug_get_permutations(2, 1) == 2
    assert debug_get_permutations(3, 1) == 3
    assert debug_get_permutations(4, 2) == 12

    assert not isprime(1)
    assert isprime(2)
    assert isprime(3)
    assert not isprime(15)
    assert isprime(131)
    assert isprime(149)
    assert not isprime(19519)


if __name__ == "__main__":
    debug_validations()
