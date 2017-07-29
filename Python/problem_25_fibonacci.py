#!/bin/python3
'''    
    https://projecteuler.net/problem=25
        # https://www.hackerrank.com/contests/projecteuler/challenges/euler025
'''

import sys

def large_sum_base(a, b):
    assert len(b) == len(a) or len(b) == len(a) - 1
    
    m = len(a)
    if m > len(b): 
        b += [0]
    # print(a, b)

    inc = False
    for i in range(m):
        b[i] += a[i]
        if inc:
            b[i] += 1
        if b[i] >= 10:
            b[i] -= 10
            inc = True
        else:
            inc = False

    if not inc:
        return False
    else:
        b += [1]
        return True

def Fibonacci_index_for_digits(n, use_cache, cache):
    assert n >= 1
    if n == 1:
        return 1

    f1 = [1]
    f2 = [1]
    digits = 1
    index = 2
    if use_cache and len(cache.table) > 0:
        assert len(cache.table) <= n
        f1 = cache.f1
        f2 = cache.f2
        digits = len(cache.table)-1
        index = cache.table[-1]
    # print(index, f1, f2, digits)

    while digits < n:
        index += 1
        if large_sum_base(f2, f1):
            digits += 1
            if use_cache:
                cache.table += [index]

        t = f1
        f1 = f2
        f2 = t
        

    if use_cache:
        cache.f1 = f1
        cache.f2 = f2

    return index

# not enough for hackerrank
def Fibonacci_index_cache(n, cache):
    if n < len(cache.table):
        return cache.table[n]
    return Fibonacci_index_for_digits(n, True, cache)

def Fibonacci_index(n):
    return Fibonacci_index_for_digits(n, False, None)

# hackerrank, \todo:   find the formula - here is the 500 table
'''
[0, 2, 7, 12, 17, 21, 26, 31, 36, 40, 45, 50, 55, 60, 64, 69, 74, 79, 84, 88, 93, 98, 103, 107, 112, 117, 122, 127, 131, 136, 141, 146, 151,
 155, 160, 165, 170, 174, 179, 184, 189, 194, 198, 203, 208, 213, 217, 222, 227, 232, 237, 241, 246, 251, 256, 261, 265, 270, 275, 280, 284,
 289, 294, 299, 304, 308, 313, 318, 323, 328, 332, 337, 342, 347, 351, 356, 361, 366, 371, 375, 380, 385, 390, 395, 399, 404, 409, 414, 418,
 423, 428, 433, 438, 442, 447, 452, 457, 462, 466, 471, 476, 481, 485, 490, 495, 500, 505, 509, 514, 519, 524, 529, 533, 538, 543, 548, 552,
 557, 562, 567, 572, 576, 581, 586, 591, 596, 600, 605, 610, 615, 619, 624, 629, 634, 639, 643, 648, 653, 658, 662, 667, 672, 677, 682, 686,
 691, 696, 701, 706, 710, 715, 720, 725, 729, 734, 739, 744, 749, 753, 758, 763, 768, 773, 777, 782, 787, 792, 796, 801, 806, 811, 816, 820,
 825, 830, 835, 840, 844, 849, 854, 859, 863, 868, 873, 878, 883, 887, 892, 897, 902, 907, 911, 916, 921, 926, 930, 935, 940, 945, 950, 954,
 959, 964, 969, 974, 978, 983, 988, 993, 997, 1002, 1007, 1012, 1017, 1021, 1026, 1031, 1036, 1041, 1045, 1050, 1055, 1060, 1064, 1069, 1074
, 1079, 1084, 1088, 1093, 1098, 1103, 1108, 1112, 1117, 1122, 1127, 1131, 1136, 1141, 1146, 1151, 1155, 1160, 1165, 1170, 1174, 1179, 1184,
1189, 1194, 1198, 1203, 1208, 1213, 1218, 1222, 1227, 1232, 1237, 1241, 1246, 1251, 1256, 1261, 1265, 1270, 1275, 1280, 1285, 1289, 1294, 12
99, 1304, 1308, 1313, 1318, 1323, 1328, 1332, 1337, 1342, 1347, 1352, 1356, 1361, 1366, 1371, 1375, 1380, 1385, 1390, 1395, 1399, 1404, 1409
, 1414, 1419, 1423, 1428, 1433, 1438, 1442, 1447, 1452, 1457, 1462, 1466, 1471, 1476, 1481, 1486, 1490, 1495, 1500, 1505, 1509, 1514, 1519,
1524, 1529, 1533, 1538, 1543, 1548, 1553, 1557, 1562, 1567, 1572, 1576, 1581, 1586, 1591, 1596, 1600, 1605, 1610, 1615, 1619, 1624, 1629, 16
34, 1639, 1643, 1648, 1653, 1658, 1663, 1667, 1672, 1677, 1682, 1686, 1691, 1696, 1701, 1706, 1710, 1715, 1720, 1725, 1730, 1734, 1739, 1744
, 1749, 1753, 1758, 1763, 1768, 1773, 1777, 1782, 1787, 1792, 1797, 1801, 1806, 1811, 1816, 1820, 1825, 1830, 1835, 1840, 1844, 1849, 1854,
1859, 1864, 1868, 1873, 1878, 1883, 1887, 1892, 1897, 1902, 1907, 1911, 1916, 1921, 1926, 1931, 1935, 1940, 1945, 1950, 1954, 1959, 1964, 19
69, 1974, 1978, 1983, 1988, 1993, 1998, 2002, 2007, 2012, 2017, 2021, 2026, 2031, 2036, 2041, 2045, 2050, 2055, 2060, 2064, 2069, 2074, 2079
, 2084, 2088, 2093, 2098, 2103, 2108, 2112, 2117, 2122, 2127, 2131, 2136, 2141, 2146, 2151, 2155, 2160, 2165, 2170, 2175, 2179, 2184, 2189,
2194, 2198, 2203, 2208, 2213, 2218, 2222, 2227, 2232, 2237, 2242, 2246, 2251, 2256, 2261, 2265, 2270, 2275, 2280, 2285, 2289, 2294, 2299, 23
04, 2309, 2313, 2318, 2323, 2328, 2332, 2337, 2342, 2347, 2352, 2356, 2361, 2366, 2371, 2376, 2380, 2385, 2390]
'''
def WIP_Fibonacci_index_formula(n):
    if n < 5:
        return 2 + (n-1)*5                                                  #  17
    elif n < 9:
        n -= 5
        return Fibonacci_index_formula(4) + 4 + n*5                         #  36
    elif n < 9+2*14:
        n -= 9 
        return Fibonacci_index_formula(8) + 4 + n*5 - n//5 - n//14          #  40+135-5-1 = 174
    elif n < 37+9:
        n -= 37
        return Fibonacci_index_formula(36) + 4 + n*5 - n//5 - n//14

        # \todo
    else:
        n -= 45
        return Fibonacci_index_formula(45) + 4 + n*5 - n//5 - n//14

# https://www.hackerrank.com/contests/projecteuler/challenges/euler025
def parse_input_with_cache(cache):
    T = int(input().strip())

    for _ in range(T):
        N = int(input().strip())
        # index = Fibonacci_index_cache(N, cache)
        index = WIP_Fibonacci_index_formula(N)
        print(index)
        # print(cache.table)

def parse_input():
    cache = lambda:None
    # initialization, not correct for the first two entries
    cache.table = [0, 2]
    cache.f1 = [1]
    cache.f2 = [1]

    parse_input_with_cache(cache)
    # Fibonacci_index_cache(500, cache)
    # print(cache.table)

def debug_assertions():
    assert Fibonacci_index(2) == 7
    assert Fibonacci_index(3) == 12
    assert Fibonacci_index(4) == 17
    assert Fibonacci_index(1000) == 4782

def main():
    # debug_assertions()
    # parse_input()
    
    print(Fibonacci_index(1000))

if __name__ == "__main__":
    main()
