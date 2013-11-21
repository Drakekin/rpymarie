import os
from rutil import random_integer

INSTRUCTIONS = {}


def register_instruction(instruction, arguments=0):
    def register(function):
        assert function.func_code.co_argcount == arguments + 1, \
            "{} (for instruction {}) must have {} arguments, has {}.".format(
                function.__name__,
                instruction,
                arguments + 1,
                function.func_code.co_argcount
            )
        INSTRUCTIONS[instruction] = arguments, function
        return function
    return register


@register_instruction("DEC", 1)
def push_decimal(vm, value):
    try:
        vm.stack.append(int(value))
    except ValueError:
        vm.panic = "Cannot push {0} to the stack, {0} is not a number.".format(value)


@register_instruction("HEX", 1)
def push_hex(vm, value):
    try:
        vm.stack.append(int(value, 16))
    except ValueError:
        vm.panic = "Cannot push {0} to the stack, {0} is not hex.".format(value)


@register_instruction("STRING", 1)
def push_string(vm, value):
    vm.stack = [ord(c) for c in value] + [0] + vm.stack


@register_instruction("ASCII", 1)
def push_ascii(vm, value):
    vm.stack(ord(value))


@register_instruction("PRINT")
def print_ascii(vm):
    os.write(1, unichr(vm.stack.pop()))


@register_instruction("WRITE")
def print_ascii(vm):
    os.write(1, str(vm.stack.pop()))


@register_instruction("ADD")
def add(vm):
    a = vm.stack.pop()
    b = vm.stack.pop()
    vm.stack.append(b + a)


@register_instruction("SUB")
def subtract(vm):
    a = vm.stack.pop()
    b = vm.stack.pop()
    vm.stack.append(b - a)


@register_instruction("MUL")
def multiply(vm):
    a = vm.stack.pop()
    b = vm.stack.pop()
    vm.stack.append(b * a)


@register_instruction("DIV")
def divide(vm):
    a = vm.stack.pop()
    b = vm.stack.pop()
    vm.stack.append(b / a)


@register_instruction("MOD")
def modulo(vm):
    a = vm.stack.pop()
    b = vm.stack.pop()
    vm.stack.append(b % a)


@register_instruction("JUMP", 1)
def jump(vm, address):
    try:
        location = (int(address) + len(vm.program)) % len(vm.program)
        vm.pc = location - 1
    except ValueError:
        vm.panic = "Cannot JUMP to {0}, {0} is not an address!".format(address)


@register_instruction("IFZERO", 2)
def ifzero(vm, then, otherwise):
    if vm.stack.pop() == 0:
        jump(vm, then)
    else:
        jump(vm, otherwise)


@register_instruction("IFPOS", 2)
def ifpos(vm, then, otherwise):
    if vm.stack.pop() > 0:
        jump(vm, then)
    else:
        jump(vm, otherwise)


@register_instruction("IFNEG", 2)
def ifneg(vm, then, otherwise):
    if vm.stack.pop() < 0:
        jump(vm, then)
    else:
        jump(vm, otherwise)


@register_instruction("COPY")
def copy(vm):
    val = vm.stack.pop()
    vm.stack.append(val)
    vm.stack.append(val)


@register_instruction("FLIP")
def flip(vm):
    a = vm.stack.pop()
    b = vm.stack.pop()
    vm.stack.append(a)
    vm.stack.append(b)


@register_instruction("SKIP")
def skip(vm):
    vm.pc += 1


@register_instruction("RAND")
def random(vm):
    a = vm.stack.pop()
    b = vm.stack.pop()
    vm.stack.append(random_integer(b, a))


@register_instruction("DIE")
def die(vm):
    vm.halt = True


@register_instruction("BUBBLE")
def bubble(vm):
    n = vm.stack.pop()
    val = vm.stack[-n]
    del vm.stack[-n]
    vm.stack.append(val)


@register_instruction("CLONE")
def clone(vm):
    n = vm.stack.pop()
    val = vm.stack[-n]
    vm.stack.append(val)


@register_instruction("PUT")
def put(vm):
    n = vm.stack.pop()
    val = vm.stack.pop()
    vm.stack[-n] = val


@register_instruction("POP")
def pop(vm):
    vm.stack.pop()
