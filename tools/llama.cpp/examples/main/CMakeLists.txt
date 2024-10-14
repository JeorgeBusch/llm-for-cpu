set(TARGET llama-cli)
add_executable(${TARGET} main.cpp)
install(TARGETS ${TARGET} RUNTIME)
target_link_libraries(${TARGET} PRIVATE common llama ${CMAKE_THREAD_LIBS_INIT})
target_compile_features(${TARGET} PRIVATE cxx_std_11)

get_target_property(MAIN_CFLAGS llama-cli  COMPILE_OPTIONS)
# also see: COMPILE_DEFINITIONS INCLUDE_DIRECTORIES
message("-- Target compiler flags are: ${MAIN_CFLAGS}")

add_custom_command(TARGET llama-cli POST_BUILD
COMMAND echo ${TARGET} built with the flags: ${MAIN_CFLAGS})