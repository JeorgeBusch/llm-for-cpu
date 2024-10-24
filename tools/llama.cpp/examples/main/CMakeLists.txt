set(TARGET llama-cli)
set(CMAKE_CXX_FLAGS "-I../../../../../include")

add_executable(${TARGET} main.cpp)
install(TARGETS ${TARGET} RUNTIME)

get_filename_component(PARENT_DIR ${CMAKE_SOURCE_DIR} DIRECTORY)
get_filename_component(PARENT_DIR ${PARENT_DIR} DIRECTORY)

target_link_libraries(${TARGET} PRIVATE common llama ${CMAKE_THREAD_LIBS_INIT} ${PARENT_DIR}/util/m5/build/x86/out/libm5.a)
target_compile_features(${TARGET} PRIVATE cxx_std_11)

get_target_property(MAIN_CFLAGS llama-cli  COMPILE_OPTIONS)
# also see: COMPILE_DEFINITIONS INCLUDE_DIRECTORIES
message("-- Target compiler flags are: ${MAIN_CFLAGS}")

add_custom_command(TARGET llama-cli POST_BUILD
COMMAND echo ${TARGET} built with the flags: ${MAIN_CFLAGS})