"""
This is an assembler for HACK computer 
To focus on the actuall translation part, I assume that
the assembly file given is perfect and the command input
always follows the expected format.
"""
import sys
from pathlib import Path
from typing import Optional

def get_output_file_path(asm_file_path: Path) -> Path:
    """
    Just change the input parameter extension from .asm to .hack
    """
    return asm_file_path.with_suffix(".hack")


class Parser():
    def __init__(self, asm_fp: Path):
        self.fp = asm_fp
        self.content_array = []
        self.current_command_num = 0
        self.total_command_num = 0

        with open(asm_fp, "r") as file:
            self.content_array = file.readlines()   # this includes newline chars
            self.total_command_num = len(self.content_array)

    def has_more_commands(self) -> bool:
        return True if self.current_command_num < self.total_command_num else False

    def advance(self):
        self.current_command_num += 1
    
    def parse(self) -> Optional[str]:
        """sanitize the instruction (remove white spaces, comments)"""
        curr_instruction = self.content_array[self.current_command_num]

        # remove all whilte space chars (space, tab, newline, etc)
        curr_instruction = "".join(curr_instruction.split())
        
        # empty line or a comment, ignore
        if curr_instruction == "" or curr_instruction[0:2] == "//":   
            return None

        if "//" in curr_instruction:    # inline comment
            return curr_instruction.split("//")[0]

        return curr_instruction


class Decoder():
    comp_mapping = {
        "0": "101010",
        "1": "111111",
        "-1": "111010",
        "D": "001100",
        "A": "110000",
        "M": "110000",
        "!D": "001101",
        "!A": "110001",
        "!M": "110001",
        "-D": "001111",
        "-A": "110011",
        "-M": "110011",
        "D+1": "011111",
        "A+1": "110111",
        "M+1": "110111",
        "D-1": "001110",
        "A-1": "110010",
        "M-1": "110010",
        "D+A": "000010",
        "D+M": "000010",
        "D-A": "010011",
        "D-M": "010011",
        "A-D": "000111",
        "M-D": "000111",
        "D&A": "000000",
        "D&M": "000000",
        "D|A": "010101",
        "D|M": "010101",
    }
    
    dest_mapping = {
        "": "000",
        "M": "001",
        "D": "010",
        "MD": "011",
        "A": "100",
        "AM": "101",
        "AD": "110",
        "AMD": "111"
    }

    jump_mapping = {
        "": "000",
        "JGT": "001",
        "JEQ": "010",
        "JGE": "011",
        "JLT": "100",
        "JNE": "101",
        "JLE": "110",
        "JMP": "111"
    }

    @classmethod
    def _decode_a_instruction(cls, instruction: str) -> str:
        prefix = "0"
        binary_15bits = "{0:015b}".format(int(instruction[1:]))

        return prefix + binary_15bits

    @classmethod
    def _decode_c_instruction(cls, instruction: str) -> str:
        # break down into 3 parts (dest = comp; jump) 
        # remember that dest or jump can be an empty string

        if "=" in instruction:
            dest, comp_and_jump = instruction.split("=")
        else:
            dest = ""
            comp_and_jump = instruction

        if ";" in comp_and_jump:
            comp, jump = comp_and_jump.split(";")
        else:
            comp = comp_and_jump
            jump = ""

        prefix = "111"
        a = "1" if "M" in comp else "0"
        c1_to_c6 = cls.comp_mapping[comp]
        d1_to_d3 = cls.dest_mapping[dest]
        j1_to_j3 = cls.jump_mapping[jump]

        return prefix + a + c1_to_c6 + d1_to_d3 + j1_to_j3

    @classmethod
    def decode(cls, instruction:str) -> Optional[str]:
        if not instruction:
            return None

        if instruction[0] == "@":
            return cls._decode_a_instruction(instruction)

        elif instruction[0] == "(" and instruction[-1] == ")":
            pass
            # this is label
        else:
            return cls._decode_c_instruction(instruction)


class SymbolManager():
    def __init__(self):
        # populate pre-defined symbols
        self.mapping_table = {
            "SP": "0",
            "LCL": "1",
            "ARG": "2",
            "THIS": "3",
            "THAT": "4",
            "SCREEN": "16384",
            "KBD": "24576",
        }




if __name__ == "__main__":
    asm_fp = Path(sys.argv[1])
    hack_fp = get_output_file_path(asm_fp)
    parser = Parser(asm_fp)
    machine_code_array = []

    while parser.has_more_commands():
        asm_code = parser.parse()
        machine_code = Decoder.decode(asm_code)

        print(f"assembly: {asm_code}, machine_code: {machine_code}")
        
        if machine_code:
            machine_code_array.append(machine_code + "\n")
        
        parser.advance()

    with open(hack_fp, "w") as output_file:
        output_file.writelines(machine_code_array)
