# mkcres tests
# resources in a minimal example that can list its included resources
# * Visit https://github.com/jahnf/mkcres for more details

cmake_minimum_required(VERSION 2.8.0)
set(CMAKE_LEGACY_CYGWIN_WIN32 0) # Remove when CMake >= 2.8.4 is required

project(mkcres_tests)

include(../mkcres.cmake)
mkcres_add_library(test_resources1 "test_resources1.json" "..")
mkcres_add_library(test_resources2 "test_resources2.json" "..")

add_executable(test_c main.c)
target_link_libraries(test_c test_resources1)

add_executable(test_cpp main.cpp)
target_link_libraries(test_cpp test_resources2)
