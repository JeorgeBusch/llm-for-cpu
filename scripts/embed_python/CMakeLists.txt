cmake_minimum_required(VERSION 3.5...3.26)
project(bert_sst)
set (PYBIND11_PYTHON_VERSION "3.8.10")# NOT NEEDED???
set(CMAKE_C_COMPILER /usr/bin/gcc-10)
set(CMAKE_CXX_COMPILER /usr/bin/g++-10)

find_package(pybind11 REQUIRED)  # or `add_subdirectory(pybind11)`

add_executable(bert_sst bert_sst.cpp)
target_link_libraries(bert_sst PRIVATE pybind11::embed)