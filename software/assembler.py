"""
This is an assembler for HACK computer. 
To focus on the actual translation part, I assume that
the assembly file given is perfect and follows the expected convention.
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
    """
    Read .asm file and remove white spaces and comments.
    """
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
    """
    Given a line of assembly code, convert it into the equivalent machine code. 
    """
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

    def __init__(self):
        self.symbol_manager = SymbolManager()
        self.next_instruction_index = 0

    def _decode_a_instruction(self, instruction: str) -> str:
        """
        A instruction format: c@positive_integer or @variable_name
        By convention, variable names cannot start with a digit.
        """
        prefix = "0"

        try:
            binary_15bits = "{0:015b}".format(int(instruction[1:]))
        
        except ValueError: # what comes after "@" is a char not a digit
            #import pdb; pdb.set_trace()
            address = self.symbol_manager.get_address(instruction[1:])

            if address is None:
                # variable appeared for the first time , so we need to add to the symbol table
                address = self.symbol_manager.add_entry(instruction[1:])
            binary_15bits = "{0:015b}".format(address)

        return prefix + binary_15bits

    def _decode_c_instruction(self, instruction: str) -> str:
        """
        C instruction format: dest (optional) = comp; jump (optional)
        """
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
        c1_to_c6 = self.comp_mapping[comp]
        d1_to_d3 = self.dest_mapping[dest]
        j1_to_j3 = self.jump_mapping[jump]

        return prefix + a + c1_to_c6 + d1_to_d3 + j1_to_j3

    def decode(self, instruction:str) -> Optional[str]:
        """
        A function that decodes an A or C instruction into a machine code.
        """
        if instruction and instruction[0] == "@":
            decoded_instruction = self._decode_a_instruction(instruction)

        elif instruction and ("=" in instruction or ";" in instruction):
            decoded_instruction = self._decode_c_instruction(instruction)
        
        else: 
            decoded_instruction = None

        return decoded_instruction
    
    def scan(self, instruction: str):
        """
        A function used for scanning the code and getting right addresses for labels.
        Does not actually generate machine code. Labels are pseudo commands
        """
        if instruction and instruction[0] == "(" and instruction[-1] == ")":
            self.symbol_manager.add_entry(instruction[1:-1], self.next_instruction_index)
        elif instruction:
            self.next_instruction_index += 1


class SymbolManager():
    "Manages symbol tables for pre-defined and user-defined symbols"
    def __init__(self):
        self.next_available_address = 16 # for variables
        # populate pre-defined symbols
        self.mapping_table = {
            "SP": 0,
            "LCL": 1,
            "ARG": 2,
            "THIS": 3,
            "THAT": 4,
            "SCREEN": 16384,
            "KBD": 24576,
        }
        
        # add virtual registers R0-R15
        for i in range(0, 16):
            self.mapping_table["R"+ str(i)] = i

    def add_entry(self, key: str, value: Optional[int] = None) -> int:
        if not value:
            value = self.next_available_address
            self.next_available_address += 1
        
        self.mapping_table[key] = value

        return value
    
    def get_address(self, key: str) -> int:
        return self.mapping_table.get(key)


if __name__ == "__main__":
    """
    First, extract instructions from .asm file using Parser.
    Second, go through the sanitized instructions and look for labels only. 
    Labels take precedence over variables. There could be an A instruction such as `@blahblah` and `blahblah` is not a variable name but label name.
    Third, now that we know how to match a label to the correct address, translate the instructions.
    """
    asm_fp = Path(sys.argv[1])
    hack_fp = get_output_file_path(asm_fp)
    parser = Parser(asm_fp)
    decoder = Decoder()
    parsed_code_array = []
    machine_code_array = []

    # Get a complete sanitized assembly code
    while parser.has_more_commands():
        asm_code = parser.parse()
        parsed_code_array.append(asm_code)
        parser.advance()

    # First pass - getting all the label addresses
    for parsed_instruction in parsed_code_array:
        decoder.scan(parsed_instruction)

    # second pass, now that labels are all filled out, actually translate
    for parsed_instruction in parsed_code_array:
        machine_code = decoder.decode(parsed_instruction)

        print(f"assembly: {parsed_instruction}, machine_code: {machine_code}")
        
        if machine_code:
            machine_code_array.append(machine_code + "\n")
        
    print(decoder.symbol_manager.mapping_table)

    with open(hack_fp, "w") as output_file:
        output_file.writelines(machine_code_array)
