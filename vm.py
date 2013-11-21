class VirtualMachine(object):
    def __init__(self, program, stack):
        self.pc = 0
        self.halt = False
        self.stack = stack
        self.program = program

    def mainloop(self):
        while not self.halt and self.pc < len(self.program):
            instruction, argument = self.program[self.pc]
            instruction(self, argument)
            self.pc += 1
        return 0