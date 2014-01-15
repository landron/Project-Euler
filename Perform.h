//	Version:	2013.12.10

#pragma once

#include <iostream>
#include <string>

class DbgCnt
{
public:
	DbgCnt(const char* function);
	~DbgCnt();

private:
	unsigned m_cnt;
	const std::string m_text;
};

inline DbgCnt::DbgCnt(const char* function): m_cnt(::GetTickCount()), m_text(function)
{}

inline DbgCnt::~DbgCnt()
{
	std::cout<<m_text.c_str()<<" : "<<(::GetTickCount()-m_cnt)<<" ms."<<std::endl;
}