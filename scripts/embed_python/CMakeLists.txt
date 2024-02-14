cmake_minimum_required(VERSION 3.5...3.26)
project(example)
set (PYBIND11_PYTHON_VERSION "3.8.10")# NOT NEEDED???
set(CMAKE_C_COMPILER /usr/bin/gcc-10)
set(CMAKE_CXX_COMPILER /usr/bin/g++-10)

find_package(pybind11 REQUIRED)  # or `add_subdirectory(pybind11)`

add_executable(example test.cpp)
target_link_libraries(example PRIVATE pybind11::embed)