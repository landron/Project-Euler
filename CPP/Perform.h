#pragma once

#include <iostream>
#include <string>
#include <chrono>

class DbgCnt
{
public:
	DbgCnt(const char* function);
	~DbgCnt();

private:
	std::chrono::time_point<std::chrono::high_resolution_clock> m_cnt;
	const std::string m_text;
};

inline DbgCnt::DbgCnt(const char* function):
	m_cnt(std::chrono::high_resolution_clock::now()),
	m_text(function)
{}

inline DbgCnt::~DbgCnt()
{
	const auto elapsed = std::chrono::high_resolution_clock::now()-m_cnt;
	const auto microseconds = std::chrono::duration_cast<std::chrono::microseconds>(elapsed).count();

	std::cout<<m_text.c_str()<<" : "<<microseconds<<" ms."<<std::endl;
}