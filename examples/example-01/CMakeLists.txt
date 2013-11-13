# mkcres example-01
# resources in a minimal example that can list its included resources

cmake_minimum_required(VERSION 2.8.0)
project(example01)

include(../../mkcres.cmake)
mkcres_add_library(myresources "resources.json" "../..")

add_executable(example01 main.c)
target_link_libraries(example01 myresources)
