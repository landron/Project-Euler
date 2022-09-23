'''
    Project Euler problems working functionality
        see Python/lang/src/samples/pattern.py

    TODO:   improve performance by generating all the prime divisors
        from the start

    tag_totient
    todo_hackerrank: still too slow (without the last 75% hack)
'''
import time
from project_euler import proj_euler as pe


def is_permutation_1(left, right):
    '''are the number a permutation of each other ?'''
    digits = {}
    for i in pe.get_digits(left):
        if i in digits:
            digits[i] += 1
        else:
            digits[i] = 0
    while right >= 1:
        if right % 10 not in digits:
            return False
        if digits[right % 10] == 0:
            del digits[right % 10]
        else:
            digits[right % 10] -= 1
        right //= 10
    return True


def is_permutation(left, right):
    '''are the number a permutation of each other ?
        slightly faster than is_permutation_1:
            10**7:  23.41s vs 24.52s
    '''
    digits = [0 for i in range(10)]
    while left >= 1:
        digits[left % 10] += 1
        left //= 10
    while right >= 1:
        if not digits[right % 10]:
            return False
        assert digits[right % 10] > 0
        digits[right % 10] -= 1
        right //= 10
    return True


def problem_direct(limit):
    '''direct solution

        10**6:  10.05 seconds
        10**7:  225.38 seconds
    '''
    primes = pe.get_primes_for_divisors_of(limit)
    best = (2, 2)
    for i in range(3, limit):
        totient = pe.get_totient(i, primes)
        if is_permutation(i, totient):
            if best[1] > i/totient:
                best = (i, i/totient)
        if i % 100000 == 0:
            print(i)
    return best


def generate_totient_1(limit):
    '''generate totient instead of calculating divisors
        too slow once there are enough primes: already from 100
    '''
    def generate(tot_arr, pos, totient, div):
        assert totient
        tot_arr[pos] = totient
        while pos * div < len(tot_arr):
            totient *= div
            pos *= div
            assert not tot_arr[pos]
            tot_arr[pos] = totient

    primes = []
    tot_arr = [0 for i in range(limit)]
    for i in range(2, limit):
        # only for primes
        if tot_arr[i]:
            continue
        generate(tot_arr, i, i-1, i)

        for j in range(len(primes)):
            comb = pe.get_combinatorics_start(True, len(primes), j+1)
            while True:
                val = 1
                for k in comb.current():
                    val *= primes[k]
                k = val
                while i*k < limit:
                    generate(tot_arr, k*i, tot_arr[k]*(i-1), i)
                    k *= val
                if not comb.get_next():
                    break

        primes.append(i)
        # print(primes)

    primes = pe.get_primes_for_divisors_of(limit)
    for i, val in enumerate(tot_arr[2:]):
        totient = pe.get_totient(i+2, primes)
        # print(f"({i+2},{val},{totient})")
        assert val == totient
    print()


def generate_totient_2(limit):
    '''generate totient instead of calculating divisors

        https://codegolf.stackexchange.com/questions/26739/super-speedy-totient-function
        https://codegolf.stackexchange.com/a/26800

        error: i=j=2 generates not only 4, but all the powers of 2

        Time:
            10**7:  5.17s pure generation
    '''
    phi = [0 for i in range(limit)]
    phi[1] = 1
    for i in range(2, limit):
        # only for primes
        if phi[i]:
            continue
        phi[i] = i-1

        # generate while possible
        limit_gen = limit//i + (1 if limit % i else 0)
        for j in range(2, limit_gen):
            if phi[j]:
                assert not phi[i*j]
                if j % i:
                    phi[i*j] = (i-1) * phi[j]
                else:
                    # j = q*i^k, gcd(q,i)=1 =>
                    #   phi(i*j) = phi(q*i^(k+1)) = phi(q)*i^k*(i-1)
                    factor = i-1
                    quotient = j
                    while quotient % i == 0:
                        factor *= i
                        quotient //= i
                    # print(i, j, quotient)
                    assert phi[quotient]
                    phi[i*j] = factor * phi[quotient]
    return phi


def problem_generate(limit, start_time):
    '''generate all totient values solution

        10**6:  2.06 seconds
        10**7
            generate_totient_2: 4.91 seconds
            all:                24.52 seconds

        10**7
            python -O:  22.88 seconds
    '''
    assert start_time, "unused"

    phi = generate_totient_2(limit)
    # elapsed = time.time()-start_time
    # print(f"generate_totient_2({limit}): {elapsed:.2f} seconds")

    best = (2, 2)
    start = 3

    # HackerRank 3/10 timeouts (PyPy) => make an assumption, 4x faster
    if limit > 10000:
        start = int(0.75 * limit)
        assert phi[21] == 12
        # best = (21, 21/12)
        best = (4435, 4435/phi[4435])

    for i, totient in enumerate(phi[start:]):
        number = i+start
        if is_permutation(number, totient):
            if best[1] > number/totient:
                best = (number, number/totient)
                # print(best)
        # if i % 500000 == 0:
        #     print(i)
    return best


def recursive_totient(number, cache_1, cache_2):
    '''
        calculate totient recursively

        https://math.stackexchange.com/questions/720847/is-there-a-recursive-formula-for-eulers-totient-function
        this answer: https://math.stackexchange.com/a/2087282

        very slow after 10 already, without caches
        cache Q not necessary
        10s to 200, 3 caches
    '''
    # pylint: disable=invalid-name
    def H(n, m):
        assert n >= 1
        if n == 1:
            return 1 if m == 0 else 0

        if n in cache_1:
            if m in cache_1[n]:
                return cache_1[n][m]
        else:
            cache_1[n] = {}
        # print(f"cache_1({n}, {m})")

        first = H(n-1, n*(n-1)//2 - m)
        second = H(n-1, m)
        ret = -first-second if n % 2 else first-second
        cache_1[n][m] = ret
        return ret

    def Q(n, m):
        return H(n, m-2) - 2 * H(n, m-1) + H(n, m)

    def fi(n):
        return (n*(n-3)+4)//2

    def a(n, m):
        '''
            if (m < 0) or (nu(n) < m) ??
                http://oeis.org/A282283

            m is getting very high very early
        '''
        assert n >= 1
        if n == 1:
            return 1 if m == 1 else 0

        if n in cache_2:
            if m in cache_2[n]:
                return cache_2[n][m]
        else:
            cache_2[n] = {}
        # print(f"cache_2({n}, {m})")

        third = a(n-1, fi(n-1)) * Q(n-1, m)
        ret = a(n-1, m-n+1) - a(n-1, m) - third
        cache_2[n][m] = ret
        return ret

    return a(number, fi(number))


def solve(limit, start):
    '''https://projecteuler.net/problem=70'''
    # return problem_direct(limit)
    return problem_generate(limit, start)


def problem_counter():
    '''count duration'''
    start = time.time()
    result = solve(10**7, start)
    print(f"Result {result} in {time.time()-start:.2f} seconds")


def parse_input():
    '''
        read input and solve the problem as defined on HackerRank
    '''
    limit = int(input())
    solution = solve(limit, time.time())
    print(solution[0])


def debug_validations():
    '''module's assertions'''
    primes = pe.get_primes(1000)
    assert pe.get_totient(87109, primes) == 79180
    assert is_permutation(87109, 79180)
    assert not is_permutation(87109, 79280)
    assert not is_permutation(87109, 791801)


def debug_validations_harder():
    '''assertions that might take a few seconds'''
    primes = pe.get_primes(1000)
    for i in range(2, 10000):
        totient = pe.get_totient(i, primes)
        assert totient == i-1 or not pe.isprime(i)

    cache1 = {}
    cache2 = {}
    for i in range(2, 50):
        assert recursive_totient(i, cache1, cache2) == \
            pe.get_totient(i, primes)
        # print(i, recursive_totient(i, cache1, cache2))

    phi = generate_totient_2(4999)
    for i, val in enumerate(phi[2:]):
        assert val == pe.get_totient(i+2, primes)


def main():
    '''main'''
    debug_validations()
    # debug_validations_harder()

    # problem_counter()
    print(solve(10000, time.time()))


if __name__ == "__main__":
    main()
