"""
Use recursive descent parsing to check a stream of valid tokens against Jack language grammar.
"""
from typing import List, Tuple
from enum import Enum
from tokenizer import TokenType


class ProgramConstructType(str, Enum):
    CLASS = "class"
    CLASS_VAR_DECLARATION = "classVarDec"
    SUBROUTINE_DECLARATION = "subroutineDec"
    # TODO: more to be added


class CompilationEngine:
    def __init__(self, token_stream: List[Tuple[str]], output_stream: List[str]):
       self.input = token_stream
       self.output = output_stream
       self.current_token_index = 0

       self.compile_class()

    def _process_terminal_token(self):
        token, type = self.input[self.current_token_index]
        self.output.append(f"<{type}>{token}</{type}>")
        self.current_token_index += 1

    def compile_class(self):
        self.output.append(f"<{ProgramConstructType.CLASS}>")
        self._process_terminal_token()  # "class"
        self._process_terminal_token()  # class_name
        self._process_terminal_token()  # "{"

        # handling 0 or more class variable declaration or subroutine declaration
        while self.input[self.current_token_index] != ("}", TokenType.SYMBOL):
            token, _ = self.input[self.current_token_index]
            if token in ["static", "field"]:
                self.compile_class_var_declaration()
            elif token in ["constructor", "function", "method"]:
                self.compile_subroutine()

        self._process_terminal_token()  # "}"
        self.output.append(f"</{ProgramConstructType.CLASS}>")

    def compile_class_var_declaration(self):
        self.output.append(f"<{ProgramConstructType.CLASS_VAR_DECLARATION}>")
        self._process_terminal_token()  # static or field
        self._process_terminal_token()  # type
        self._process_terminal_token()  # variable name

        # handling optional (0 or more) piece
        while self.input[self.current_token_index] == (",", TokenType.SYMBOL):
            self._process_terminal_token()  # ","
            self._process_terminal_token()  # variable name
        
        self._process_terminal_token()  # ";"
        self.output.append(f"</{ProgramConstructType.CLASS_VAR_DECLARATION}>")
        
    def compile_subroutine():
        pass

    def compile_parameter_list():
        pass

    def compile_var_declaration():
        pass

    def compile_statements():
        pass

    def compile_do():
        pass

    def compile_let():
        pass

    def compile_while():
        pass

    def compile_return():
        pass

    def compile_if():
        pass

    def compile_expression():
        pass

    def compile_term():
        pass

    def compile_expression_list():
        pass


# if it's a terminal, then just use the given type and the value itself and make the marked-up output
    