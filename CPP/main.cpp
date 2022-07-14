#include <iostream>

// #include "Perform.h"

// extern std::uint64_t Problem1();
extern size_t Multiples3and5(size_t below);
extern size_t even_Fibonacci_sum(size_t below);

namespace problem_1 {
void parse_input()
{
	unsigned tests_no;
	std::cin >> tests_no;
	for (size_t i = 0; i < tests_no; ++i) {
		unsigned limit;
		std::cin >> limit;
		std::cout<<Multiples3and5(limit)<<std::endl;
	}
}
}

namespace problem_2 {
void parse_input()
{
	size_t tests_no;
	std::cin >> tests_no;
	for (size_t i = 0; i < tests_no; ++i) {
		size_t limit;
		std::cin >> limit;
		std::cout<<even_Fibonacci_sum(limit)<<std::endl;
	}
}
}

int main()
{
	//std::cout<<std::endl<<"Solution: "<<Problem1()<<std::endl;
	//problem_1::parse_input();
	problem_2::parse_input();

	return 0;
}