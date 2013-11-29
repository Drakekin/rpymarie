import os
from rutil import random_integer, is_hex

INSTRUCTIONS = {}
NAMES = {}


def register_instruction(instruction):
    def register(function):
        INSTRUCTIONS[instruction] = function
        return function
    return register


@register_instruction("DEC")
def DEC(vm, value):
    try:
        vm.append(int(value))
    except ValueError:
        pass


@register_instruction("HEX")
def HEX(vm, value):
    try:
        if is_hex(value):
            vm.append(int(value, 16))
    except ValueError:
        pass


@register_instruction("ASCII")
def ASCII(vm, value):
    assert len(value) == 1
    value = value[0]
    vm.append(ord(value))


@register_instruction("PRINT")
def PRINT(vm, arg):
    os.write(1, chr(vm.pop()))


@register_instruction("WRITE")
def WRITE(vm, arg):
    os.write(1, str(vm.pop()))


@register_instruction("ADD")
def ADD(vm, arg):
    a = vm.pop()
    b = vm.pop()
    vm.append(b + a)


@register_instruction("SUB")
def SUB(vm, arg):
    a = vm.pop()
    b = vm.pop()
    vm.append(b - a)


@register_instruction("MUL")
def MUL(vm, arg):
    a = vm.pop()
    b = vm.pop()
    vm.append(b * a)


@register_instruction("DIV")
def DIV(vm, arg):
    a = vm.pop()
    b = vm.pop()
    vm.append(b / a)


@register_instruction("MOD")
def MOD(vm, arg):
    a = vm.pop()
    b = vm.pop()
    vm.append(b % a)


@register_instruction("JUMP")
def JUMP(vm, address):
    try:
        location = (int(address) + len(vm.program)) % len(vm.program)
        vm.pc = location - 1
    except ValueError:
        pass


@register_instruction("IFZERO")
def IFZERO(vm, then):
    if vm.pop() == 0:
        JUMP(vm, then)


@register_instruction("IFPOS")
def IFPOS(vm, then):
    if vm.pop() > 0:
        JUMP(vm, then)


@register_instruction("IFNEG")
def IFNEG(vm, then):
    if vm.pop() < 0:
        JUMP(vm, then)


@register_instruction("COPY")
def COPY(vm, arg):
    val = vm.pop()
    vm.append(val)
    vm.append(val)


@register_instruction("FLIP")
def FLIP(vm, arg):
    a = vm.pop()
    b = vm.pop()
    vm.append(a)
    vm.append(b)


@register_instruction("SKIP")
def SKIP(vm, arg):
    vm.pc += 1


@register_instruction("RAND")
def RAND(vm, arg):
    n = vm.pop()
    value = random_integer(n)
    vm.append(value)


@register_instruction("DIE")
def DIE(vm, arg):
    vm.halt = True


@register_instruction("BUBBLE")
def BUBBLE(vm, arg):
    n = vm.pop()
    val = vm.get(-n)
    vm.delete(-n)
    vm.append(val)


@register_instruction("CLONE")
def CLONE(vm, arg):
    n = vm.pop()
    val = vm.get(-n)
    vm.append(val)


@register_instruction("PUT")
def PUT(vm, arg):
    n = vm.pop()
    val = vm.pop()
    vm.set(-n, val)


@register_instruction("POP")
def POP(vm, arg):
    vm.pop()
