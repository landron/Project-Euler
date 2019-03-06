#[[
	Packages
	  * vcpkg install gtest --triplet x64-windows
	  * vcpkg install bigint --triplet x64-windows

    Knowledge Base
      * vcpkg stuff
        https://github.com/landron/workshop/blob/master/c%2B%2B/11-tests-collection/cpp17/copy-elision/CMakeLists.txt

    \todo:  tag_ub_1
    ]]
cmake_minimum_required(VERSION 3.12)

if(DEFINED ENV{VCPKG_ROOT} AND NOT DEFINED CMAKE_TOOLCHAIN_FILE)
    set(VCPKG_ROOT "$ENV{VCPKG_ROOT}")
    message(STATUS "VCPKG_ROOT=${VCPKG_ROOT}")
    set(CMAKE_TOOLCHAIN_FILE "${VCPKG_ROOT}/scripts/buildsystems/vcpkg.cmake" CACHE FILEPATH "")
endif()

set(CMAKE_CXX_STANDARD 14)  # 20, 17 not supported by HackerRank
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

project(happy-numbers)

find_package(GTest MODULE REQUIRED)
find_library(BigInt bigint)
# It builds without ... . Does it help with something ? Path still not found ...
find_path(BigIntInc "bigint/BigIntegerLibrary.hh")

add_executable(${PROJECT_NAME} main.cpp TinyBigInt.h)
target_include_directories(${PROJECT_NAME} PRIVATE ${BigIntInc})
target_link_libraries(${PROJECT_NAME} PRIVATE GTest::GTest GTest::Main ${BigInt})
