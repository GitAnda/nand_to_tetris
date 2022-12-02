from pathlib import Path
from argparse import ArgumentParser

SEG = {"local": "LCL", "argument": "ARG", "this": "THIS", "that": "THAT", "temp": "5"}

class Parser:
    def __init__(self, path):
        self.path = Path(path)
        self.f = open(path, "r")

    @staticmethod
    def sanitize(line):
        return line.split('//')[0].strip()

    @staticmethod
    def components(line):
        comp = line.split()
        if len(comp) == 3:
            return tuple(comp)
        if len(comp) == 2:
            return *comp, None
        if len(comp) == 1:
            return *comp, None, None

    def get_next(self):
        line = self.f.readline()
        if not line:  # end of file
            return None
        sline = self.sanitize(line)
        if not sline:  # comment
            return self.get_next()
        return self.components(line)


class CodeWriter:
    def __int__(self, path):
        self.path = Path(path)
        self.f = open(self.path, 'w')

    def write_next(self, components):
        command, _, _ = components
        if command == "push" or command == "pop":
            self.write_push_pop(components)
        else:
            self.write_arithmetic(components)

    def write_arithmetic(self, components):
        pass

    def write_push_pop(self, components):
        command, segment, location = components
        if command == 'pop':
            if segment in SEG.keys():
                seg = SEG[segment]
                self.f.write(f"@{seg}\nD=M\n@{location}\nD=D+A\n@temp\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@temp\nA=M\nM=D")
        elif command == "push":
            if segment in SEG.keys():
                seg = SEG[segment]
                self.f.write(f"@{location}\nD=A\n@{seg}\nA=M+D\nD=A\n@SP\nA=M\nM=D\n")

    def close(self):
        self.f.close()

if __name__ == "__main__":
    parser = ArgumentParser(description="VM Translator", add_help=False)
    parser.add_argument("path", type=Path, help="VM file")
    # parser.add_argument("outpath", type=Path, help="output file .asm")
    args = parser.parse_args()

    vm = Parser(args.path)
    print(vm.get_next())
    print(vm.get_next())
    print(vm.get_next())
    print(vm.get_next())
