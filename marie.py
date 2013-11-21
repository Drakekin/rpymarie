from opcodes import INSTRUCTIONS, skip
from vm import VirtualMachine


def run(source, args):
    program = parse(source)
    args = [int(arg) for arg in args]
    vm = VirtualMachine(program, list(reversed(args)))
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
            num_arguments, instruction = INSTRUCTIONS.get(tokens[0], (-1, lambda: None))
            arguments = tokens[1:]
            if num_arguments != len(arguments):
                raise SyntaxError("Line %s: %s\nSyntax Error.\n%s takes %s arguments, %s given." % (
                    line_no, line, tokens[0], num_arguments, len(arguments)
                ))
            code.append((instruction, arguments))
    program = []
    for func, args in code:
        program.append((func, [labels.get(arg, arg) for arg in args]))
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
