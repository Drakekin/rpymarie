class VirtualMachine(object):
    __slots__ = ["pc", "halt", "panic", "stack", "program"]

    def __init__(self, program, stack):
        self.pc = 0
        self.halt = False
        self.panic = ""
        self.stack = stack
        self.program = program

    def mainloop(self):
        while not self.halt and not self.panic and self.pc < len(self.program):
            instruction, arguments = self.program[self.pc]
            arguments = tuple(arguments)
            instruction(self, *arguments)
            self.pc += 1
        if self.panic:
            print self.panic
            return 1
        return 0