cmake_minimum_required(VERSION 2.8)
project(algorithms CXX)

set(CMAKE_CXX_FLAGS "-std=c++11 -Wall -Wextra")

## GTest
add_subdirectory(google-test)
enable_testing()
include_directories(${gtest_SOURCE_DIR}/include ${gtest_SOURCE_DIR})

set(BST_FROM_ARRAY_SOURCES bst_from_array.cpp)
add_executable("bst_from_array" ${BST_FROM_ARRAY_SOURCES})
target_link_libraries("bst_from_array" gtest gtest_main)
add_test("bst_from_array" "bst_from_array")

add_subdirectory(potyczki-algorytmiczne/13)

