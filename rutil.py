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
from time import time

random = Random(int(time()))


def read_file(filename):
    contents = ""
    fp = os.open(filename, os.O_RDONLY, 0777)
    read = os.read(fp, 4096)
    while len(read):
        contents += read
        read = os.read(fp, 4096)
    os.close(fp)
    return contents


def random_integer(min=0, max=None):
    i = random.genrand32()
    if max is not None:
        assert max > min
        range = max + 1 - min
        assert range > 0
        i = i % range + min
    return i
