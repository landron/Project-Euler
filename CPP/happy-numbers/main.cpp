/*
    Problems:
        Still do not passes 5,6,7: "Terminated due to timeout".

        I use some "return BigInt" and most implementations are old enough and do not know about move operations.

    Reference
        https://github.com/landron/Project-Euler/blob/master/Python/todo_hackerrank/happy_numbers.py
        The Python version misses 2/10 HackerRank tests even with PyPy.

    \todo   make my own basic BigInt (+,-,%)

    tag_big_int
*/
#include <cassert>
#include <iostream>
#include <vector>
#include <functional>

#include "gtest/gtest.h"

#include "TinyBigInt.h"

using CppBigInt = unsigned long long int;
/*
    various bigint libraries

    the given times are for problem_rec(80); HackerRank expects decent times until 200
*/

#include "bigint/BigIntegerLibrary.hh"
//  https://github.com/sercantutar/infint
//#include "InfInt.h"
//  https://raw.githubusercontent.com/indy256/codelibrary/master/cpp/numeric/bigint.cpp
//#include "bigint.cpp.h"7
//  https://github.com/faheel/BigInt : does not compile, then even slower
//#include "BigInt.hpp"

//using MyBigInteger = BigInt; // ?? very, very big
//using MyBigInteger = InfInt;  //  133250 ms !!
//using MyBigInteger = bigint; // 89093 ms

// this seems alright, unfortunately the implementation is hard to transpose on HackerRank
using MyBigInteger = BigUnsigned;   // 17427 ms
//using MyBigInteger = lee_woo::BigInt;

// constexpr does not get along with most implementations: memory allocation is needed
constexpr auto get_pow(unsigned number, unsigned power) {
    auto result = static_cast<CppBigInt>(1);
    for (unsigned i = 0; i < power; ++i) result *= number;
    return result;
};

auto get_pow_big(unsigned number, unsigned power) {
    auto result = static_cast<MyBigInteger>(1);
    for (unsigned i = 0; i < power; ++i) result *= number;
    return result;
};

//  get_pow: it works if MyBigInteger knows about CppBigInt
static const auto MODULO_HK = get_pow_big(10,9) + 7;

constexpr auto sum_of_pow_digits(unsigned number)
{
    auto sum_of = static_cast<unsigned>(0);
    for (; number >= 1; number /= 10) {
        const auto digit = number % 10;
        sum_of += digit * digit;
    };
    return sum_of;
};

/*
    http://echochamber.me/viewtopic.php?t=96670

    Bryan Wolf's wonderful recursive solution:
        calculate the count recursively for each of
            81*digits_no possible sums
*/
constexpr auto get_happy_count_rec_pure(unsigned digits_no, int number) -> unsigned long
{
    assert(digits_no >= 0);

    if (number < 0) return 0;
    if (number == 0) return 1;
    if (digits_no == 0) return 0;

    unsigned long sum_of = 0;
    for (auto i = 0; i < 10; ++i) {
        const auto prev = number - i * i;
        if (prev < 0) break;
        sum_of += get_happy_count_rec_pure(digits_no - 1, prev);
    }
    return sum_of;
};

std::vector<unsigned> get_precalculated_table(unsigned digits_no)
{
    const auto get_presolved = [](unsigned digits_no) {
        return (digits_no < 4) ? 243 : 81 * digits_no;
    };
    const auto limit_presolved = 1 + get_presolved(digits_no);

    std::vector<unsigned> solved(limit_presolved);
    solved[1] = 1;

    for (unsigned i = 2; i < limit_presolved; ++i) {
        if (solved[i]) continue;

        std::vector<unsigned> gen = {i};
        auto number = i;
        for (; number != 1 && number != 89; ){
            number = sum_of_pow_digits(number);
            if (solved[number]) {
                number = solved[number];
                break;
            }
                
            gen.push_back(number);
        }

        for (const auto j : gen)
            solved[j] = number;
    }

    return solved;
}

auto problem_rec(unsigned digits_no) {
    // retains value+1 to allow 0 for initialization
    using CacheTable = std::vector< std::vector<MyBigInteger> >;

    //std::function <constexpr BigInteger(unsigned, unsigned, CacheTable&) > get_happy_count_rec;
    std::function <MyBigInteger(unsigned, unsigned, CacheTable&) > get_happy_count_rec;

    get_happy_count_rec = [&get_happy_count_rec](unsigned digits_no, int number,
        CacheTable& table) -> MyBigInteger {
        assert(digits_no >= 0);

        if (number < 0) return 0;
        if (number == 0) return 1;
        if (digits_no == 0) return 0;
        if (table[digits_no - 1][number - 1] != 0) return table[digits_no - 1][number - 1]-1;

        auto sum_of = static_cast<MyBigInteger>(0);
        for (auto i = 0; i < 10; ++i) {
            const auto prev = number - i * i;
            if (prev < 0) break;
            sum_of += get_happy_count_rec(digits_no - 1, prev, table);
        }
        table[digits_no - 1][number - 1] = sum_of+1;
        return sum_of;
    };

    const auto get_happy_count_with_hash = [&get_happy_count_rec](unsigned digits_no, unsigned number, 
        CacheTable& table)
    {
        const auto count = get_happy_count_rec(digits_no, number, table);
        assert(table[digits_no - 1][number - 1] != 0);
        return count;
    };

    const auto solved = get_precalculated_table(digits_no);
    const auto precalculated = solved.size();

    CacheTable table(digits_no);
    for (auto& i : table)
        i.resize(precalculated);

    auto happy = static_cast<MyBigInteger>(0);
    for (auto i = 1; i < solved.size(); ++i) {
        if (solved[i] == 1) {
            const auto count = get_happy_count_with_hash(digits_no, i, table);
            happy += count;
        }
    }

    return get_pow_big(10, digits_no) - happy - 1;
}

void parse_input() 
{
    unsigned digits_no;
    std::cin >> digits_no;
    auto result = problem_rec(digits_no);
    result = result % MODULO_HK;
    std::cout << result << std::endl;
}

TEST(test_units, basic)
{
    // C++ 11 requires a message in static_asserts

    static_assert(sum_of_pow_digits(10) == 1, "");
    static_assert(sum_of_pow_digits(13) == 10, "");

    static_assert(get_happy_count_rec_pure(1, 81) == 1, "");
    static_assert(get_happy_count_rec_pure(2, 82) == 2, "");
    static_assert(get_happy_count_rec_pure(2, 97) == 2, "");

    ASSERT_TRUE(sum_of_pow_digits(999) == 243);
}

TEST(test_units, tiny_big_int_additions)
{
    using BigInt = lee_woo::BigInt;

    BigInt test;
    ASSERT_TRUE(test == 0);
    test = 13;
    ASSERT_TRUE(test == 13);
    ASSERT_TRUE(test.increase_size(4) == 13);
    ASSERT_TRUE(test.add(8) == 21);
    ASSERT_TRUE(test.add(138) == 159);
    ASSERT_TRUE(test.add(892) == 1051);
    ASSERT_TRUE(test.add(32123) == 33174);

    test = 999123;
    ASSERT_TRUE(test.add(877) == 1000000);
}

TEST(test_units, tiny_big_int_multiplications)
{
    using BigInt = lee_woo::BigInt;

    auto test = BigInt(13);
    ASSERT_TRUE(test.multiply(3) == 39);
    test = 13;
    ASSERT_TRUE(test.multiply(137) == 1781);
    ASSERT_TRUE(test.multiply(0) == 0);

    test = 6073;
    auto second = BigInt(631);
    test += second;
    ASSERT_TRUE(test == 6704);
    second = BigInt(228);
    test += second;
    ASSERT_TRUE(test == 6932);
    second = BigInt(3111);
    test += second;
    ASSERT_TRUE(test == 10043);

    second = BigInt(3);
    test *= second;
    ASSERT_TRUE(test == 30129);
    second = BigInt(11);
    test *= second;
    ASSERT_TRUE(test == 331419);
    test = 10043;
    second = BigInt(417);
    test *= second;
    ASSERT_TRUE(test == 4187931);
}


TEST(test_units, DISABLED_get_precalculated_table)
//TEST(test_units, get_precalculated_table)
{
    ASSERT_TRUE(get_precalculated_table(1).size() == 243+1);
    ASSERT_TRUE(get_precalculated_table(10).size() == 810+1);

    const auto table = get_precalculated_table(10);
    ASSERT_TRUE(table[0] == 0);
    ASSERT_TRUE(table[1] == 1);
    ASSERT_TRUE(table[2] == 89);
}

TEST(test_units, DISABLED_happy_numbers)
{
    ASSERT_TRUE(problem_rec(1) == 7);
    ASSERT_TRUE(problem_rec(2) == 80);
    ASSERT_TRUE(problem_rec(3) == 857);
    ASSERT_TRUE(problem_rec(4) == 8558);
    ASSERT_TRUE(problem_rec(5) == 85623);
    ASSERT_TRUE(problem_rec(6) == 856929);

    ASSERT_TRUE(problem_rec(9) == 854325192);
    ASSERT_TRUE(problem_rec(10)%MODULO_HK == 507390796);
    ASSERT_TRUE(problem_rec(11)%MODULO_HK == 908800055);
}

TEST(performance_tests, DISABLED_limit_80)
{
    auto result = problem_rec(80);
    result = result % MODULO_HK;
    std::cout << result << std::endl;

    //parse_input();
}
