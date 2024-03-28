cmake_minimum_required(VERSION 3.5...3.26)
project(bert_sst)
find_package(pybind11 REQUIRED)  # or `add_subdirectory(pybind11)`
add_executable(bert_sst bert_sst.cpp)
target_link_libraries(bert_sst PRIVATE pybind11::embed)