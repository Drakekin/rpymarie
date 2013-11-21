from opcodes import INSTRUCTIONS, skip
from vm import VirtualMachine


def run(source, args):
    program = parse(source)
    args = [int(arg) for arg in args]
    args.reverse()
    vm = VirtualMachine(program, args)
    return vm.mainloop()


def parse(source):
    lines = [l.strip(" ") for l in source.split("\n") if l.strip(" ") and not l.strip(" ").startswith(";")]
    code = []
    labels = {}
    for line_no, line in enumerate(lines):
        tokens = line.split(" ")
        if tokens[-1].startswith("!"):
            label = tokens.pop()
            label = "#" + label.strip(" ").lstrip("!")
            labels[label] = str(line_no)
        if len(tokens):
            instruction = INSTRUCTIONS.get(tokens[0], lambda vm, arg: None)
            argument = tokens[1] if tokens[1:] else "0"  # Zero is the default argument
            code.append((instruction, argument))
    program = []
    for func, arg in code:
        program.append((func, labels.get(arg, arg)))
    return program

if __name__ == "__main__":
    print parse("""
    DEC 15 !fifteen
    HEX a
    ADD
    WRITE
    ; Comments!
    HEX a
    PRINT
    DIE
    
    JUMP #fifteen
    """)
