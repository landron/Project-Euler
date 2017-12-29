#! /usr/bin/python3
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
        solve_problem_precalculate  :
            using the "Investigating combinations of English currency denominations" document on https://projecteuler.net/problem=31
            The idea is simple: pre-calculate all the sums less than the needed one starting with the smaller coin

            With t = total sum, c = coin
            "The function w(t, c) can be reformulated as follows:
                
                w(t, c) =   1           
                                if c = 1 or t = 0
                            w(t, s(c))  
                                if c > 1 and t < c
                            w(t, s(c)) + w(t − c, c) 
                                if c > 1 and t ≥ c

                s(c) = previous coin

    pylint 1.5.5
        Your code has been rated at 8.78/10.
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
#   hackerrank : 25/100

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

def solve_problem_rec(pences):
    types = len(COINS)

    already_calculated = []
    for _ in range(types):
        already_calculated.append({})

    # return solve_problem_recursive_1(pences, pences, array('I', types*[0]), types-1)
    # return solve_problem_recursive_2(already_calculated, pences, types-1)
    return solve_problem_recursive_3(already_calculated, pences, types-1)

##################################################################################################
#   hackerrank : 25/100
#
#   solve_problem_precalculated_1:
#       #3 - #4 : "wrong answer"s    
#       #5 - #8 : timeouts

def get_last_coin(pences):
    last_coin = 0
    for i, el in enumerate(COINS):
        if el > pences:
            break
        last_coin = i
    return last_coin

def get_precalculated_1(pences, print_it=False):
    precalcul = {}

    last_coin = 0
    for i, el in enumerate(COINS):
        if el > pences:
            break
        last_coin = i
        precalcul[i] = [0]*(1+pences)   #space for 0

    prev = -1
    for i, el in enumerate(COINS):
        if el > pences:
            break
        for j in range(1+pences):
            if i == 0:
                if pences % el == 0:  # always for COINS[0]=1
                    precalcul[i][j] = 1
            elif j < el:
                precalcul[i][j] = precalcul[prev][j]
            else:
                precalcul[i][j] = precalcul[prev][j] + precalcul[i][j-el]
        prev = i

    if print_it:
        for i in precalcul:
            print(COINS[i], precalcul[i])

    return precalcul

def solve_problem_precalculate_all(pences, print_it=False):

    precalcul = get_precalculated_1(pences, print_it)
    last_coin = 0
    for i, el in enumerate(COINS):
        if el > pences:
            break
        last_coin = i

    return precalcul[last_coin][-1]

def solve_problem_precalculated_1(pences, precalcul, print_it=False):

    if not precalcul or len(precalcul[0]) < pences+1:
        precalcul = get_precalculated_1(pences, print_it)

    last_coin = 0
    for i, el in enumerate(COINS):
        if el > pences:
            break
        last_coin = i

    return precalcul[last_coin][-1]

##################################################################################################
#   hackerrank : 25/100
#
#   Probably:   "RecursionError: maximum recursion depth exceeded in comparison"
#

def solve_problem_precalculate_rec(precalculated, pences, coin):

    no_possibilities = precalculated[coin][pences]
    if no_possibilities != 0:
        return no_possibilities

    assert coin != 0
    no_possibilities = solve_problem_precalculate_rec(precalculated, pences, coin-1)
    if pences >= COINS[coin]:
        no_possibilities += solve_problem_precalculate_rec(precalculated, pences-COINS[coin], coin)
    precalculated[coin][pences] = no_possibilities
    return no_possibilities

def solve_problem_precalculate_on_demand_1(pences, print_it=False):

    last_coin = 0

    precalcul = {}
    for i, el in enumerate(COINS):
        if el > pences:
            break
        elif i == 0:
            precalcul[i] = [1]*(1+pences)   #space for 0
        else:
            last_coin = i
            precalcul[i] = [0]*(1+pences)   #space for 0
            precalcul[i][0] = 1

    result = solve_problem_precalculate_rec(precalcul, pences, last_coin)

    if print_it:
        for i in precalcul:
            print(i, precalcul[i])

    return result

##################################################################################################
#   hackerrank : 25/100 , but no runtime error
#
#   #3 - #4 : "wrong answer"s    
#   #5 - #8 : timeouts
#
#   adapted for English coins 
#       can still be optimized: 1,2 do not need to be calculated
#       score: 0

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
        r = remainder%COINS[i]
        # print("remainder", r, COINS[i])
        precalcul[i][r] = precalcul[i-1][r]
        # print(i, r, precalcul[i][r])
        for j in range(r+COINS[i], remainder+1, COINS[i]):
            precalcul[i][j] = precalcul[i-1][j] + precalcul[i][j-COINS[i]]

    if last_coin > 1:
        for i in range(remainder+5, pences+1, 5):
            precalcul[2][i] = precalcul[1][i] + precalcul[2][i-5]

# no recursion
def solve_problem_precalculate_English_coins(pences, print_it=False):

    last_coin = 0

    precalcul = {}
    for i, el in enumerate(COINS):
        if el > pences:
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
            r = (remainder+10)%20
            precalcul[j][r] = precalcul[j-1][r]
            for i in range(r+COINS[j], pences+1, COINS[j]):
                precalcul[j][i] = precalcul[j-1][i] + precalcul[j][i-COINS[j]] 

    if print_it:
        for i in precalcul:
            print(COINS[i], precalcul[i])

    return precalcul[last_coin][pences]

##################################################################################################
#   hackerrank
#
#       cache the precalculated table and reuse it
#       25/100: #3 -#8 = wrong answers

# https://www.hackerrank.com/contests/projecteuler/challenges/euler031
def parse_input():
    cases = int(input().strip())

    sums = [] 
    max_sum = 0
    for _ in range(cases):
        next_sum = int(input().strip())
        if next_sum > max_sum:
            max_sum = next_sum
        sums.append(next_sum)

    pre = get_precalculated_1(max_sum)
    # print(pre)

    for i in sums:
        last_coin = get_last_coin(i)
        print(pre[last_coin][i])
    
##################################################################################################
#   main

def solve_problem_precalculate_on_demand(pences, print_it=False):
    # return solve_problem_precalculate_on_demand_3(pences, print_it)
    return solve_problem_precalculate_all(pences, print_it)

def solve_problem(pences):
    return solve_problem_precalculate_on_demand(pences)

def problem():
    print(solve_problem(200))

def debug_assertions():
    # 5x1, 2+3x1, 2x2+1x1, 5
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

    for i in range(1, 100):
        no1 = solve_problem_precalculate_all(i)
        no2 = solve_problem_precalculate_English_coins(i)
        # print(i, no1, no2)
        assert no1 == no2

def just_debug():

    if 0:
        print(solve_problem_precalculate_all(69, True))
        print(solve_problem_precalculate_English_coins(69, True))

    if 0:
        for i in range(1, 11):
            print(i)
            print(solve_problem_precalculate_all(i, True))
            # print(solve_problem_precalculate_on_demand(i, True))
            print()

def main():
    debug_assertions()
    just_debug()

    # parse_input()
    problem()

if __name__ == "__main__":
    main()
