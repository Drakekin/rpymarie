import os
from rutil import random_integer, is_hex

INSTRUCTIONS = {}
NAMES = {}


def register_instruction(instruction):
    def register(function):
        INSTRUCTIONS[instruction] = function
        return function
    return register


def instruction_to_string(command, argument=""):
    string = "%s %s" % (command, argument)
    return string.strip(" ")


@register_instruction("DEC")
def DEC(vm, value):
    try:
        vm.stack.append(int(value))
    except ValueError:
        pass


@register_instruction("HEX")
def HEX(vm, value):
    try:
        if is_hex(value):
            vm.stack.append(int(value, 16))
    except ValueError:
        pass


@register_instruction("STRING")
def STRING(vm, value):
    vm.stack = [ord(c) for c in value] + [0] + vm.stack


@register_instruction("ASCII")
def ASCII(vm, value):
    assert len(value) == 1
    value = value[0]
    vm.stack.append(ord(value))


@register_instruction("PRINT")
def PRINT(vm, arg):
    os.write(1, chr(vm.stack.pop()))


@register_instruction("WRITE")
def WRITE(vm, arg):
    os.write(1, str(vm.stack.pop()))


@register_instruction("ADD")
def ADD(vm, arg):
    a = vm.stack.pop()
    b = vm.stack.pop()
    vm.stack.append(b + a)


@register_instruction("SUB")
def SUB(vm, arg):
    a = vm.stack.pop()
    b = vm.stack.pop()
    vm.stack.append(b - a)


@register_instruction("MUL")
def MUL(vm, arg):
    a = vm.stack.pop()
    b = vm.stack.pop()
    vm.stack.append(b * a)


@register_instruction("DIV")
def DIV(vm, arg):
    a = vm.stack.pop()
    b = vm.stack.pop()
    vm.stack.append(b / a)


@register_instruction("MOD")
def MOD(vm, arg):
    a = vm.stack.pop()
    b = vm.stack.pop()
    vm.stack.append(b % a)


@register_instruction("JUMP")
def JUMP(vm, address):
    try:
        location = (int(address) + len(vm.program)) % len(vm.program)
        vm.pc = location - 1
    except ValueError:
        pass


@register_instruction("IFZERO")
def IFZERO(vm, then):
    if vm.stack.pop() == 0:
        JUMP(vm, then)


@register_instruction("IFPOS")
def IFPOS(vm, then):
    if vm.stack.pop() > 0:
        JUMP(vm, then)


@register_instruction("IFNEG")
def IFNEG(vm, then):
    if vm.stack.pop() < 0:
        JUMP(vm, then)


@register_instruction("COPY")
def COPY(vm, arg):
    val = vm.stack.pop()
    vm.stack.append(val)
    vm.stack.append(val)


@register_instruction("FLIP")
def FLIP(vm, arg):
    a = vm.stack.pop()
    b = vm.stack.pop()
    vm.stack.append(a)
    vm.stack.append(b)


@register_instruction("SKIP")
def SKIP(vm, arg):
    vm.pc += 1


@register_instruction("RAND")
def RAND(vm, arg):
    n = vm.stack.pop()
    value = random_integer(n)
    vm.stack.append(value)


@register_instruction("DIE")
def DIE(vm, arg):
    vm.halt = True


@register_instruction("BUBBLE")
def BUBBLE(vm, arg):
    n = vm.stack.pop()
    val = vm.stack[-n]
    del vm.stack[-n]
    vm.stack.append(val)


@register_instruction("CLONE")
def CLONE(vm, arg):
    n = vm.stack.pop()
    val = vm.stack[-n]
    vm.stack.append(val)


@register_instruction("PUT")
def PUT(vm, arg):
    n = vm.stack.pop()
    val = vm.stack.pop()
    vm.stack[-n] = val


@register_instruction("POP")
def POP(vm, arg):
    vm.stack.pop()
