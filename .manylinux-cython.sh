#!/usr/bin/env bash
# Passes the right version of cython into update_cpp.sh for manylinux builds 

shopt -s expand_aliases
alias cython="${BIN}/cython"
source ./update_cpp.sh
