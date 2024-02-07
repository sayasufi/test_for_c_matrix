#! /usr/bin/env python3
from math import sqrt
from parser_header import parser_header
import cffi

def main():
    ffi = cffi.FFI()
    lib = ffi.dlopen('c_code/matrix.so')
    ffi.cdef(parser_header())

    lst = list(range(8))
    len_lst = len(lst)
    arr_var = ffi.new('double[]', lst)
    print(arr_var, type(arr_var))
    res = lib.AbsWideVect(len_lst, arr_var)
    print(f"Sum of {lst} is {res}", sqrt(sum(map(lambda x: x**2, lst))))



if __name__ == "__main__":
    main()