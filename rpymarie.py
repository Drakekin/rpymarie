import sys
from marie import run
from rutil import read_file


def jitpolicy(driver):
    from rpython.jit.codewriter.policy import JitPolicy
    return JitPolicy()


def entry_point(argv):
    try:
        filename = argv[1]
        args = argv[2:]
    except IndexError:
        print "You must supply a filename"
        return 1
    return run(read_file(filename), args)


def target(*args):
    return entry_point, None


if __name__ == "__main__":
    entry_point(sys.argv)
