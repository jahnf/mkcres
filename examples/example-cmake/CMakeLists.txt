# mkcres example-01
# resources in a minimal example that can list its included resources
# * Visit https://github.com/jahnf/mkcres for more details

cmake_minimum_required(VERSION 2.8.0)
set(CMAKE_LEGACY_CYGWIN_WIN32 0) # Remove when CMake >= 2.8.4 is required

project(example01)

include(../../mkcres.cmake)
mkcres_add_library(myresources "resources.json" "../..")

add_executable(example01 main.c)
target_link_libraries(example01 myresources)
