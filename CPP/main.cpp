#include "Perform.h"

extern std::uint64_t Problem1();

void parse_input()
{
	extern std::uint64_t Multiples3and5(const std::uint64_t below);

	unsigned tests_no;
	std::cin >> tests_no;
	for (size_t i = 0; i < tests_no; ++i) {
		unsigned limit;
		std::cin >> limit;
		std::cout<<Multiples3and5(limit)<<std::endl;
	}
}

int main()
{
	//std::cout<<std::endl<<"Solution: "<<Problem1()<<std::endl;
	parse_input();

	return 0;
}