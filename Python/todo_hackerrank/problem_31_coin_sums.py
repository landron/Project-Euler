#!/bin/python3
'''
    tag_primes

    https://projecteuler.net/problem=31
        How many different ways can £2 be made using any number of coins?

    https://www.hackerrank.com/contests/projecteuler/challenges/euler031
        solve_problem_recursive_1   :   0
        solve_problem_recursive_2   :   25.00 ; 1 wrong answer + 5 timeouts
            also found in problem overview
        solve_problem_recursive_3   :   same 25.00, even if improved
        todo_hackerrank

    pylint 1.5.5
        Your code has been rated at 8.78/10.
'''

COINS = [1, 2, 5, 10, 20, 50, 100, 200]

##################################################################################################
#   hackerrank : 0

def get_sum_dbg(coins):
    assert len(COINS) == len(coins)
    sum_of = 0
    for i, coin_val in enumerate(COINS):
        sum_of += coins[i]*coin_val
    return sum_of

def solve_problem_recursive_1(initial_dbg, pences, coins, position):
    assert coins[position] == 0
    # coins[position] = 0

    if position == 0 or pences == 0:
        if pences%COINS[position] != 0:
            return 0
        coins[position] = pences//COINS[position]
        # print(coins.tolist())
        assert get_sum_dbg(coins) == initial_dbg
        coins[position] = 0
        return 1

    # try without the current coin first
    possibilities = solve_problem_recursive_1(initial_dbg, pences, coins, position-1)
    while pences >= COINS[position]:
        pences -= COINS[position]
        coins[position] += 1
        possibilities += solve_problem_recursive_1(initial_dbg, pences, coins, position-1)

    coins[position] = 0
    return possibilities

# this variant does not generate all the possibilities; it uses a cache
def solve_problem_recursive_2(already_calculated, pences, position):
    if position == 0 or pences == 0:
        # first position is 1 pence => can express everything
        return 1

    if pences in already_calculated[position]:
        possibilities = already_calculated[position][pences]
        # print("Found in cache: ", position, pences, "->", possibilities)
        return possibilities
    pences_in = pences

    # try without the current coin first
    possibilities = solve_problem_recursive_2(already_calculated, pences, position-1)
    while pences >= COINS[position]:
        pences -= COINS[position]
        possibilities += solve_problem_recursive_2(already_calculated, pences, position-1)

    already_calculated[position][pences_in] = possibilities

    return possibilities

##################################################################################################

# this variant does not generate all the possibilities; it uses a cache
def solve_problem_recursive_3(already_calculated, pences, position):
    if position == 0 or pences == 0:
        # first position is 1 pence => can express everything
        return 1

    if pences in already_calculated[position]:
        possibilities = already_calculated[position][pences]
        # print("Found in cache: ", position, pences, "->", possibilities)
        return possibilities
    pences_in = pences

    # try without the current coin first
    possibilities = solve_problem_recursive_3(already_calculated, pences, position-1)
    while pences >= COINS[position]:
        pences -= COINS[position]
        if pences in already_calculated[position]:
            # print("Found in cache 2: ", position, pences, "->", possibilities)
            possibilities += already_calculated[position][pences]
            break
        else:
            # it will also add in cache
            possibilities += solve_problem_recursive_3(already_calculated, pences, position-1)

    already_calculated[position][pences_in] = possibilities

    return possibilities

def solve_problem(pences):
    types = len(COINS)

    already_calculated = []
    for _ in range(types):
        already_calculated.append({})

    # return solve_problem_recursive_1(pences, pences, array('I', types*[0]), types-1)
    # return solve_problem_recursive_2(already_calculated, pences, types-1)
    return solve_problem_recursive_3(already_calculated, pences, types-1)

# https://www.hackerrank.com/contests/projecteuler/challenges/euler031
def parse_input():
    cases = int(input().strip())
    for _ in range(cases):
        sum_to_solve = int(input().strip())
        print(solve_problem(sum_to_solve))

def problem():
    print(solve_problem(200))

def debug_assertions():
    assert solve_problem(10) == 11
    assert solve_problem(15) == 22
    assert solve_problem(20) == 41

def main():
    debug_assertions()

    # parse_input()
    problem()

if __name__ == "__main__":
    main()
