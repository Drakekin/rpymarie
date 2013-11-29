from opcodes import INSTRUCTIONS

try:
    from rpython.rlib.jit import JitDriver, elidable
except ImportError:
    def elidable(func):
        return func

    class JitDriver(object):
        def __init__(self, **kw):
            pass

        def jit_merge_point(self, **kw):
            pass

        def can_enter_jit(self, **kw):
            pass

STACK_SIZE = 1024


def get_printable_location(pc, program):
    a = max(0, pc - 2)
    b = min(len(program)-1, pc + 3)
    assert a >= 0
    assert b > 0
    instructions = program[a:b]
    excerpt = []
    for n, line in enumerate(instructions):
        instruction, argument = program[n+a]
        excerpt.append("%s%s:%s %s%s" % (">" if n + a == pc else "", n + a, instruction, argument, "<" if n + a == pc else ""))
    if pc >= len(program):
        excerpt.append(">EOF<;???;???")
    return ";".join(excerpt)


jit_driver = JitDriver(greens=[
    "pc",
    "program",
], reds=[
    "halt",
    "stack",
    "vm"
], get_printable_location=get_printable_location)


class VirtualMachine(object):
    __immutable_fields__ = ["program[*]"]

    def __init__(self, program, stack):
        self.pc = 0
        self.halt = False
        self.stack = stack + ([0] * (STACK_SIZE - len(stack)))
        self.stack_head = len(stack) - 1
        self.program = program

    def pop(self):
        if self.stack_head == 0:
            return 0
        result = self.stack[self.stack_head]
        self.stack_head -= 1
        return result

    def append(self, value):
        self.stack_head += 1
        self.stack[self.stack_head] = value

    def set(self, index, value):
        if index < 0:
            index = self.stack_head + index + 1
        assert self.stack_head >= index >= 0
        self.stack[index] = value

    def get(self, index):
        if index < 0:
            index = self.stack_head + index + 1
        assert self.stack_head >= index >= 0
        return self.stack[index]

    def delete(self, index):
        if index < 0:
            index = self.stack_head + index + 1
        assert self.stack_head >= index >= 0
        for n in range(self.stack_head - index):
            self.stack[index + n] = self.stack[index + n + 1] if index + n + 1 < len(self.stack) else 0
        self.stack_head -= 1

    @elidable
    def fetch_instruction(self, pc):
        instruction, argument = self.program[pc]
        opcode = INSTRUCTIONS[instruction]
        return opcode, argument

    def mainloop(self):
        while not self.halt and self.pc < len(self.program):
            pc, stack, program, halt = self.pc, self.stack, self.program, self.halt
            jit_driver.jit_merge_point(pc=pc, program=program, halt=halt, stack=stack, vm=self)
            self.pc, self.stack, self.program, self.halt = pc, stack, program, halt

            opcode, argument = self.fetch_instruction(pc)
            opcode(self, argument)
            self.pc += 1
        return 0