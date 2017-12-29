#! /usr/bin/python3
'''
    This problem was a crazy story, such a blast!
        Done in 2018, during two distant sessions. 2017/12/29

    https://projecteuler.net/problem=31
        How many different ways can £2 be made using any number of coins?

    https://www.hackerrank.com/contests/projecteuler/challenges/euler031
        solve_problem_recursive_1   :   0
        solve_problem_recursive_2   :   25.00 ; 1 wrong answer + 5 timeouts
            also found in problem overview
        solve_problem_recursive_3   :   same 25.00, even if improved

        solve_problem_precalculate  :
            using the "Investigating combinations of English currency denominations" document
             from https://projecteuler.net/problem=31
             The idea is simple: pre-calculate all the sums less than the needed one starting
             with the smaller coin

            With t = total sum, c = coin
            "The function w(t, c) can be reformulated as follows:

                w(t, c) =   1
                                if c = 1 or t = 0
                            w(t, s(c))
                                if c > 1 and t < c
                            w(t, s(c)) + w(t − c, c)
                                if c > 1 and t ≥ c

                s(c) = previous coin

        100/100:
            get_precalculated_1 did it !!!

            - cache the precalculated table for the set of tests
            - "as the result can be large, print answer mod 10^9+7"
            - get_precalculated_2 still has timeouts, even if it seemed an improvement over
                get_precalculated_1

    pylint --version
        No config file found, using default configuration
        pylint 1.8.1,
        astroid 1.6.0
        Python 3.6.4

        Your code has been rated at 9.86/10.
'''

COINS = [1, 2, 5, 10, 20, 50, 100, 200]

##################################################################################################
#   hackerrank : 0/100

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

def solve_problem_recursive_2(already_calculated, pences, position):
    '''
        no w(t, c) function use
        this variant does not generate all the possibilities; it uses a cache
    '''
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
#   hackerrank : 25/100

def solve_problem_recursive_3(already_calculated, pences, position):
    '''
        no w(t, c) function use
        this variant does not generate all the possibilities; it uses a cache
        final variant
    '''
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

def solve_problem_rec(pences):
    '''
        solve the problem recursively, without the w(t, c) function
            calculate without the last (usable) coin, then add coins of this type progressively
    '''
    types = len(COINS)

    already_calculated = []
    for _ in range(types):
        already_calculated.append({})

    # return solve_problem_recursive_1(pences, pences, array('I', types*[0]), types-1)
    # return solve_problem_recursive_2(already_calculated, pences, types-1)
    return solve_problem_recursive_3(already_calculated, pences, types-1)

##################################################################################################
#   hackerrank : 100/100
#
#       cache the precalculated table and reuse it
#       it calculates ALL the values to the needed sum, no optimization
#

def get_last_coin(pences):
    '''get last usable coin'''

    last_coin = 0
    for i, coin in enumerate(COINS):
        if coin > pences:
            break
        last_coin = i
    return last_coin

def get_precalculated_1(pences, print_it=False):
    '''build the entire cache (for all the values)'''

    precalcul = {}

    last_coin = 0
    for i, coin in enumerate(COINS):
        if coin > pences:
            break
        last_coin = i
        precalcul[i] = [0]*(1+pences)   #space for 0

    prev = -1
    for i in range(1+last_coin):
        coin = COINS[i]
        for j in range(1+pences):
            if i == 0:
                if pences % coin == 0:  # always for COINS[0]=1
                    precalcul[i][j] = 1
            elif j < coin:
                precalcul[i][j] = precalcul[prev][j]
            else:
                precalcul[i][j] = precalcul[prev][j] + precalcul[i][j-coin]
        prev = i

    if print_it:
        for i in precalcul:
            print(COINS[i], precalcul[i])

    return precalcul

def solve_problem_precalculate_all(pences, print_it=False):
    '''shortcut function: the table is not cached between calls'''
    return solve_problem_precalculated_1(pences, None, print_it)

def solve_problem_precalculated_1(pences, precalcul, print_it=False):
    '''solve the given sum using the given precalculated cache'''

    if not precalcul or len(precalcul[0]) < pences+1:
        precalcul = get_precalculated_1(pences, print_it)
    last_coin = get_last_coin(pences)

    return precalcul[last_coin][pences]

##################################################################################################
#   hackerrank : 25/100
#
#   Probably:   "RecursionError: maximum recursion depth exceeded in comparison"
#

def precalculate_rec(precalculated, pences, coin):
    '''
        calculate on demand using (unlimited) recursion
    '''

    no_possibilities = precalculated[coin][pences]
    if no_possibilities != 0:
        return no_possibilities

    assert coin != 0
    no_possibilities = precalculate_rec(precalculated, pences, coin-1)
    if pences >= COINS[coin]:
        no_possibilities += precalculate_rec(precalculated, pences-COINS[coin], coin)
    precalculated[coin][pences] = no_possibilities
    return no_possibilities

def precalculate_on_demand(pences, print_it=False):
    '''
        RecursionError: maximum recursion depth exceeded in comparison
    '''

    last_coin = 0

    precalcul = {}
    for i, coin in enumerate(COINS):
        if coin > pences:
            break
        elif i == 0:
            precalcul[i] = [1]*(1+pences)   #space for 0
        else:
            last_coin = i
            precalcul[i] = [0]*(1+pences)   #space for 0
            precalcul[i][0] = 1

    result = precalculate_rec(precalcul, pences, last_coin)

    if print_it:
        for i in precalcul:
            print(i, precalcul[i])

    return result

##################################################################################################
#   hackerrank : 0/100
#       ERROR:  precalculate_english_coins_norec(151) == 22412
#           should be 22414
#
#   adapted for English coins
#       can still be optimized: 1,2 do not need to be calculated
#       score: 0
#       no recursion

def precalculate_remainder(pences, precalcul, last_coin):
    '''
        only the remainder + last_coin values TO pences are interesting
            here we get the remainder for all coin types
    '''

    remainder = pences%COINS[last_coin]
    # print("big remainder", remainder)

    # it's enough and necessary to calculate all the values for 2 & 5
    if last_coin > 0:
        for i in range(pences+1):
            precalcul[1][i] = 1+i//2

    for i in range(2, 1+last_coin):
        start = remainder%COINS[i]
        # print("remainder", start, COINS[i])
        precalcul[i][start] = precalcul[i-1][start]
        # print(i, start, precalcul[i][start])
        for j in range(start+COINS[i], remainder+1, COINS[i]):
            precalcul[i][j] = precalcul[i-1][j] + precalcul[i][j-COINS[i]]

    if last_coin > 1:
        for i in range(remainder+5, pences+1, 5):
            precalcul[2][i] = precalcul[1][i] + precalcul[2][i-5]

 # ERROR: precalculate_english_coins_norec(151) == 22412
def precalculate_english_coins_norec(pences, print_it=False):
    '''
        hackerrank: 0

        adapted for English coins
            can still be optimized: 1,2 do not need to be calculated
            no recursion

        unfortunately, it does not work for the hackerrank cases
    '''

    last_coin = 0

    precalcul = {}
    for i, coin in enumerate(COINS):
        if coin > pences:
            break
        elif i == 0:
            precalcul[i] = [1]*(1+pences)   #space for 0
        else:
            last_coin = i
            precalcul[i] = [0]*(1+pences)   #space for 0
            precalcul[i][0] = 1

    precalculate_remainder(pences, precalcul, last_coin)

    # if print_it:
    #     for i in precalcul:
    #         print(COINS[i], precalcul[i])

    remainder = pences%COINS[last_coin]
    for j in range(3, 1+last_coin):
        for i in range(remainder+COINS[j], pences+1, COINS[j]):
            precalcul[j][i] = precalcul[j-1][i] + precalcul[j][i-COINS[j]]
        # also do ... the other 10s
        if COINS[j] == 20:
            start = (remainder+10)%20
            precalcul[j][start] = precalcul[j-1][start]
            for i in range(start+COINS[j], pences+1, COINS[j]):
                precalcul[j][i] = precalcul[j-1][i] + precalcul[j][i-COINS[j]]

    if print_it:
        for i in precalcul:
            print(COINS[i], precalcul[i])

    return precalcul[last_coin][pences]

##################################################################################################
#   hackerrank: 25/100 (probably more after the modulo correction)
#
#   #5-#8 : timeouts
#       memory optimization, but the valuer are calculated on demand
#       SO more passings through the entire table - this might be the reason
#

def get_precalculated_2(pences):
    '''build the intelligent cache:
        - always larger > 200
        - English coins knowledge:
            - 1,2 are unneeded
            - 5 must be calculated for all
            - 20 also for the 10 intermediate interval

        it works only with special function
    '''

    if pences < 200:
        pences += 200

    # space can be optimized, lots of 0
    precalcul = {}
    for i in range(2, len(COINS)):
        precalcul[i-2] = [0]*(pences+1)

    # 5 pennies: calculate them all
    for i in range(5):
        precalcul[0][i] = 1+i//2
    for i in range(5, pences+1):
        precalcul[0][i] = (1+i//2) + precalcul[0][i-5]

    return precalcul

def precalculated_2_extend(pences, remainder, precalcul, coin_index):
    '''
        extend cache on demand: calculate the values for this new remainder
    '''
    assert coin_index != 0

    coin = COINS[coin_index+2]
    # if coin == 50:
    #     print('50', coin_index, remainder, remainder%coin)

    precalcul[coin_index][remainder%coin] = precalcul[coin_index-1][remainder%coin]
    freq = coin

    # 20 pennies : also the intermediate 10s
    if coin == 20:
        remainder2 = (remainder+10)%coin
        # print('20', coin_index, remainder, remainder2)
        precalcul[coin_index][remainder2] = precalcul[coin_index-1][remainder2]
        if remainder%coin > remainder2:
            remainder = remainder2
        freq = 10

    for i in range(remainder%coin+coin, pences+1, freq):
        precalcul[coin_index][i] = precalcul[coin_index-1][i] + precalcul[coin_index][i-coin]

def solve_problem_precalculated_2(pences, precalcul, print_it=False):
    '''
        solve the given sum using the (actively) precalculated cache
        #5-#8 : timeouts
    '''

    precalcul = get_precalculated_2(pences)
    last_coin = get_last_coin(pences)

    if last_coin < 2:
        return pences-1 if pences > 2 else pences
    coin = COINS[last_coin]
    last_coin -= 2

    val = precalcul[last_coin][pences]
    if val != 0:
        return val

    remainder = pences%coin
    # print('remainder', remainder, last_coin)
    for i in range(1, last_coin+1):
        precalculated_2_extend(pences, remainder, precalcul, i)

    if print_it:
        print()
        for i in precalcul:
            print(COINS[i+2], precalcul[i])
            print()

    return precalcul[last_coin][pences]

##################################################################################################
#   hackerrank
#       "as the result can be large, print answer mod 10^9+7"
#
#   get_precalculated_1:  100/100
#   get_precalculated_2:  25/100    #5-#8 : timeouts
#       why the first is faster ? see get_precalculated_2 comments
#

def parse_input():
    '''the hackerrank solution

        https://www.hackerrank.com/contests/projecteuler/challenges/euler031
    '''

    cases = int(input().strip())

    sums = []
    max_sum = 0
    for _ in range(cases):
        next_sum = int(input().strip())
        if next_sum > max_sum:
            max_sum = next_sum
        sums.append(next_sum)

    pre = get_precalculated_1(max_sum)
    # pre = get_precalculated_2(max_sum)
    # print(pre)

    mod_print = 10**9+7

    for i in sums:
        last_coin = get_last_coin(i)

        result = pre[last_coin][i]
        # result = solve_problem_precalculated_2(i, pre)
        result = result%mod_print
        print(result)

##################################################################################################
#   main

def solve_problem_precalculate_on_demand(pences, print_it=False):
    '''calculate values only when needed'''
    return precalculate_english_coins_norec(pences, print_it)

def problem():
    '''the (simple) problem enonced by project Euler'''

    print(solve_problem_precalculate_on_demand(200))

def debug_assertions():
    '''unit tests'''

    # 4: 5x1, 2+3x1, 2x2+1x1, 5
    for i in range(4, 10):
        assert solve_problem_rec(i) == i-1
    assert solve_problem_rec(10) == 11
    assert solve_problem_rec(11) == 12
    assert solve_problem_rec(12) == 15
    assert solve_problem_rec(13) == 16
    assert solve_problem_rec(14) == 19
    assert solve_problem_rec(15) == 22
    assert solve_problem_rec(20) == 41

    for i in range(4, 10):
        assert solve_problem_precalculate_all(i) == i-1
    assert solve_problem_precalculate_all(10) == 11
    assert solve_problem_precalculate_all(11) == 12
    assert solve_problem_precalculate_all(12) == 15
    assert solve_problem_precalculate_all(13) == 16
    assert solve_problem_precalculate_all(14) == 19
    assert solve_problem_precalculate_all(15) == 22
    assert solve_problem_precalculate_all(20) == 41
    assert solve_problem_precalculate_all(23) == 54

    for i in range(4, 10):
        assert solve_problem_precalculate_on_demand(i) == i-1
    assert solve_problem_precalculate_on_demand(10) == 11
    assert solve_problem_precalculate_on_demand(11) == 12
    assert solve_problem_precalculate_on_demand(12) == 15
    assert solve_problem_precalculate_on_demand(13) == 16
    assert solve_problem_precalculate_on_demand(14) == 19
    assert solve_problem_precalculate_on_demand(15) == 22
    assert solve_problem_precalculate_on_demand(20) == 41
    assert solve_problem_precalculate_on_demand(23) == 54

    # solve_problem_precalculate_on_demand is very strong
    assert solve_problem_precalculate_on_demand(2000) == 23812353521

    assert precalculate_english_coins_norec(151) == 22412
    assert solve_problem_rec(151) == 22414
    assert solve_problem_precalculate_all(60) == 793
    assert solve_problem_precalculate_all(70) == 1311

    pre1 = get_precalculated_1(1000)
    pre2 = get_precalculated_2(1000)
    for i in range(1, 201):
        no1 = solve_problem_precalculated_1(i, pre1)
        no2 = solve_problem_precalculated_2(i, pre2)
        # print(i, no1, no2)
        assert no1 == no2

        # no2 = solve_problem_rec(i)
        # assert no1 == no2

        no2 = precalculate_on_demand(i)
        assert no1 == no2

def just_debug():
    '''debugging code'''

    if 0:   #pylint: disable=using-constant-test
        print(solve_problem_precalculate_all(151, True))
        print(precalculate_english_coins_norec(151, True))
        print(solve_problem_rec(151))

    if 0:   #pylint: disable=using-constant-test
        for i in range(1, 11):
            print(i)
            print(solve_problem_precalculate_all(i, True))
            # print(solve_problem_precalculate_on_demand(i, True))
            print()

    if 0:   #pylint: disable=using-constant-test
        get_precalculated_1(70, True)

        pre = get_precalculated_2(70)
        print(solve_problem_precalculated_2(70, pre, True))

def main():
    '''THE main'''

    debug_assertions()
    just_debug()

    # parse_input()  # activate for hackerrank
    problem()

if __name__ == "__main__":
    main()
