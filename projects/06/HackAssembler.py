from argparse import ArgumentParser
from pathlib import Path
import re


class HackAssembler():
    def __init__(self, path: Path):
        self.path = path

        self.register_symbols = {f'R{i}': i for i in range(16)}
        self.available_register = 16
        self.jump_symbols = dict()
        self.instructions = self.set_instructions()

        with open('comp') as f:
            self.lookup_comp = {}
            for line in f.readlines():
                s, b = line.strip().split(' ')
                self.lookup_comp[s] = b
        with open('jump') as f:
            self.lookup_jump = {}
            for line in f.readlines():
                s, b = line.strip().split(' ')
                self.lookup_jump[s] = b

        self.machine_code = self.get_machine_code()

    @staticmethod
    def split_c_instruction(str_instruction):
        res = re.split('=|;', str_instruction)
        if '=' not in str_instruction:
            res.insert(0, 'null')
        if ';' not in str_instruction:
            res.append('null')
        return res
    
    def get_machine_code(self):
        code = []
        for instruction in self.instructions:
            if instruction[0] == '@':
                v = self.register_symbols[instruction[1:]]
                machine_code = f'0{v:15x}'.replace(' ', '0')

            else:
                d, c, j = self.split_c_instruction(instruction)
                c = self.lookup_comp[c]
                d = f"{int('A' in d)}{int('D' in d)}{int('M' in d)}"
                j = self.lookup_jump[j]
                machine_code = f'111{c}{d}{j}'
                print(instruction, machine_code)
            code.append(machine_code)
        return code

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

    # for s, b in zip(assembler.instructions, assembler.machine_code):
    #     print(f"{s}, {b}")

    exit(0)


    


    