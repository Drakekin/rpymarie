import os
try:
    from rpython.rlib.rrandom import Random
except ImportError:
    import random as cpython_random

    # Shim for running in cpython
    class Random(object):
        def __init__(self, seed=0):
            cpython_random.seed(seed)

        def genrand32(self):
            return cpython_random.randint(0, 2**32-1)
try:
    from rpython.rlib.rarithmetic import intmask
except ImportError:
    def intmask(n):
        return int(n)
from time import time

random = Random(int(time()))


def is_hex(char):
    for x in char.lower():
        if not x in "0123456789abcdef":
            return False
    return True


def read_file(filename):
    contents = ""
    fp = os.open(filename, os.O_RDONLY, 0777)
    read = os.read(fp, 4096)
    while len(read):
        contents += read
        read = os.read(fp, 4096)
    os.close(fp)
    return contents


def random_integer(n):
    assert n > 0
    return intmask(random.genrand32()) % n
