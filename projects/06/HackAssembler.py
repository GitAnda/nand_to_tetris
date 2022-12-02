from argparse import ArgumentParser
from pathlib import Path
import re
import json


class HackAssembler():
    def __init__(self, path: Path):
        self.path = path
        
        with open('symbols.json') as f:
            self.symbols = json.load(f)
        self.jump_symbols = dict()
        self.instructions = self.get_instructions(path)
        self.find_symbols()

        with open('comp.json') as f:
            self.comp = json.load(f)
        with open('jump.json') as f:
            self.jump = json.load(f)

    def c_instruction(self, str_instr):
        res = re.split('=|;', str_instr)
        if '=' not in str_instr:
            res.insert(0, 'null')
        if ';' not in str_instr:
            res.append('null')
        
        d, c, j = res
        d, c, j = f"{int('A' in d)}{int('D' in d)}{int('M' in d)}", self.comp[c], self.jump[j]
        return f'111{c}{d}{j}'
    
    def a_instruction(self, str_instr):
        v = str_instr[1:]
        if v.isnumeric():
            code = f'0{int(v):15b}'
        else:
            code = f'0{self.symbols[v]:15b}'
        return code.replace(' ', '0')
    
    def get_machine_code(self):
        machine_code = []
        for instr in self.instructions:
            if instr[0] == '@':
                code = self.a_instruction(instr)
            else:
                code = self.c_instruction(instr)
            machine_code.append(code)
        return machine_code

    def find_next_register(self, address):
        while address in self.symbols.values():
            address += 1
        return address
        
    def get_instructions(self, path):
        instructions = []
        count = 0
        with open(self.path, 'r') as f:
            for line in f.readlines():
                line = line.split('//')[0]
                line = line.strip().replace(' ', '')
                if not line:
                    continue

                if line[0] == '(' and line[-1] == ')':
                    self.jump_symbols[line[1:-1]] = count
                    continue
                
                instructions.append(line)
                count += 1
            
        return instructions
    
    def find_symbols(self):
        next_addr = 16
        for instr in self.instructions:
            if instr[0] == '@':
                
                v = instr[1:]
                if v not in self.symbols and v not in self.jump_symbols:
                    if not v.isnumeric():
                        self.symbols[v] = next_addr
                        next_addr = self.find_next_register(next_addr)
        self.symbols.update(self.jump_symbols)



if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('path', type=Path, help='Path to assembly program')
    args = parser.parse_args()

    assembler = HackAssembler(args.path)
    machine_code = assembler.get_machine_code()
    
    with open(Path(args.path.stem + '.hack'), 'w') as f:
        f.write('\n'.join(machine_code))
        

    exit(0)


    


    