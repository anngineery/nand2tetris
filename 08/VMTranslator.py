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

#### -- functions to be used by the orchestrator (main) -- ###
def get_output_file_path(asm_file_path: Path) -> Path:
    """
    If the file path is a directory, then the output file should be <directory_name>.asm.
    If it's a file, then same name with .asm extension
    """
    if asm_file_path.is_dir():
        file_name = asm_file_path.stem + ".asm"
        print(asm_file_path.joinpath(file_name))
        return asm_file_path.joinpath(file_name)

    else:
        print(asm_file_path.with_suffix(".asm"))
        return asm_file_path.with_suffix(".asm")
    
def get_vm_files(vm_file_path: Path) -> List[Path]:
    vm_files = []

    if vm_file_path.is_dir():
        for child in vm_fp.iterdir():
            if ".vm" in child.name:
                vm_files.append(child)
    else:
        vm_files.append(vm_file_path)

    print(vm_files)
    return vm_files
#### ----------------------------------------------------- ###


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
        self.current_vm_file = None

    def set_file_name(self, file_name: str):
        """
        Informs the Code Writer that the tranlsation of has started. Necessary for handling static segments across multiple files.
        Convention is to set static variable to have <file_name>.<index> format.
        """
        self.current_vm_file = file_name

    def add_bootstrap_code(self):
        """
        Bootstrap code = placed in ROM[0~] -> because we designed HACK platform in such a way that
        when it boots up (upon reset) it starts executing from ROM[0]. But we do not handle placing the
        code in ROM, so it only means that this bootstrap code should be generated at the very beginning of the .asm file.
        1. Initialize VM stack
        2. first VM function that starts executing should be Sys.init (argumentless)
        """        
        bootstrap_init = """\
            // initialize pointer registers
            @256
            D = A
            @SP
            M = D
            @LCL
            M = -1
            @ARG
            M = -1
            @THIS
            M = -1
            @THAT
            M = -1"""
        bootstrap_call_sys_init = self._write_function_calling("call", "Sys.init", "0")
        infinite_loop = """\
            (INF_LOOP)
            @INF_LOOP
            0; JMP"""
        
        self.translated_commands.append(bootstrap_init)
        self.translated_commands.append(bootstrap_call_sys_init)
        self.translated_commands.append(infinite_loop)

    def _write_arithmetic(self, command:str) -> str:
        """
        Operands are popped from the stack and the result is pushed to the stack.
        """
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
                D = D + M    // add two operands 

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

                @EQ_{self.unique_label_index}
                D; JEQ

                @SP         // 'not equal' portion
                M = M + 1   // Increment the SP (ahead of time)
                A = M - 1   // insert the result to where SP used to point at
                M = 0       // false is 0

                @NEXT_{self.unique_label_index}
                0; JMP

                (EQ_{self.unique_label_index})
                @SP         
                M = M + 1   // Increment the SP (ahead of time)
                A = M - 1   // insert the result to where SP used to point at
                M = -1      // true is -1

                (NEXT_{self.unique_label_index}) // so that when not equal, we can skip over (EQ_{self.unique_label_index})"""

        elif command == "gt":
            # bottom - top > 0 
            output = f"""\
                @SP
                AM = M - 1   // decrement sp, and get the top operand   
                D = M       

                @SP
                AM = M - 1   // decrement sp, and get the bottom operand   
                D = M - D    // bottom - top

                @GT_{self.unique_label_index}
                D; JGT

                @SP         // 'not greater than' portion
                M = M + 1   // Increment the SP (ahead of time)
                A = M - 1   // insert the result to where SP used to point at
                M = 0       // false is 0

                @NEXT_{self.unique_label_index}
                0; JMP

                (GT_{self.unique_label_index})
                @SP         
                M = M + 1   // Increment the SP (ahead of time)
                A = M - 1   // insert the result to where SP used to point at
                M = -1      // true is -1

                (NEXT_{self.unique_label_index}) // so that when not equal, we can skip over (EQ_{self.unique_label_index})"""

        elif command == "lt": 
            # bottom - top < 0 
            output = f"""\
                @SP
                AM = M - 1   // decrement sp, and get the top operand   
                D = M       

                @SP
                AM = M - 1   // decrement sp, and get the bottom operand   
                D = M - D    // bottom - top

                @LT_{self.unique_label_index}
                D; JLT

                @SP         // 'not less than' portion
                M = M + 1   // Increment the SP (ahead of time)
                A = M - 1   // insert the result to where SP used to point at
                M = 0       // false is 0

                @NEXT_{self.unique_label_index}
                0; JMP

                (LT_{self.unique_label_index})
                @SP         
                M = M + 1   // Increment the SP (ahead of time)
                A = M - 1   // insert the result to where SP used to point at
                M = -1      // true is -1

                (NEXT_{self.unique_label_index}) // so that when not equal, we can skip over (EQ_{self.unique_label_index})"""

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
        """
        local, argument, this and that segments: 
            base addresses are stored in LCL, ARG, THIS and THAT registers respectively 
            (aka those are pointer registers containing memory address).
        pointer, temp segments: 
            mapped directly onto a fixed area in the RAM. 
                pointer = RAM[3-4], temp = RAM[5-12]
        constant segment: 
            it is a 'virtual' segment that doesn't really exist, meaning it doesn't occupy
            any space in the RAM.
        static segment:
            store static variables shared by all functions in the same .vm file.
            takes up RAM[16~255] before the stack starts at RAM[256]. 
            Since the HACK assembler allocates newly encountered variables starting RAM[16], 
            we are gonna leverage this property. For example,
                push static 3 --> @file_name.3 
                                  D = M
        """
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
            MemorySegment.STATIC: (f"{self.current_vm_file.stem}.{index}", None)
        }
        
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
    
    def _write_program_flow(self, command: str, label: str) -> str:
        """
        Handle branching operations required for if-statements and loops.
        """
        label = label.upper()

        if command == "label":
            output = f"""\
                ({label})"""

        elif command == "goto": # unconditional jump
            output = f"""\
                @{label}
                0;JMP"""
            
        elif command == "if-goto":  # conditional jump
            # pop an entry from the stack and use that for evaluation
            # if the value is NOT zero, then go to the label.
            output = f"""\
                @SP
                M = M - 1
                A = M
                D = M

                @{label}
                D;JNE"""

        return output

    def _write_function_calling(self, command: str, func_name: Optional[str]=None, arg_num: Optional[str]=None) -> str:
        """
        Handle a function calling another. 
        """
        func_name = func_name.upper() if func_name else func_name

        if command == "function":
            # mark the function entry and initialize local variables to zero
            output = f"""\
                ({func_name})
                @i
                MD = 0

                ({func_name}$INIT_LCL)
                @{arg_num}
                D = D - A   // D = i - arg_num

                @{func_name}$END_LCL
                D; JGE

                @SP
                M = M + 1   // increment SP ahead of time
                A = M - 1
                M = 0   // init to zero

                @i
                MD = M + 1

                @{func_name}$INIT_LCL
                0; JMP

                ({func_name}$END_LCL)"""
            
        elif command == "call":
            # save the current frame (return address, LCL, ARG, THIS, THAT)
            # adjust ARG and LCL for the callee
            # mark where the return location should be
            # jump to the callee function
            output = f"""\
                @RET_FROM_{func_name}_{self.unique_label_index}
                D = A
                @SP
                M = M + 1   // increment SP ahead of time
                A = M - 1
                M = D   // push return address

                @LCL
                D = M
                @SP
                M = M + 1   // increment SP ahead of time
                A = M - 1
                M = D   // save LCL

                @ARG
                D = M
                @SP
                M = M + 1   // increment SP ahead of time
                A = M - 1
                M = D   // save ARG
                
                @THIS
                D = M
                @SP
                M = M + 1   // increment SP ahead of time
                A = M - 1
                M = D   //save THIS

                @THAT
                D = M
                @SP
                M = M + 1   // increment SP ahead of time
                A = M - 1
                M = D   //save THAT

                @SP
                D = M
                @LCL
                M = D   // LCL = SP
                @ARG
                M = D   // ARG = SP
                @5 
                D = A
                @{arg_num}
                D = D + A   // D = 5 + arg_num
                @ARG
                M = M - D   // ARG = SP - (5 + arg_num)

                @{func_name}
                0; JMP

                (RET_FROM_{func_name}_{self.unique_label_index})"""
            
            self.unique_label_index += 1

        elif command == "return":
            # restore the called function's original environment using the saved frame
            # copy the callee's return value (pushed to the top of the stack) to ARG 0
            # go to the return address saved in the frame
            output = """\
                @LCL
                D = M

                @frame 
                M = D   // frame = LCL
                @5
                D = A
                @frame 
                AM = M - D   // frame = LCL - 5
                D = M
                @return_address
                M = D   // return address need to be saved in a temp variable
                // this is because for argumentless func, memory address that hold
                // return address is the same as where ARG is pointing
                // so when ARG 0 gets overriden with the return value, return address gets wiped out

                @SP
                A = M - 1 
                D = M       // D = pop value
                @ARG
                A = M
                M = D       // *ARG = pop()

                @ARG
                D = M + 1
                @SP
                M = D   // SP = ARG + 1

                @frame 
                AM = M + 1
                D = M   // D = *(frame - 4)
                @LCL
                M = D

                @frame 
                AM = M + 1
                D = M   // D = *(frame - 3)
                @ARG
                M = D

                @frame 
                AM = M + 1
                D = M   // D = *(frame - 2)
                @THIS
                M = D

                @frame 
                AM = M + 1
                D = M   // D = *(frame - 1)
                @THAT
                M = D

                @return_address 
                A = M
                0; JMP"""

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
        elif keyword in ["label", "goto", "if-goto"]:
            arg1 = command[1]
            translated_command = self._write_program_flow(keyword, arg1)
        elif keyword in ["function", "call"]:
            arg1 = command[1]
            arg2 = command[2]
            translated_command = self._write_function_calling(keyword, arg1, arg2)
        elif keyword ==  "return":
            translated_command = self._write_function_calling(keyword)
        else:
            raise NotImplementedError("more to come in the next project")
        
        self.unique_label_index += 1
        self.translated_commands.append(translated_command)

    def write(self):
        with open(self.output_file, "w") as output_file:
            for translated_commands in self.translated_commands:
                output_file.write(dedent(translated_commands + "\n\n"))


if __name__ == "__main__":
    """
    If the input is a single .vm file, the output should be the same name with .hack extension.
    If the input is a directory, each .vm file in the directory should have a Parser but one Codewriter module.
    The output should be one aggregated file called <directory_name>.hack.
    """
    vm_fp = Path(sys.argv[1])
    files_to_translate = get_vm_files(vm_fp)
    asm_fp = get_output_file_path(vm_fp)
    code_writer = CodeWriter(asm_fp)

    # If the given path is a directory, then bootstrap is needed
    if len(files_to_translate) > 1:
        code_writer.add_bootstrap_code()

    for vm_file in files_to_translate:
        parser = Parser(vm_file)
        code_writer.set_file_name(vm_file)

        while parser.has_more_commands():
            command = parser.get_command()
            code_writer.translate(command)
            parser.advance()

    code_writer.write()


