//	Version:	2013.12.11, 2

#include <cstdint>
#include <sstream>
#include <atlbase.h>

#include "Perform.h"

typedef std::uint64_t UIntType;

static bool s_debug = true;

static 
auto EvenFibonacci_1_B(const UIntType below)
{
	UIntType sum = 0;

	for (UIntType curr = 2, prev = 1; curr < below;)
	{
		if (0 == curr%2)
			sum += curr;

		auto temp = prev;
		prev = curr;
		curr += temp;
	}

	return sum;
}

template <typename T>
static inline
UIntType Fibonacci(T n)
{
	//	(1 + sqrt(5)) / 2
	static double const nombreDOr = 1.61803398874989;
	//	0.5 added to round to the closest integer
	return (UIntType)(0.5 + pow(nombreDOr, n)/sqrt(5));
}

static 
UIntType EvenFibonacci_2_B(const UIntType below)
{
	UIntType sum = 0;
	UIntType next = 0;
	for (size_t i = 0; next < below; i+=3, next = Fibonacci(i))
		sum += next;
	return sum;
}

//ATLASSERT(Fibonacci(33) < 4000000);
//ATLASSERT(Fibonacci(36) > 4000000);
static 
UIntType EvenFibonacci_3_B(const UIntType)
{
	UIntType sum = 0;
	for (size_t i = 3; i < 36; i+=3)
		sum += Fibonacci(i);
	return sum;
}

/*
	F(n) = F(n-1)+F(n-2)=2*F(n-2)+F(n-3)=2F(n-3)+2F(n-4)+F(n-3)=3F(n-3)+2F(n-4)=3F(n-3)+(F(n-4)+F(n-5))+F(n-6)=4F(n-3)+F(n-6)
	From the documentation of the problem, to avoid testing for even
*/
static 
UIntType EvenFibonacci_4_B(const UIntType below)
{
	UIntType sum = 2;

	UIntType prev = 2;
	for (UIntType curr = 8; curr < below; )
	{
		sum += curr;

		UIntType temp = prev;
		prev = curr;
		curr = (4*curr+temp);
	}

	return sum;
}

//	also from the documentation of the problem
static 
UIntType EvenFibonacci_5_B(const UIntType below)
{
	UIntType sum = 0;

	UIntType prev = 1;
	for (UIntType curr = 2; curr < below;)
	{
		sum += curr;

		UIntType next = prev+curr;
		prev = next+curr;
		curr = prev+next;
	}

	return sum;
}

static
UIntType EvenFibonacci_W(const UIntType below, unsigned index)
{
	switch (index)
	{
	case 1:
		return EvenFibonacci_1_B(below);
	case 2:
		return EvenFibonacci_2_B(below);
	case 3:
		return EvenFibonacci_3_B(below);
	case 4:
		return EvenFibonacci_4_B(below);
	case 5:
		return EvenFibonacci_5_B(below);
	default:
		ATLASSERT(false && "EvenFibonacci_W_112");
		return 0;
	}
}

static inline
UIntType EvenFibonacci_WD(UIntType below, unsigned index, bool debug)
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

		return EvenFibonacci_W(below, index);
	}
	else
		return EvenFibonacci_W(below, index);
}

static inline
UIntType EvenFibonacci_1(const UIntType below)
{
	return EvenFibonacci_WD(below, 1, s_debug);
}

static inline
UIntType EvenFibonacci_2(const UIntType below)
{
	return EvenFibonacci_WD(below, 2, s_debug);
}

static inline
UIntType EvenFibonacci_3(const UIntType below)
{
	return EvenFibonacci_WD(below, 3, s_debug);
}

static inline
UIntType EvenFibonacci_4(const UIntType below)
{
	return EvenFibonacci_WD(below, 4, s_debug);
}

static inline
UIntType EvenFibonacci_5(const UIntType below)
{
	return EvenFibonacci_WD(below, 5, s_debug);
}

UIntType EvenFibonacci(UIntType below)
{
	//for (int i = 1; i < 100; ++i)
	//	std::cout<<i<<" : "<<Fibonacci(i)<<std::endl;
	//std::cout<<std::endl;
	static const unsigned FIBONACCI[] = {1,1,2,3,5,8,13,21,34,55,89,144};
	for (int i = 0; i < sizeof(FIBONACCI)/sizeof(FIBONACCI[0]); ++i)
		ATLASSERT(FIBONACCI[i] == Fibonacci(1+i));
	ATLASSERT(Fibonacci(33) < 4000000);
	ATLASSERT(Fibonacci(36) > 4000000);

	ATLASSERT(10 == EvenFibonacci_1(10));
	ATLASSERT(10 == EvenFibonacci_2(10));
	ATLASSERT(10 == EvenFibonacci_4(10));
	ATLASSERT(10 == EvenFibonacci_5(10));
	ATLASSERT(44 == EvenFibonacci_1(40));
	ATLASSERT(44 == EvenFibonacci_2(40));
	ATLASSERT(44 == EvenFibonacci_4(40));
	ATLASSERT(44 == EvenFibonacci_5(40));
	ATLASSERT(44 == EvenFibonacci_1(100));
	ATLASSERT(44 == EvenFibonacci_2(100));
	ATLASSERT(44 == EvenFibonacci_4(100));
	ATLASSERT(44 == EvenFibonacci_5(100));
	ATLASSERT(798 == EvenFibonacci_1(1000));
	ATLASSERT(798 == EvenFibonacci_2(1000));
	ATLASSERT(798 == EvenFibonacci_4(1000));
	ATLASSERT(798 == EvenFibonacci_5(1000));
	ATLASSERT(3382 == EvenFibonacci_1(4000));
	ATLASSERT(3382 == EvenFibonacci_2(4000));
	ATLASSERT(3382 == EvenFibonacci_4(4000));
	ATLASSERT(3382 == EvenFibonacci_5(4000));
	ATLASSERT(3382 == EvenFibonacci_1(10000));
	ATLASSERT(3382 == EvenFibonacci_2(10000));
	ATLASSERT(3382 == EvenFibonacci_4(10000));
	ATLASSERT(3382 == EvenFibonacci_5(10000));
	ATLASSERT(4613732 == EvenFibonacci_1(4000000));
	ATLASSERT(4613732 == EvenFibonacci_2(4000000));
	ATLASSERT(4613732 == EvenFibonacci_3(4000000));
	ATLASSERT(4613732 == EvenFibonacci_4(4000000));
	ATLASSERT(4613732 == EvenFibonacci_5(4000000));
	ATLASSERT(EvenFibonacci_1(40000000) == EvenFibonacci_2(40000000));
	ATLASSERT(EvenFibonacci_1(400000000) == EvenFibonacci_2(400000000));
	ATLASSERT(EvenFibonacci_1(4000000000) == EvenFibonacci_2(4000000000));
	ATLASSERT(EvenFibonacci_1(10000000000) == EvenFibonacci_2(10000000000));
	ATLASSERT(EvenFibonacci_1(100000000000) == EvenFibonacci_2(100000000000));
	ATLASSERT(EvenFibonacci_1(1000000000000) == EvenFibonacci_2(1000000000000));

	return EvenFibonacci_1(below);
}

size_t even_Fibonacci_sum(size_t below)
{
	return EvenFibonacci_WD(below, 1, false);
}

std::uint64_t Problem2()
{
	return EvenFibonacci(4000000);
}
