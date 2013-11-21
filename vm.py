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


jit_driver = JitDriver(greens=[
    "pc",
    "program",
], reds=[
    "halt",
    "stack",
    "vm"
])


class VirtualMachine(object):
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
            instruction(self, argument)
            self.pc += 1
        return 0