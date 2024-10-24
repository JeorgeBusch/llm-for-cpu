# common

find_package(Threads REQUIRED)

# Build info header
#

set(TARGET build_info)
add_library(${TARGET} OBJECT build-info.cpp)
if (BUILD_SHARED_LIBS)
    set_target_properties(${TARGET} PROPERTIES POSITION_INDEPENDENT_CODE ON)
endif()

set(TARGET common)

add_library(${TARGET} STATIC
    arg.cpp
    arg.h
    base64.hpp
    common.cpp
    common.h
    console.cpp
    console.h
    json-schema-to-grammar.cpp
    json.hpp
    log.cpp
    log.h
    ngram-cache.cpp
    ngram-cache.h
    sampling.cpp
    sampling.h
    train.cpp
    train.h
    )

if (BUILD_SHARED_LIBS)
    set_target_properties(${TARGET} PROPERTIES POSITION_INDEPENDENT_CODE ON)
endif()

set(LLAMA_COMMON_EXTRA_LIBS build_info)

# Use curl to download model url
if (LLAMA_CURL)
    find_package(CURL REQUIRED)
    add_definitions(-DLLAMA_USE_CURL)
    include_directories(${CURL_INCLUDE_DIRS})
    find_library(CURL_LIBRARY curl REQUIRED)
    set(LLAMA_COMMON_EXTRA_LIBS ${LLAMA_COMMON_EXTRA_LIBS} ${CURL_LIBRARY})
endif ()

target_include_directories(${TARGET} PUBLIC .)
target_compile_features   (${TARGET} PUBLIC cxx_std_11)
target_link_libraries     (${TARGET} PRIVATE ${LLAMA_COMMON_EXTRA_LIBS} PUBLIC llama Threads::Threads)
