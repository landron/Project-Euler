//	Version:	2013.12.11

#include <cstdint>
#include <sstream>
#include <atlbase.h>

#include "Perform.h"

typedef std::uint64_t UIntType;

static bool s_debug = true;

static 
UIntType ProblemT_1_B(const UIntType /*below*/)
{
	return 0;
}

static
UIntType ProblemT_W(const UIntType below, unsigned index)
{
	switch (index)
	{
	case 1:
		return ProblemT_1_B(below);
	//case 2:
	//	return ProblemT_2_B(below);
	//case 3:
	//	return ProblemT_3_B(below);
	default:
		ATLASSERT(false && "ProblemT_W_25");
		return 0;
	}
}

static
UIntType ProblemT_WD(const UIntType below, unsigned index, bool debug)
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

		return ProblemT_W(below, index);
	}
	else
		return ProblemT_W(below, index);
}

static inline
UIntType ProblemT_1(const UIntType below)
{
	return ProblemT_WD(below, 1, s_debug);
}

UIntType ProblemT()
{
	return ProblemT_1(1010101);
}

std::uint64_t ProblemN()
{
	return ProblemT();
}