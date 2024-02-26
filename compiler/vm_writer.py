from pathlib import Path
from enum import Enum


class MemorySegment (str, Enum):
    CONSTANT = "constant"
    LOCAL = "local"
    ARG = "argument"
    THIS = "this"
    THAT = "that"
    TEMP = "temp"
    POINTER = "pointer"
    STATIC = "static"


class ArithmeticCommand(str, Enum):
    ADD = "add"
    SUB = "sub"
    NEG = "neg"
    EQ = "eq"
    GT = "gt"
    LT = "lt"
    AND = "and"
    OR = "or"
    NOT = "not"


class VMWriter:
    """
    Write VM commands into a file.
    """
    def __init__(self, file_name: Path):
        self.fp = open(file_name, "w")

    def write_push(self, segment: MemorySegment, index: int):
        self.fp.write(f"push {segment} {index}\n")

    def write_pop(self, segment: MemorySegment, index: int):
        self.fp.write(f"pop {segment} {index}\n")

    def write_arithmetic(self, command: ArithmeticCommand):
        self.fp.write(f"{command}\n")

    def write_label(self, label: str):
        pass

    def write_goto(self, label: str):
        pass

    def write_if_goto(self, label: str):
        pass

    def write_call(self, name: str, num_args: int):
        pass

    def write_function(self, name: str, num_locals: int):
        pass

    def write_return(self):
        pass

    def close(self):
        self.fp.close()