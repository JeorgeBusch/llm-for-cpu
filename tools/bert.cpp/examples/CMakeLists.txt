include_directories(${CMAKE_SOURCE_DIR}/)

set(CMAKE_CXX_FLAGS "-I../../../../include")

if (MSVC)
    if (BERT_AVX2)
        add_compile_options(/arch:AVX2)
    elseif (BERT_AVX)
        add_compile_options(/arch:AVX)
    endif()
endif()

if(WIN32)
add_definitions(-DNOMINMAX=1)
endif()


add_executable(server server.cpp)
if(NOT WIN32)
	target_link_libraries(server PRIVATE bert ggml)
else()
	target_link_libraries(server PRIVATE bert ggml ws2_32)
endif()
add_executable(main main.cpp)
target_link_libraries(main PRIVATE bert ggml)

add_executable(fp16_dot fp16_dot.cpp)
target_link_libraries(fp16_dot PRIVATE bert ggml /mnt/c/Users/aej45/Desktop/llm-for-cpu/util/m5/build/x86/out/libm5.a)

add_executable(test_tokenizer test_tokenizer.cpp)
target_link_libraries(test_tokenizer PRIVATE bert ggml)