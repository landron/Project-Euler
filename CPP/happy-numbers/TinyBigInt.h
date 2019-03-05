#pragma once

#include <cassert>
//#include <string_view> // not C++ 14

namespace lee_woo 
{
    constexpr auto digits_no(unsigned number) {
        auto digits_no = 0;
        for (; number >= 1; number /= 10, ++digits_no);
        return digits_no ? digits_no : 1;
    };

    class BigInt
    {
    public:
        BigInt(unsigned = 0);
        BigInt(size_t, char /*= 0*/);

        //  move functionality: should not be necessary

        bool operator==(unsigned val) const noexcept {
            return equals(*this, val);
        }

        bool operator!=(unsigned val) const noexcept {
            return !operator==(val);
        }

    public:
        BigInt& operator *= (const BigInt& factor) {
            multiply_big(*this, factor);
            return *this;
        }

        BigInt& multiply(unsigned factor) {
            multiply(*this, factor);
            return *this;
        }

        BigInt& operator += (const BigInt& term) {
            add_big(*this, term);
            return *this;
        }

        BigInt& operator+ (unsigned term) {
            add(*this, term);
            return *this;
        }

        BigInt& add(unsigned term) {
            add(*this, term);
            return *this;
        }

        BigInt& increase_size(size_t len) {
            increase_size(*this, len);
            return *this;
        }

    private:
        const std::string& get() const {
            return m_nb;
        }

        static bool equals(const BigInt&, const std::string&) noexcept;
        static bool equals(const BigInt&, unsigned) noexcept;

        static inline void increase_size(BigInt&, size_t);

        static void multiply_big(BigInt& first, const BigInt& second);
        static void add_big(BigInt&, const BigInt&, size_t position_from_end = 0);
        static void multiply(BigInt&, unsigned);
        static void add(BigInt&, unsigned, size_t position_from_end = 0);

    private:
        std::string m_nb;
        // not generalized
        bool m_signed = false;
    };
};

lee_woo::BigInt::BigInt(unsigned number)
{
    std::string nb;
    for (; number >= 1; number /= 10) {
        const auto digit = number % 10;
        nb += ('0' + digit);
    };
    if (nb.empty())
        m_nb = "0";
    else {
        std::reverse(nb.begin(), nb.end());
        m_nb = std::move(nb);
    }
}

lee_woo::BigInt::BigInt(size_t size, char fill)
{
    assert(fill == 0 || ('0' <= fill && fill <= '9'));
    if (fill == 0)
        fill = '0';
    std::string resized(size, fill);
    m_nb = std::move(resized);
}

bool lee_woo::BigInt::equals(const BigInt& nb, const std::string& val) noexcept
{
    size_t pos = 0;
    for (; pos < nb.m_nb.size() && nb.m_nb[pos] == '0'; ++pos);
    return ((nb.m_nb.size() - pos) == val.size()) && 
           (0 == nb.m_nb.compare(pos, nb.m_nb.size() - pos, val));
}

bool lee_woo::BigInt::equals(const BigInt& nb, unsigned val) noexcept
{
    auto i = nb.m_nb.size();
    for (; val >= 1 && i > 0; val /= 10, --i) {
        if (val % 10 != (nb.m_nb[i - 1] - '0')) return false;
    }
    if (i == 0) return (val < 1);

    size_t j = 0;
    for (; j < nb.m_nb.size() && nb.m_nb[j] == '0'; ++j);

    return i == j;
}

void lee_woo::BigInt::increase_size(BigInt& nb, size_t len) {
    if (nb.m_nb.size() <= len) {
        const auto size1 = nb.m_nb.size();

        std::string resized(len, '0');
        resized.replace(resized.size() - size1, size1, nb.m_nb);
        nb.m_nb = std::move(resized);
    }
}

void lee_woo::BigInt::multiply_big(BigInt& first, const BigInt& second) 
{
    BigInt result(1 + std::max(first.m_nb.size(), second.m_nb.size()), 0);

    auto i = second.m_nb.size();
    for (BigInt next = first; i > 0; --i, next = first) {
        multiply(next, second.m_nb[i-1]-'0');
        add_big(result, next, second.m_nb.size() - i);
    }

    first = std::move(result);
};

void lee_woo::BigInt::multiply(BigInt& number, unsigned factor)
{
    const auto size_result = number.m_nb.size() + digits_no(factor) + 1;

    BigInt result(size_result, '0');
    for (auto i = number.m_nb.size(); i > 0; --i) {
        const auto j = i - 1;
        const auto term = factor * (number.m_nb[j] - '0');
        add(result, term, number.m_nb.size() - j - 1);
    }

    number = std::move(result);
}

void lee_woo::BigInt::add(BigInt& number, unsigned term, size_t position_from_end) {
    const auto size_result = position_from_end + digits_no(term) + 1;
    number.increase_size(size_result);

    constexpr auto add_digits = [](unsigned d1, unsigned d2, unsigned& carry) {
        const auto sum_of = d1 + d2 + carry;
        carry = 0;
        if (sum_of < 10) return sum_of;
        assert(sum_of < 100);
        carry = sum_of / 10;
        assert(carry == 1);
        return sum_of % 10;
    };

    unsigned carry = 0;
    auto i = number.m_nb.size()-position_from_end;
    for (; term >= 1; term /= 10, --i) {
        assert(0 < i && i <= number.m_nb.size());
        assert(number.m_nb[i-1] >= '0' && number.m_nb[i-1] <= '9');
        number.m_nb[i-1] = '0' + add_digits(term % 10, number.m_nb[i-1] - '0', carry);
    }
    while (carry && i) {
        number.m_nb[i-1] = '0' + add_digits(0, number.m_nb[i-1] - '0', carry);
        --i;
    }
    if (i == 0 && carry)
        number.m_nb.insert(0, "1");
}

void lee_woo::BigInt::add_big(BigInt& number, const BigInt& term, size_t position_from_end) 
{
    const auto size_result = position_from_end + term.m_nb.size() + 1;
    number.increase_size(size_result);

    for (size_t i = term.m_nb.size(); i > 0; --i)
        add(number, term.m_nb[i - 1]-'0', position_from_end + term.m_nb.size() - i);
}