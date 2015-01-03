"""
    Problem 8 : largest product in a series
    http://projecteuler.net/problem=8
        Find the thirteen adjacent digits in the 1000-digit number that have the greatest product.
    Version: 2015.01.03

    Your code has been rated at 10.00/10

    TODO:   add a functional programming solution
"""

LARGE_NUMBER = "\
73167176531330624919225119674426574742355349194934\
96983520312774506326239578318016984801869478851843\
85861560789112949495459501737958331952853208805511\
12540698747158523863050715693290963295227443043557\
66896648950445244523161731856403098711121722383113\
62229893423380308135336276614282806444486645238749\
30358907296290491560440772390713810515859307960866\
70172427121883998797908792274921901699720888093776\
65727333001053367881220235421809751254540594752243\
52584907711670556013604839586446706324415722155397\
53697817977846174064955149290862569321978468622482\
83972241375657056057490261407972968652414535100474\
82166370484403199890008895243450658541227588666881\
16427171479924442928230863465674813919123162824586\
17866458359124566529476545682848912883142607690042\
24219022671055626321111109370544217506941658960408\
07198403850962455444362981230987879927244284909188\
84580156166097919133875499200524063689912560717606\
05886116467109405077541002256983155200055935729725\
71636269561882670428252483600823257530420752963450\
"
ORD_CHAR_0 = 48

def calculate_product(number, number_of_digits, index):
    """calculate the product of a sequence"""
    prod = 1
    for i in range(number_of_digits):
        prod *= (ord(number[index+i]) - ORD_CHAR_0)
    return prod

def compare_sequences_unused(number, number_of_digits, first, second):
    """compare two sequences"""
    assert first + number_of_digits <= len(number)
    assert second + number_of_digits <= len(number)

    prod1 = 1
    prod2 = 1
    for i in range(number_of_digits):
        prod1 *= (ord(number[first+i]) - ORD_CHAR_0)
        prod2 *= (ord(number[second+i]) - ORD_CHAR_0)

    return prod1 < prod2

def greatest_sequence(number, number_of_digits, trace):
    """Find 13 digits sequence with the largest product"""
    assert isinstance(number, str)
    assert number_of_digits > 0
    assert len(number) >= number_of_digits

    partial = 0
    for partial in range(0, len(number) - number_of_digits + 1):
        zero_found = False
        for i in range(number_of_digits):
            if '0' == number[partial+i]:
                zero_found = True
                partial = partial+i+1
        if not zero_found:
            break

    dbg_stats = lambda: None
    dbg_stats.product_comp = 0
    dbg_stats.zero_found = 0
    dbg_stats.last_greater = 0

    result = 0  # the found index
    prod = 0

    i = partial+1
    while i < len(number) - number_of_digits + 1:
        # optimization 1: new last is greater than the first of the previous sequence
        if number[i+number_of_digits-1] >= number[partial]:
            partial = i
            dbg_stats.last_greater += 1
        else:
            prod2 = calculate_product(number, number_of_digits, partial)
            if prod < prod2:
                result = partial
                prod = prod2
            else:
                # optimization 2: skip sequences containing 0
                if '0' == number[i+number_of_digits-1]:
                    partial = i+number_of_digits
                    i = partial+number_of_digits-1
                    dbg_stats.zero_found += 1
                else:
                    partial = i+2
                    i += 1
            dbg_stats.product_comp += 1
        i += 1

    # 421: 13 digits
    if trace:
        print("Product stats: ", dbg_stats.__dict__)
        # print("Largest product: ", prod)

    return result

def greatest_sequence_wrap(number, number_of_digits, trace=True):
    """greatest_sequence, but with print and validations"""

    index = greatest_sequence(number, number_of_digits, trace)
    assert index + number_of_digits <= len(number)
    result = number[index:index+number_of_digits]
    if trace:
        print("Sequence found ({0}): ".format(index), result)

    prod = calculate_product(number, number_of_digits, index)
    if trace:
        print("Product: ", prod)
    return prod

if __name__ == "__main__":
    assert 1000 == len(LARGE_NUMBER)
    assert 48 == ORD_CHAR_0

    # unit tests
    assert 9 == greatest_sequence_wrap(LARGE_NUMBER, 1, False)
    assert 81 == greatest_sequence_wrap(LARGE_NUMBER, 2, False)
    assert 648 == greatest_sequence_wrap(LARGE_NUMBER, 3, False)
    assert 5832 == greatest_sequence_wrap(LARGE_NUMBER, 4, False)
    assert 61725888 == greatest_sequence_wrap(LARGE_NUMBER, 9, False)
    assert 23514624000 == greatest_sequence_wrap(LARGE_NUMBER, 13, False)

    greatest_sequence_wrap(LARGE_NUMBER, 13)
