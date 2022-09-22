'''
    Project Euler problems working functionality
        see Python/lang/src/samples/pattern.py

    TODO:   improve performance by generating all the prime divisors
        from the start
'''
import time
from project_euler import proj_euler as pe


def is_permutation(left, right):
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


def problem_direct(limit):
    '''direct solution'''
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


def generate_totient(limit):
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


def problem(limit):
    '''https://projecteuler.net/problem=70'''
    return problem_direct(limit)


def problem_counter():
    '''count problem() duration

        10**6:  10.05 seconds
        10**7:  225.38 seconds
    '''
    start = time.time()
    result = problem(10**7)
    print(f"Result {result} in {time.time()-start:.2f} seconds")


def debug_validations():
    '''module's assertions'''
    primes = pe.get_primes(1000)
    assert pe.get_totient(87109, primes) == 79180
    assert is_permutation(87109, 79180)
    assert not is_permutation(87109, 79280)
    assert not is_permutation(87109, 791801)

    for i in range(2, 10000):
        totient = pe.get_totient(i, primes)
        assert totient == i-1 or not pe.isprime(i)


def main():
    '''main'''
    debug_validations()
    # problem_counter()

    generate_totient(50)


if __name__ == "__main__":
    main()
