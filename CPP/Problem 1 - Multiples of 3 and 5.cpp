//	Version:	2013.12.10

#include <cstdint>
#include <sstream>
#include <atlbase.h>
#include <cassert>

#include "Perform.h"

typedef std::uint64_t UIntType;

static bool s_debug = false;

static 
UIntType MultiplesDe3Et5_1_B(const UIntType below)
{
	UIntType sum = 0;
	for (UIntType i = 0; i < below; ++i)
		if (!(i%3) || !(i%5))
			sum += i;
	return sum;
}

static 
UIntType MultiplesDe3Et5_2_B(const UIntType below)
{
	UIntType sum = 0;

	UIntType i = 0;
	for (i = 3; i < below; i+=3)
		sum += i;

	//	avoid 3 divisors already added
	for (i = 0; (i+10) < below; i+=15)
		sum += (2*i+15);
	for (;i < below; ++i)
		if (!(i%5) && (i%3))
			sum += i;

	return sum;
}

//	it calculates immediately
static 
UIntType MultiplesDe3Et5_3_B(const UIntType below)
{
	UIntType sum = 0;

	UIntType end3 = below/3;
	if (0 == below%3)
		--end3;
	sum += (3*end3*(end3+1))/2;

	//	avoid 3 divisors already added
	UIntType end5 = below/5;
	if (0 == below%5)
		--end5;
	end3 = end5/3;
	sum += 5*(end5*(end5+1) - 3*end3*(end3+1))/2;

	return sum;
}

static inline
UIntType MultiplesDe3Et5_W(const UIntType below, unsigned index)
{
	switch (index)
	{
	case 1:
		return MultiplesDe3Et5_1_B(below);
	case 2:
		return MultiplesDe3Et5_2_B(below);
	case 3:
		return MultiplesDe3Et5_3_B(below);
	default:
		assert(false && "MultiplesDe3Et5_W_44");
		return 0;
	}
}

static
UIntType MultiplesDe3Et5_WD(const UIntType below, unsigned index, bool debug)
{
	if (debug)
	{
		std::string func("MultiplesDe3Et5_");
		func += ('0'+(char)index);
		func += (", ");
		std::stringstream ss;
		ss << below;
		func += ss.str();
		DbgCnt cnt(func.c_str());

		return MultiplesDe3Et5_W(below, index);
	}
	else
		return MultiplesDe3Et5_W(below, index);
}

static inline
UIntType MultiplesDe3Et5_1(const UIntType below)
{
	return MultiplesDe3Et5_WD(below, 1, s_debug);
}

static inline
UIntType MultiplesDe3Et5_2(const UIntType below)
{
	return MultiplesDe3Et5_WD(below, 2, s_debug);
}

static inline
UIntType MultiplesDe3Et5_3(const UIntType below)
{
	return MultiplesDe3Et5_WD(below, 3, s_debug);
}

UIntType MultiplesDe3Et5()
{
	//	variant 3:	it calculates immediately
	ATLASSERT(23 == MultiplesDe3Et5_1(10));
	ATLASSERT(23 == MultiplesDe3Et5_2(10));
	ATLASSERT(23 == MultiplesDe3Et5_3(10));
	ATLASSERT(2318 == MultiplesDe3Et5_1(100));
	ATLASSERT(2318 == MultiplesDe3Et5_2(100));
	ATLASSERT(2318 == MultiplesDe3Et5_3(100));
	ATLASSERT(233168 == MultiplesDe3Et5_1(1000));
	ATLASSERT(233168 == MultiplesDe3Et5_2(1000));
	ATLASSERT(233168 == MultiplesDe3Et5_3(1000));
	ATLASSERT(23331668 == MultiplesDe3Et5_1(10000));
	ATLASSERT(23331668 == MultiplesDe3Et5_2(10000));
	ATLASSERT(23331668 == MultiplesDe3Et5_3(10000));
	ATLASSERT(2333316668 == MultiplesDe3Et5_1(100000));
	ATLASSERT(2333316668 == MultiplesDe3Et5_2(100000));	
	ATLASSERT(2333316668 == MultiplesDe3Et5_3(100000));	
	/*
		31, 0, 234, 32
		31, 0, 296, 31
		31, 0, 265, 16
	*/
	ATLASSERT(233333166668 == MultiplesDe3Et5_1(1000000));
	ATLASSERT(233333166668 == MultiplesDe3Et5_2(1000000));
	ATLASSERT(233333166668 == MultiplesDe3Et5_3(1000000));
	ATLASSERT(23333331666668 == MultiplesDe3Et5_1(10000000));
	ATLASSERT(23333331666668 == MultiplesDe3Et5_2(10000000));
	ATLASSERT(23333331666668 == MultiplesDe3Et5_3(10000000));
	//	2449, 234	2449, 219	2433, 234
	ATLASSERT(2333333316666668 == MultiplesDe3Et5_1(100000000));
	ATLASSERT(2333333316666668 == MultiplesDe3Et5_2(100000000));
	ATLASSERT(2333333316666668 == MultiplesDe3Et5_3(100000000));

	return MultiplesDe3Et5_3(1000);
}

std::uint64_t Problem1()
{
	return MultiplesDe3Et5();
}

size_t Multiples3and5(const size_t below)
{
	return MultiplesDe3Et5_WD(below, 3, s_debug);
}