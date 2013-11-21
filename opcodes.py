import os
from rutil import random_integer, is_hex

INSTRUCTIONS = {}


def register_instruction(instruction):
    def register(function):
        INSTRUCTIONS[instruction] = function
        return function
    return register


@register_instruction("DEC")
def push_decimal(vm, value):
    try:
        vm.stack.append(int(value))
    except ValueError:
        pass


@register_instruction("HEX")
def push_hex(vm, value):
    try:
        if is_hex(value):
            vm.stack.append(int(value, 16))
    except ValueError:
        pass


@register_instruction("STRING")
def push_string(vm, value):
    vm.stack = [ord(c) for c in value] + [0] + vm.stack


@register_instruction("ASCII")
def push_ascii(vm, value):
    assert len(value) == 1
    value = value[0]
    vm.stack.append(ord(value))


@register_instruction("PRINT")
def print_ascii(vm, arg):
    os.write(1, chr(vm.stack.pop()))


@register_instruction("WRITE")
def print_ascii(vm, arg):
    os.write(1, str(vm.stack.pop()))


@register_instruction("ADD")
def add(vm, arg):
    a = vm.stack.pop()
    b = vm.stack.pop()
    vm.stack.append(b + a)


@register_instruction("SUB")
def subtract(vm, arg):
    a = vm.stack.pop()
    b = vm.stack.pop()
    vm.stack.append(b - a)


@register_instruction("MUL")
def multiply(vm, arg):
    a = vm.stack.pop()
    b = vm.stack.pop()
    vm.stack.append(b * a)


@register_instruction("DIV")
def divide(vm, arg):
    a = vm.stack.pop()
    b = vm.stack.pop()
    vm.stack.append(b / a)


@register_instruction("MOD")
def modulo(vm, arg):
    a = vm.stack.pop()
    b = vm.stack.pop()
    vm.stack.append(b % a)


@register_instruction("JUMP")
def jump(vm, address):
    try:
        location = (int(address) + len(vm.program)) % len(vm.program)
        vm.pc = location - 1
    except ValueError:
        pass


@register_instruction("IFZERO")
def ifzero(vm, then):
    if vm.stack.pop() == 0:
        jump(vm, then)


@register_instruction("IFPOS")
def ifpos(vm, then):
    if vm.stack.pop() > 0:
        jump(vm, then)


@register_instruction("IFNEG")
def ifneg(vm, then):
    if vm.stack.pop() < 0:
        jump(vm, then)


@register_instruction("COPY")
def copy(vm, arg):
    val = vm.stack.pop()
    vm.stack.append(val)
    vm.stack.append(val)


@register_instruction("FLIP")
def flip(vm, arg):
    a = vm.stack.pop()
    b = vm.stack.pop()
    vm.stack.append(a)
    vm.stack.append(b)


@register_instruction("SKIP")
def skip(vm, arg):
    vm.pc += 1


@register_instruction("RAND")
def random(vm, arg):
    n = vm.stack.pop()
    value = random_integer(n)
    vm.stack.append(value)


@register_instruction("DIE")
def die(vm, arg):
    vm.halt = True


@register_instruction("BUBBLE")
def bubble(vm, arg):
    n = vm.stack.pop()
    val = vm.stack[-n]
    del vm.stack[-n]
    vm.stack.append(val)


@register_instruction("CLONE")
def clone(vm, arg):
    n = vm.stack.pop()
    val = vm.stack[-n]
    vm.stack.append(val)


@register_instruction("PUT")
def put(vm, arg):
    n = vm.stack.pop()
    val = vm.stack.pop()
    vm.stack[-n] = val


@register_instruction("POP")
def pop(vm, arg):
    vm.stack.pop()
