"""
This is a VM translator that converts the intermediate language to HACK assembly. 
To focus on the actuall translation part, I assume that
the assembly file given is perfect and follows the expected convention.
"""
import sys
from pathlib import Path
from typing import Optional, List
from enum import Enum
from textwrap import dedent

def get_output_file_path(asm_file_path: Path) -> Path:
    """
    Just change the input parameter extension from .vm to .asm
    """
    return asm_file_path.with_suffix(".asm")


class MemorySegment (str, Enum):
    CONSTANT = "constant"
    LOCAL = "local"
    ARG = "argument"
    THIS = "this"
    THAT = "that"
    TEMP = "temp"
    POINTER = "pointer"
    STATIC = "static"


class Parser():
    """
    Read .vm file and remove white spaces and comments.
    """
    def __init__(self, vm_fp: Path):
        self.fp = vm_fp
        self.content_array = []
        self.current_command_num = 0
        self.total_command_num = 0

        with open(vm_fp, "r") as file:
            self.content_array = file.readlines()   # this includes newline chars
            self.total_command_num = len(self.content_array)

    def has_more_commands(self) -> bool:
        return True if self.current_command_num < self.total_command_num else False

    def advance(self):
        self.current_command_num += 1

    def get_command(self) -> Optional[List[str]]:
        """
        Given the current command to translate, cleaned-up and broken down into an array. 
        If it's an empty line or a line comment, it returns None.
        """
        current_command = self._trim(self.content_array[self.current_command_num])

        if current_command is None:  
            return None
        else:
            return current_command.lower().split()   # takes care of multiple spaces between words


    def _trim(self, command) -> Optional[str]:
        """Take the raw command and remove white spaces and comments"""
        # remove leading, trailing whilte space chars (space, tab, newline, etc)
        command = command.strip()
        
        # empty line or a comment, ignore
        if command == "" or command[0:2] == "//":   
            return None

        if "//" in command:    # inline comment
            return command.split("//")[0]

        return command
    

class CodeWriter():
    """
    Given VM code, convert it into the equivalent HACK assembly code. 
    """
    def __init__(self, output_fp: Path):
        self.output_file = output_fp
        self.translated_commands = []   # list to store translated asm instructions
        self.unique_label_index = 0 # TODO: I have to increment this somewhere. currently not doing it

    def _write_arithmetic(self, command:str) -> str:
        if command == "add":
            # what to do: pop 2 top-most entries, add and push again
            # current sp - 1 is where the top operand is
            # current sp - 2 is where the bottom operand is
            output = """\
                @SP
                AM = M - 1   // decrement sp, and get the top operand   
                D = M       

                @SP
                AM = M - 1   // decrement sp, and get the bottom operand   
                D = M + D    // add two operands 

                @SP
                M = M + 1   // Increment the SP (ahead of time)
                A = M - 1   // insert the result to where SP used to point at
                M = D"""

        elif command == "sub":
            # what to do: pop 2 top-most entries, sub (bottom - top) and push again
            # current sp - 1 is where the top operand is
            # current sp - 2 is where the bottom operand is
            output = """\
                @SP
                AM = M - 1   // decrement sp, and get the top operand   
                D = M       

                @SP
                AM = M - 1   // decrement sp, and get the bottom operand   
                D = M - D    // bottom - top

                @SP
                M = M + 1   // Increment the SP (ahead of time)
                A = M - 1   // insert the result to where SP used to point at
                M = D"""

        elif command == "neg":
            output = """\
                @SP
                A = M - 1   // don't decrement SP, bc it will be the same in the end
                M = -M"""   

        elif command == "eq":
            # pop two elements
            # compute (x-y) and use JEQ on the result
            # if equal, stack should have -1, if not equal, 0
            output = f"""\
                @SP
                AM = M - 1   // decrement sp, and get the top operand   
                D = M       

                @SP
                AM = M - 1   // decrement sp, and get the bottom operand   
                D = M - D    // bottom - top

                @eq_{self.unique_label_index}
                D; JEQ

                @SP         // 'not equal' portion
                M = M + 1   // Increment the SP (ahead of time)
                A = M - 1   // insert the result to where SP used to point at
                M = 0       // false is 0

                @next_{self.unique_label_index}
                0; JMP

                (eq_{self.unique_label_index})
                @SP         
                M = M + 1   // Increment the SP (ahead of time)
                A = M - 1   // insert the result to where SP used to point at
                M = -1      // true is -1

                (next_{self.unique_label_index}) // so that when not equal, we can skip over (eq_{self.unique_label_index})"""

        elif command == "gt":
            # bottom - top > 0 
            output = f"""\
                @SP
                AM = M - 1   // decrement sp, and get the top operand   
                D = M       

                @SP
                AM = M - 1   // decrement sp, and get the bottom operand   
                D = M - D    // bottom - top

                @gt_{self.unique_label_index}
                D; JGT

                @SP         // 'not greater than' portion
                M = M + 1   // Increment the SP (ahead of time)
                A = M - 1   // insert the result to where SP used to point at
                M = 0       // false is 0

                @next_{self.unique_label_index}
                0; JMP

                (gt_{self.unique_label_index})
                @SP         
                M = M + 1   // Increment the SP (ahead of time)
                A = M - 1   // insert the result to where SP used to point at
                M = -1      // true is -1

                (next_{self.unique_label_index}) // so that when not equal, we can skip over (eq_{self.unique_label_index})"""

        elif command == "lt": 
            # bottom - top < 0 
            output = f"""\
                @SP
                AM = M - 1   // decrement sp, and get the top operand   
                D = M       

                @SP
                AM = M - 1   // decrement sp, and get the bottom operand   
                D = M - D    // bottom - top

                @lt_{self.unique_label_index}
                D; JLT

                @SP         // 'not less than' portion
                M = M + 1   // Increment the SP (ahead of time)
                A = M - 1   // insert the result to where SP used to point at
                M = 0       // false is 0

                @next_{self.unique_label_index}
                0; JMP

                (lt_{self.unique_label_index})
                @SP         
                M = M + 1   // Increment the SP (ahead of time)
                A = M - 1   // insert the result to where SP used to point at
                M = -1      // true is -1

                (next_{self.unique_label_index}) // so that when not equal, we can skip over (eq_{self.unique_label_index})"""

        elif command == "and":
            output = """\
                @SP
                AM = M - 1   // decrement sp, and get the top operand   
                D = M       

                @SP
                AM = M - 1   // decrement sp, and get the bottom operand   
                D = D & M    // AND two operands

                @SP
                M = M + 1   // Increment the SP (ahead of time)
                A = M - 1   // insert the result to where SP used to point at
                M = D"""

        elif command == "or":
            output = """\
                @SP
                AM = M - 1   // decrement sp, and get the top operand   
                D = M       

                @SP
                AM = M - 1   // decrement sp, and get the bottom operand   
                D = D | M    // OR two operands
    
                @SP
                M = M + 1   // Increment the SP (ahead of time)
                A = M - 1   // insert the result to where SP used to point at
                M = D"""

        elif command == "not":
            output = """\
                @SP
                A = M - 1   // don't decrement SP, bc it will be the same in the end
                M = !M"""   

        return output

    def _write_memory_access(self, command:str, segment: str, index: str) -> str:
        output = None
        command = command.lower()
        segment = segment.lower()
        segment_name_to_symbol_mapping = {
            MemorySegment.LOCAL: ("LCL", "M"),
            MemorySegment.ARG: ("ARG", "M"),
            MemorySegment.THIS: ("THIS", "M"),
            MemorySegment.THAT: ("THAT", "M"),
            MemorySegment.TEMP: ("R5", "A"),
            MemorySegment.POINTER: ("THIS", "A"),
            MemorySegment.STATIC: (f"{self.output_file.stem}.{index}", None)
        }
        # pointer segment is mapped on RAM 3-4
        # temp location 5-12
        
        if command == "push":
            if segment == MemorySegment.CONSTANT:
                output = f"""\
                    @{index}
                    D = A

                    @SP
                    A = M
                    M = D   // insert the constant

                    @SP
                    M = M + 1   // increment SP"""
                
            elif segment == MemorySegment.STATIC:
                label_name = segment_name_to_symbol_mapping[segment][0]
                output = f"""\
                    @{label_name}
                    D = M

                    @SP
                    A = M
                    M = D   // insert the constant

                    @SP
                    M = M + 1   // increment SP"""
            
            else:
                base_addr_symbol = segment_name_to_symbol_mapping[segment][0]
                register = segment_name_to_symbol_mapping[segment][1]
                output = f"""\
                    @{index}
                    D = A

                    @{base_addr_symbol}
                    A = D + {register} // compute the base addr + index, aka target addr
                    D = M      // get the target val

                    @SP
                    M = M + 1   // increment SP ahead of time
                    A = M - 1
                    M = D      // place the value where SP was originally pointing at"""

        elif command == "pop":
            # NOTE: constant segment never gets popped, so exclude it
            if segment == MemorySegment.STATIC:
                label_name = segment_name_to_symbol_mapping[segment][0]
                output = f"""\
                    @SP
                    M = M - 1   // decrement the pointer
                    A = M
                    D = M

                    @{label_name}
                    M = D                    
                    """
            else:
                base_addr_symbol = segment_name_to_symbol_mapping[segment][0]
                register = segment_name_to_symbol_mapping[segment][1]
                output = f"""\
                    @{index}
                    D = A

                    @{base_addr_symbol}
                    D =  D + {register}  // compute the target addr

                    @SP
                    M = M - 1 // decrement the pointer
                    // store target addr at 'one above' the top of the stack temporarily (will be overriden anyway)
                    A = M + 1 
                    M = D
                    // get the pop value
                    A = A - 1
                    D = M
                    // go back to where we stored the target addr, pop the value there
                    A = A + 1
                    A = M
                    M = D"""

        return output
    
    def translate(self, command: Optional[List[str]]):
        if command is None:
            return  # no-op
        
        keyword = command[0]

        if keyword in ["add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"]:
            translated_command = self._write_arithmetic(keyword)
        elif keyword in ["push", "pop"]:
            arg1 = command[1]
            arg2 = command[2]
            translated_command = self._write_memory_access(keyword, arg1, arg2)
        else:
            raise NotImplementedError("more to come in the next project")
        
        self.unique_label_index += 1
        self.translated_commands.append(dedent(translated_command) + "\n\n")

    def write(self):
        infinite_loop = """\
            (infinite_loop)
            @infinite_loop
            0; JMP"""
        
        self.translated_commands.append(dedent(infinite_loop))

        with open(self.output_file, "w") as output_file:
            output_file.writelines(self.translated_commands)

if __name__ == "__main__":
    """
    If the input is a single .vm file, the output should be the same name with .hack extension.
    If the input is a directory, each .vm file in the directory should have a Parser but one Codewriter module.
    The output should be one aggregated file called <directory_name>.hack.
    """
    vm_fp = Path(sys.argv[1])
    asm_fp = get_output_file_path(vm_fp)
    files_to_translate = []
    code_writer = CodeWriter(asm_fp)

    if vm_fp.is_dir():
        for child in vm_fp.iterdir():
            if ".vm" in child.name: # only care about .vm files 
                files_to_translate.append(vm_fp)

    else:
        files_to_translate.append(vm_fp)

    for vm_file in files_to_translate:
        parser = Parser(vm_file)

        while parser.has_more_commands():
            command = parser.get_command()
            code_writer.translate(command)
            parser.advance()

    code_writer.write()