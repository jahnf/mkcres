#!/bin/bash
set -e

SCRIPT_DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
TEST_DIR="build_and_test"

# since travis-ci only sets CC environment 
[ -z "$CC" ] || export CXX="$CC"

# build
rm -rf $TEST_DIR
mkdir -p $TEST_DIR && cd $TEST_DIR
cmake $SCRIPT_DIR
make

# run test executables
./test_c
./test_cpp

# export resources from the c test executable
# and compare them with the original input file.
./test_c images/linux_logo.jpg output_file
cmp output_file ${SCRIPT_DIR}/linux_logo.jpg
./test_c data-files/FILE01 output_file
cmp output_file ${SCRIPT_DIR}/FILE01
./test_c data-files/FILE02 output_file
cmp output_file ${SCRIPT_DIR}/FILE02
./test_c data-files/FILE03 output_file
cmp output_file ${SCRIPT_DIR}/FILE03
./test_c images/tux.jpg output_file
cmp output_file ${SCRIPT_DIR}/linux_logo.jpg

# export resources from the cpp test executable
# and compare them with the original input file.
./test_cpp images/linux_logo.jpg output_file
cmp output_file ${SCRIPT_DIR}/linux_logo.jpg
./test_cpp data-files/FILE01 output_file
cmp output_file ${SCRIPT_DIR}/FILE01
./test_cpp data-files/FILE02 output_file
cmp output_file ${SCRIPT_DIR}/FILE02
./test_cpp data-files/FILE03 output_file
cmp output_file ${SCRIPT_DIR}/FILE03
./test_cpp images/tux.jpg output_file
cmp output_file ${SCRIPT_DIR}/linux_logo.jpg
./test_cpp source-main.cpp output_file
cmp output_file ${SCRIPT_DIR}/main.cpp
./test_cpp source-main.c output_file
cmp output_file ${SCRIPT_DIR}/main.c
./test_cpp images/penguin.jpg output_file
cmp output_file ${SCRIPT_DIR}/linux_logo.jpg

# modify a resource file, build and compare again
echo `date` >> ${SCRIPT_DIR}/FILE01
make
./test_c data-files/FILE01 output_file
cmp output_file ${SCRIPT_DIR}/FILE01
./test_cpp data-files/FILE01 output_file
cmp output_file ${SCRIPT_DIR}/FILE01

echo "DONE."