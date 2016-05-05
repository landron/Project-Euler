"""
    Project Euler problems working functionality
        primes, divisors
    Version: 2016.01.17

    pylint --version
        No config file found, using default configuration
        pylint 1.5.2,
        astroid 1.4.3
        Python 3.5.1 (v3.5.1:37a07cee5969, Dec  6 2015, 01:38:48) [MSC v.1900 32 bit (Intel)]

"""
import proj_euler

def fi_base(limit, no_primes, primes_n):
    # print(limit,no_primes)
    assert limit > 0
    assert no_primes >= 0

    if no_primes == 0:
        return limit
    result = fi_base(limit, no_primes-1, primes_n)
    result -= fi_base(int(limit/primes_n[no_primes-1]), no_primes-1, primes_n)
    return result

 # Let p_1, p_2,...,p_n be the first n primes and denote by \Phi(m,n) the number of natural\
 #  numbers not greater than m which are divisible by no p_i.
 # http://en.wikipedia.org/wiki/Prime-counting_function, Ernst Meissel
def fi(limit, no_primes):
    prob7_module = __import__("Problems 7 & 10 - 10001st prime")
    primes_n = proj_euler.get_primes(1+prob7_module.find_prime_number(no_primes))
    # print(primes_n)
    assert no_primes == len(primes_n)
    return int(fi_base(limit, no_primes, primes_n))

def debug_validations():
    """module's assertions"""

def main():
    '''main: defined here to avoid scope problems'''
    debug_validations()

    # print(fi(17, 2))
    prob7_module = __import__("problem_19_couting_sundays")
    prob7_module.main()

if __name__ == "__main__":
    main()
