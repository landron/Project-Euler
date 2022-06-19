#[[
	VsDevCmd.bat -arch=amd64
	cd F:\_Devel\build\proj-euler
	cmake -G Ninja -DCMAKE_BUILD_TYPE=Debug <path to CMakeLists.txt folder>
]]
cmake_minimum_required(VERSION 3.12)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

project(project-euler)

set(sources main.cpp "Problem 1 - Multiples of 3 and 5.cpp")
add_executable(${PROJECT_NAME} ${sources})
