from argparse import ArgumentParser
from pathlib import Path


class HackAssembler():
    def __init__(self, path: Path):
        self.path = path

        self.register_symbols = {f'R{i}': i for i in range(16)}
        self.available_register = 16
        self.jump_symbols = dict()
        self.instructions = self.set_instructions()

        self.lookup_comp = None

        self.machine_code = self.get_machine_code()

    def convert(self, line):
        pass
    
    def get_machine_code(self):
        for instruction in self.instructions:

        pass

    def find_next_register(self):
        while self.available_register in self.register_symbols.values():
            self.available_register += 1
        
    def set_instructions(self):
        instructions = []
        count = 0
        with open(self.path, 'r') as f:
            for line in f.readlines():
                line = line.strip().replace(' ', '')
                if not line or line[:2] == '//':
                    continue

                if line[0] == '(' and line[-1] == ')':
                    self.jump_symbols[line[1:-1]] = count
                    continue

                if line[0] == '@':
                    v = line[1:]
                    if not v in self.register_symbols:
                        if v.isnumeric():
                            self.register_symbols[v] = int(v)
                        else:
                            self.register_symbols[v] = self.available_register
                            self.find_next_register()

                instructions.append(line)
                count += 1
        return instructions



if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('path', type=Path, help='Path to assembly program')
    args = parser.parse_args()

    assembler = HackAssembler(args.path)

    exit(0)


    


    