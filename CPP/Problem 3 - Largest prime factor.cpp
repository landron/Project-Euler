//	Version:	2013.12.31
/*
	LargestPrimeFactor_1_Base:	it builds the sieve of Eratosthenes
	LargestPrimeFactor_2_Base:	brute force, first validates the divison, then the prime number
	LargestPrimeFactor_3_Base:	brute force, first validates the prime number, then the division

	for 600851475143: 1<3<2
*/

#include <cassert>
#include <cstdint>
#include <sstream>
#include <atlbase.h>
#include <vector>

#include "Perform.h"

typedef std::uint64_t UIntType;

static bool s_debug = false;

static
void SieveOfEratosthenes(std::vector<UIntType>& sieve, UIntType first, const size_t size)
{
	if (!(first & 0x1))
		++first;

	sieve.resize(size);
	for (size_t i = 0; i < size; ++i)
		sieve[i] = (first+i);

	for (size_t factor = 3; factor < (first+size)/10; factor +=2)
	{
		size_t start = (factor-first%factor);
		if ((start+first) == factor)
			start += factor;
		if (!sieve[start])
			continue;

		for (size_t i = start; i < size; i += factor)
		{
			//std::cout<<(first+i)<<" ";
			sieve[i] = 0;
		}
		//std::cout<<std::endl;
	}
}

static 
bool LargestPrimeFactor_1_Base_Range(const UIntType number, const UIntType first, const size_t size, UIntType& largest)
{
	std::vector<UIntType> sieve;
	SieveOfEratosthenes(sieve, first, size);
	for (size_t i = 0; i < sieve.size(); i+=2)
	{
		if (!sieve[i])
			continue;

		//	TODO:	2 divisions
		//int c = (int)a / b;
		//int d = a % b; // Likely uses the result of the division.

		if (number/sieve[i] < sieve[i])
			return false;
		if (0 == number%sieve[i])
			largest = sieve[i];
	}
	return true;
}

/*
	1048576	??
*/
static 
UIntType LargestPrimeFactor_1_Base(const UIntType number)
{
	UIntType temp = number;
	UIntType pow2;
	for (pow2 = 0; temp; temp >>= 1)
		pow2++;
	UIntType maxF = (pow2%2) ? (1<<(pow2/2+1)) : (1<<(pow2/2));
	//std::cout<<maxF<<std::endl;

	UIntType largest = 0;

	static const size_t SIEVE_MAX_SIZE = 100000;
	if (SIEVE_MAX_SIZE > maxF)
		(void)LargestPrimeFactor_1_Base_Range(number, 0, (size_t)maxF, largest);
	else
	{
		size_t i;
		for (i = 0; i < maxF; i += SIEVE_MAX_SIZE)
			if (!LargestPrimeFactor_1_Base_Range(number, i, SIEVE_MAX_SIZE, largest))
				return largest;
		(void)LargestPrimeFactor_1_Base_Range(number, i-SIEVE_MAX_SIZE, (size_t)(maxF-(i-SIEVE_MAX_SIZE)), largest);
	}

	return largest;
}

template <typename U>
static inline
bool IsPrime(const U number)
{
	if (number < 3)
		return number == 2;
	if (0 == number%2)
		return false;

	const U max = static_cast<U>(sqrt(number));
	size_t i;
	for (i = 3; (i <= max) && (number%i); i+=2);
	return (max < i);
}

static 
UIntType LargestPrimeFactor_2_Base(const UIntType number)
{
	if (number%2 == 0) {
		auto candidate =  LargestPrimeFactor_2_Base(number/2);
		return candidate > 1 ? candidate : 2;
	}

	UIntType largest = 1;
	const auto max = static_cast<UIntType>(sqrt(number));
	for (size_t i = 3; i <= max; i+=2)
	{
		if (number%i)
			continue;
		if (IsPrime(i))
			largest = i;
		if (number/i > largest) {
			auto candidate = LargestPrimeFactor_2_Base(number/i);
			if (candidate > largest) {
				//std::cout<<"132: " << i << " " << candidate << " " << largest << std::endl;
				return candidate;
			}
		}
	}
	if (largest < 3)
		if (largest == 1 || IsPrime(number/largest))
			return number/largest;

	return largest;
}

//	same as the previous, but reverses the comparisons order: IsPrime, then division
static 
UIntType LargestPrimeFactor_3_Base(const UIntType number)
{
	UIntType largest = !(number%2) ? 2 : 1;

	const auto max = static_cast<UIntType>(sqrt(number));
	for (size_t i = 3; i <= max; i+=2)
	{
		if (IsPrime(i) && !(number%i))
			largest = i;
	}

	return largest;
}

//	same as version 2, but 
static 
UIntType LargestPrimeFactor_4_Base(const UIntType number)
{
	UIntType largest = !(number%2) ? 2 : 1;

	const UIntType max = static_cast<UIntType>(sqrt(number));
	for (size_t i = 3; i <= max; i+=2)
	{
		if (IsPrime(i) && !(number%i))
			largest = i;
	}

	return largest;
}

static
UIntType LargestPrimeFactor_Wrapper(const UIntType number, unsigned index)
{
	switch (index)
	{
	case 1:
		return LargestPrimeFactor_1_Base(number);
	case 2:
		return LargestPrimeFactor_2_Base(number);
	case 3:
		return LargestPrimeFactor_3_Base(number);
	default:
		ATLASSERT(false && "LargestPrimeFactor_W_25");
		return 0;
	}
}

static
UIntType LargestPrimeFactor_WrapperDebug(const UIntType number, unsigned index, bool debug)
{
	if (debug)
	{
		std::string func("LargestPrimeFactor_");
		func += ('0'+(char)index);
		func += (", ");
		std::stringstream ss;
		ss << number;
		func += ss.str();
		DbgCnt cnt(func.c_str());

		return LargestPrimeFactor_Wrapper(number, index);
	}
	else
		return LargestPrimeFactor_Wrapper(number, index);
}

static inline
UIntType LargestPrimeFactor_1(const UIntType number)
{
	return LargestPrimeFactor_WrapperDebug(number, 1, s_debug);
}

static inline
UIntType LargestPrimeFactor_2(const UIntType number)
{
	return LargestPrimeFactor_WrapperDebug(number, 2, s_debug);
}

static inline
UIntType LargestPrimeFactor_3(const UIntType number)
{
	return LargestPrimeFactor_WrapperDebug(number, 3, s_debug);
}

void debug_assert()
{
	assert(29 == LargestPrimeFactor_1(13195));
	assert(6857 == LargestPrimeFactor_1(600851475143));
	assert(29 == LargestPrimeFactor_2(13195));
	assert(6857 == LargestPrimeFactor_2(600851475143));
	assert(29 == LargestPrimeFactor_3(13195));
	assert(6857 == LargestPrimeFactor_3(600851475143));

	assert(17 == LargestPrimeFactor_2(17));
}

UIntType LargestPrimeFactor()
{ 
	if (0)
	{
		std::vector<UIntType> sieve;
		SieveOfEratosthenes(sieve, 3000, 10000);
		for (size_t i = 0; i < sieve.size(); i+=2)
			if (sieve[i])
				std::cout<<sieve[i]<<" ";
		std::cout<<std::endl;
	}

 	debug_assert();
	return LargestPrimeFactor_2(600851475143);
}

size_t largest_prime_factor(size_t number)
{
	debug_assert();
	return LargestPrimeFactor_WrapperDebug(number, 2, false);
}

std::uint64_t Problem3()
{
	return LargestPrimeFactor();
}