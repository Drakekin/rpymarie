from opcodes import instruction_to_string, INSTRUCTIONS

try:
    from rpython.rlib.jit import JitDriver
except ImportError:
    class JitDriver(object):
        def __init__(self, **kw):
            pass

        def jit_merge_point(self, **kw):
            pass

        def can_enter_jit(self, **kw):
            pass


def get_printable_location(pc, program):
    a = max(0, pc - 2)
    b = min(len(program)-1, pc + 2)
    assert a > 0
    assert b > 0
    instructions = program[a:b]
    excerpt = []
    for n, line in enumerate(instructions):
        excerpt.append("%s %s: %s" % (">" if n + a == pc else " ", n + a, instruction_to_string(*program[n+a])))
    return "\n".join(excerpt)


jit_driver = JitDriver(greens=[
    "pc",
    "program",
], reds=[
    "halt",
    "stack",
    "vm"
], get_printable_location=get_printable_location)


class VirtualMachine(object):
    #__immutable_fields__ = ["program[*]"]

    def __init__(self, program, stack):
        self.pc = 0
        self.halt = False
        self.stack = stack
        self.program = program

    def mainloop(self):
        while not self.halt and self.pc < len(self.program):
            pc, stack, program, halt = self.pc, self.stack, self.program, self.halt
            jit_driver.jit_merge_point(pc=pc, program=program, halt=halt, stack=stack, vm=self)
            self.pc, self.stack, self.program, self.halt = pc, stack, program, halt

            instruction, argument = self.program[self.pc]
            opcode = INSTRUCTIONS[instruction]
            opcode(self, argument)
            self.pc += 1
        return 0