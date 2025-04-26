"""
Project Euler problems common functionality
    primes, divisors

Functions:
    get_primes
    get_divisors (needs all the primes section)
    get_digits

    get_totient

    Combinatorics
        k-permutations & combinations

Reference:
    divisors:       problem_12_smallest_triangular
    get_totient:    p72_totient_summatory.py

\todo better organize it (namespace ?)

pylint, flake8
"""

import math
import itertools

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
            for j in range(i * i, limit, 2 * i):
                primes[j] = 0

    # eliminate zeros
    primes = [i for i in primes if i != 0]

    return primes


def get_primes_2(limit):
    """minor optimization version of the previous"""
    # not rounded since we skip 1 & 2
    primes = [i * 2 + 3 for i in range(limit // 2 - 1)]
    limit_of_sieve = 1 + math.floor(math.sqrt(limit))
    for i in range(3, limit_of_sieve, 2):
        if primes[i // 2 - 1]:
            for j in range(i * i, limit, 2 * i):
                primes[j // 2 - 1] = 0
    return [2] + [i for i in primes if i != 0]


def get_primes_limits(limit_inf, limit_sup):
    """get the prime numbers in an interval (but used ?)"""
    primes = list(range(limit_inf, limit_sup))
    # print(primes)
    limit_of_sieve = 1 + math.floor(math.sqrt(limit_sup))

    for i in range(3, limit_of_sieve, 2):
        remainder = limit_inf % i
        inf = limit_inf
        if remainder != 0:
            inf = limit_inf - remainder + i
        for j in range(inf, limit_sup, i):
            if j != i:
                primes[j - limit_inf] = 0
    remainder = limit_inf % 2
    inf = limit_inf
    if remainder != 0:
        inf = limit_inf - remainder + 2
    for j in range(inf, limit_sup, 2):
        if j != 2:
            primes[j - limit_inf] = 0
    if limit_inf <= 1:
        primes[1 - limit_inf] = 0

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


def is_prime(n):  # pylint: disable=invalid-name
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
    limit = 1 + math.floor(math.sqrt(n))
    while i < limit:
        if n % i == 0:
            return False

        i += w
        w = 6 - w  # pylint: disable=invalid-name

    return True


def __get_power(number, prime):
    """gets the maximal power of the prime that divides the number"""
    if number % prime:
        return number, 0
    power = 1
    divisor = prime * prime
    while number % divisor == 0:
        divisor *= prime
        power += 1
    return number // (divisor // prime), power


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
        #   a final (prime) divisor (like 7 in 28)
        divisors.append((number, 1))
    return divisors


def get_totient(number, primes):
    """
    In number theory, Euler's totient function counts the positive
    integers up to a given integer n that are relatively prime to n.

    using get_prime_divisors is significantly slower

    Reference
        p72_totient_summatory.py
        https://projecteuler.net/problem=72

        https://en.wikipedia.org/wiki/Euler%27s_totient_function
    """

    def get_prime_divisors_list(number, primes):
        """
        get the set of divisors for a number

        like get_prime_divisors, but without powers
        """
        assert number > 1
        assert primes
        limit = 1 + math.floor(math.sqrt(number))
        divisors = set()
        for prime in primes:
            if limit < prime:
                break
            while number % prime == 0:
                number //= prime
                divisors.add(prime)
        if number > 1:
            divisors.add(number)
        return divisors

    divisors = get_prime_divisors_list(number, primes)

    def euler_formula(number, divisors):
        """why not directly product ?
        This does not use powers
        https://en.wikipedia.org/wiki/Euler%27s_totient_function#Euler's_product_formula
        """
        numerator = number
        denominator = 1
        for i in divisors:
            numerator *= i - 1
            denominator *= i
        assert numerator % denominator == 0
        return numerator // denominator

    return euler_formula(number, divisors)


def get_divisors_as_primes(number, primes=None):
    """get the divisors of a given number as a list of primes and powers"""
    if not primes:
        primes = get_primes_for_divisors_of(number)
    return get_prime_divisors(number, primes)


def get_divisors(number, primes=None):
    """get all the divisors of a given number"""
    divisors_and_powers = get_divisors_as_primes(number, primes)

    # each element is a prime with all the possible powers
    # Ex.: 3150 [[2], [3, 9], [5, 25], [7]]
    divisors_expanded = []
    for item in divisors_and_powers:
        divisors_expanded.append([item[0] ** (i + 1) for i in range(item[1])])

    divisors = []
    # 0 generates [1]
    for i in range(1 + len(divisors_expanded)):
        # combinations of divisors_expanded of size i
        for item in itertools.combinations(divisors_expanded, i):
            # cartesian product of the combination item
            for j in list(itertools.product(*item)):
                prod = 1
                for k in j:
                    prod *= k
                divisors.append(prod)

    divisors = sorted(divisors)
    return divisors


####################################################
# combinatorics


class Combinatorics:
    """
    Generate k-permutations & combinations
    """

    def __init__(self, is_combinations, limit, limit_subset=0):
        """
        initialization
        taken = used indexes (each index appears one time only)
        """
        self.is_combinations = is_combinations

        assert limit_subset <= limit
        if limit_subset == 0:
            limit_subset = limit

        self.taken = [False] * limit
        self.indexes = []

        for i in range(limit_subset):
            self.indexes.append(i)
            self.taken[i] = True

    def get_limit(self):
        """
        the superior limit of our groupings
        """
        return len(self.taken)

    def get_limit_subset(self):
        """
        the count of our generated set
        """
        return len(self.indexes)

    def current(self):
        """
        current permutation/combination
        """
        return self.indexes

    @staticmethod
    def get_combinatorics_next(indexes, taken, is_combinations):
        """
        P(n,k) = k-permutations of n
            Number (n, k) = n! / (n-k)!
        k-combination of a set

        n & k are deduced (not explicitly set):
            n = len(taken)
            k = len(indexes)
        """
        assert is_combinations in [True, False]
        assert indexes and taken

        max_i = len(indexes) - 1
        limit = len(taken)
        assert indexes[max_i] < limit

        i = max_i

        found = False
        while not found:
            found = True

            # propagate the value change
            #   if the limit is reached, we increment the previous digits
            #   (like for a number base "limit")

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
            assert indexes[i] != limit, "test"

            taken[indexes[i]] = True

            # give proper values to the remaining

            if not is_combinations:
                next_free = 0
                for j in range(i + 1, max_i + 1):
                    while taken[next_free]:
                        next_free += 1
                        assert next_free != limit
                    taken[next_free] = True
                    indexes[j] = next_free
            else:
                # taken ignored
                for j in range(i + 1, max_i + 1):
                    indexes[j] = indexes[j - 1] + 1
                    if indexes[j] == limit:
                        found = False
                        break

        # print(indexes, taken)

        return True

    def get_next(self):
        """
        get the next combination/permutation
        """
        if not Combinatorics.get_combinatorics_next(
            self.indexes, self.taken, self.is_combinations
        ):
            self.indexes = []
            return None
        return self.current()

    def next(self):
        """convenient alias"""
        return self.get_next()


def get_combinatorics_start(is_combinatorics, limit, limit_subset=0):
    """
    limit, limit_subset = (usually known as) n, k
        P(n,k) = k-permutations of n
    """
    return Combinatorics(is_combinatorics, limit, limit_subset)


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
    """
    get the digits of the given number in the given base

    Return
        the result is in reversed order
            use reversed to run trough in ascending order
    """
    digits = []
    while number >= 1:
        digits.append(number % base)
        number //= base
    return digits if digits else [0]


def combine_numbers(numbers, revert=False):
    """get the number from the given numbers"""
    number = 0
    size = len(numbers)
    for i in range(size):
        current = numbers[i] if not revert else numbers[size - i - 1]
        number *= 10 ** number_of_digits(current)
        number += current
    return number


def get_number(digits, revert=False):
    """get the number from the digits"""
    number = 0
    size = len(digits)
    for i in range(size):
        number *= 10
        number += digits[i] if not revert else digits[size - i - 1]
    return number


####################################################


def debug_combinatorics(is_combinations, limit, subset_limit, print_it):
    """
    debug function to test combinations & permutations
    """
    combination = get_combinatorics_start(is_combinations, limit, subset_limit)
    if print_it:
        print(combination.current())

    cnt = 1
    while combination.get_next():
        if print_it:
            print(combination.current())
        cnt += 1

    return cnt


def debug_get_permutations(limit, subset_limit=0, print_it=False):
    """
    debug function to test permutations
    """
    return debug_combinatorics(False, limit, subset_limit, print_it)


def debug_get_combinations(limit, subset_limit=0, print_it=False):
    """
    debug function to test combinations
    """
    return debug_combinatorics(True, limit, subset_limit, print_it)


def debug_validations():
    """module's assertions"""
    assert [
        1,
        2,
        3,
        5,
        6,
        7,
        9,
        10,
        14,
        15,
        18,
        21,
        25,
        30,
        35,
        42,
        45,
        50,
        63,
        70,
        75,
        90,
        105,
        126,
        150,
        175,
        210,
        225,
        315,
        350,
        450,
        525,
        630,
        1050,
        1575,
        3150,
    ] == get_divisors(3150)
    assert [1, 2, 3, 4, 6, 11, 12, 22, 33, 44, 66, 132] == get_divisors(132)
    assert [1, 2, 3, 4, 6, 8, 9, 12, 16, 18, 24, 36, 48, 72, 144] == get_divisors(144)
    assert [1, 2, 4, 8, 16, 32, 64] == get_divisors(64)
    assert [1, 2, 3, 4, 6, 8, 12, 16, 24, 48] == get_divisors(48)
    assert get_divisors(21) == [1, 3, 7, 21]

    assert number_of_digits(7) == 1
    assert number_of_digits(7567) == 4
    assert get_digits(1037567) == [7, 6, 5, 7, 3, 0, 1]
    assert get_digits(7567, 8) == [7, 1, 6, 6, 1]

    # add print_it=True to see them
    assert debug_get_permutations(2) == 2
    assert debug_get_permutations(3) == 6
    assert debug_get_permutations(4) == 24

    assert debug_get_permutations(3, 2) == 6
    assert debug_get_permutations(2, 1) == 2
    assert debug_get_permutations(3, 1) == 3
    assert debug_get_permutations(4, 2) == 12
    assert debug_get_permutations(4, 3) == 24

    assert debug_get_combinations(3, 3) == 1
    assert debug_get_combinations(5, 5) == 1
    assert debug_get_combinations(4, 3) == 4
    assert debug_get_combinations(5, 2) == 10

    assert not is_prime(1)
    assert is_prime(2)
    assert is_prime(3)
    assert not is_prime(4)
    assert not is_prime(15)
    assert is_prime(131)
    assert is_prime(149)
    assert not is_prime(19519)

    primes_1000 = get_primes(1000)
    # primes
    assert get_totient(2, primes_1000) == 1
    assert get_totient(5, primes_1000) == 4
    assert get_totient(11, primes_1000) == 10
    assert get_totient(37, primes_1000) == 36
    # not primes
    assert get_totient(6, primes_1000) == 2
    assert get_totient(12, primes_1000) == 4
    assert get_totient(15, primes_1000) == 8
    assert get_totient(16, primes_1000) == 8
    assert get_totient(22, primes_1000) == 10
    assert get_totient(34, primes_1000) == 16
    assert get_totient(35, primes_1000) == 24
    assert get_totient(36, primes_1000) == 12
    # vs 15
    assert get_totient(45, primes_1000) == 24
    assert get_totient(135, primes_1000) == 72
    assert get_totient(75, primes_1000) == 40
    assert get_totient(270, primes_1000) == 72

    assert get_prime_divisors(28, primes_1000) == [(2, 2), (7, 1)]

    assert combine_numbers([1, 4, 3]) == 143
    assert combine_numbers([1, 20, 3]) == 1203
    assert combine_numbers([1, 8, 111]) == 18111


if __name__ == "__main__":
    debug_validations()

    # 4-combination of 7
    # debug_get_combinations(7, 4, print_it=True)
    # 3-permutation of 4
    # debug_get_permutations(4, 3, print_it=True)
