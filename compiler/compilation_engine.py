"""
Use recursive descent parsing to check a stream of valid tokens against Jack language grammar.
"""
from typing import List, Tuple
from enum import Enum
from tokenizer import TokenType
from symbol_table import SymbolTable, Category
from vm_writer import VMWriter, MemorySegment, ArithmeticCommand
from pathlib import Path
from uuid import uuid4


category_to_memory_segment_mapping = {
    Category.ARGUMENT: MemorySegment.ARG,
    Category.FIELD: MemorySegment.THIS, # TODO: set Pointer 0 (This) first and then...
    Category.STATIC: MemorySegment.STATIC,
    Category.VARIALBE: MemorySegment.LOCAL,
}


class CompilationEngine:
    def __init__(self, token_stream: List[Tuple[str]], output_file_path: Path):
       self.input = token_stream
       self.current_token_index = 0
       self.symbol_table = SymbolTable()
       self.current_class_name = None
       self.current_subroutine_name = None
       self.vm_writer = VMWriter(output_file_path)

    def _process_terminal_token(self) -> str:
        token, type = self.input[self.current_token_index]
        self.current_token_index += 1

        return token

    def _compile_subroutine_call(self):
        # look one token ahead to determine if this subroutine call is a method or not
        name = None

        if self.input[self.current_token_index + 1] == (".", TokenType.SYMBOL):
            name = self._process_terminal_token()  # class name or variable name
            self._process_terminal_token()  # "."
        subroutine_name = self._process_terminal_token()  # subroutine name
        self._process_terminal_token()  # "("
        num_args = self.compile_expression_list()
        self._process_terminal_token()  # ")"

        self.vm_writer.write_call(
            f"{name or self.current_class_name}.{subroutine_name}", num_args   # TODO: revisit this later
        )

    def compile_class(self):
        self._process_terminal_token()  # "class"
        self.current_class_name = self._process_terminal_token()  # class_name
        self._process_terminal_token()  # "{"

        # handling 0 or more class variable declaration or subroutine declaration
        while self.input[self.current_token_index] != ("}", TokenType.SYMBOL):
            token, _ = self.input[self.current_token_index]
            if token in ["static", "field"]:
                self.compile_class_var_declaration()
            elif token in ["constructor", "function", "method"]:
                self.compile_subroutine()

        self._process_terminal_token()  # "}"
        self.vm_writer.close()

        # FOR DEBUGGING
        self.symbol_table.print()

    def compile_class_var_declaration(self):
        category, data_type, name = None, None, None

        category = self._process_terminal_token()  # "static" or "field"
        data_type = self._process_terminal_token()  # type
        name = self._process_terminal_token()  # variable name
        self.symbol_table.define(name, data_type, Category(category))

        # handling optional (0 or more) piece
        while self.input[self.current_token_index] == (",", TokenType.SYMBOL):
            self._process_terminal_token()  # ","
            name = self._process_terminal_token()  # variable name
            self.symbol_table.define(name, data_type, Category(category))
        
        self._process_terminal_token()  # ";"
        
    def compile_subroutine(self):
        self.symbol_table.start_subroutine()
        subroutine_type = self._process_terminal_token()  # "constructor", "function" or "method"
        self._process_terminal_token()  # "void" or type
        self.current_subroutine_name = self._process_terminal_token()  # subroutine name
        self._process_terminal_token()  # "("
        if subroutine_type in ["constructor", "method"]:
            # always the object itself is passed as the first argument implicitly
            self.symbol_table.define("this", self.current_class_name, Category.ARGUMENT)
        self.compile_parameter_list()   # this fills up the subroutine symbol table with args
        self._process_terminal_token()  # ")"
        self.compile_subroutine_body()

    def compile_parameter_list(self):
        token, type = self.input[self.current_token_index]
        # check if there is at least one parameter
        while token in ["int", "char", "boolean"] or type == TokenType.IDENTIFIER:
            data_type = self._process_terminal_token()  # type
            name = self._process_terminal_token()  # variable name
            self.symbol_table.define(name, data_type, Category.ARGUMENT)

            if self.input[self.current_token_index] == (",", TokenType.SYMBOL):
                self._process_terminal_token()  # ","

            token, type = self.input[self.current_token_index]

    def compile_subroutine_body(self):
        self._process_terminal_token()  # "{"
        # 0 or more variable declaration
        while self.input[self.current_token_index] == ("var", TokenType.KEYWORD): 
            self.compile_var_declaration()  # this fills up the subroutine symbol table with vars (locals)
    
        num_locals = self.symbol_table.count_variables(Category.VARIALBE)
        self.vm_writer.write_function(
            f"{self.current_class_name}.{self.current_subroutine_name}", num_locals
        )

        self.compile_statements()
        self._process_terminal_token()  # "}"

    def compile_var_declaration(self):
        category = self._process_terminal_token()  # "var"
        data_type = self._process_terminal_token()  # type
        name = self._process_terminal_token()  # variable name
        self.symbol_table.define(name, data_type, Category(category))

        # handling optional (0 or more) piece
        while self.input[self.current_token_index] == (",", TokenType.SYMBOL):
            self._process_terminal_token()  # ","
            name = self._process_terminal_token()  # variable name
            self.symbol_table.define(name, data_type, Category(category))
        
        self._process_terminal_token()  # ";"

    def compile_statements(self):
        token, type = self.input[self.current_token_index]

        # handle 0 or more various types of statements
        while type == TokenType.KEYWORD and token in ["let", "if", "while", "do", "return"]:
            if token == "let":
                self.compile_let()
            elif token == "if":
                self.compile_if()
            elif token == "while":
                self.compile_while()
            elif token == "do":
                self.compile_do()
            elif token == "return":
                self.compile_return()

            token, type = self.input[self.current_token_index]

    def compile_do(self):
        self._process_terminal_token()  # "do"
        self._compile_subroutine_call()
        self._process_terminal_token()  # ";"

    def compile_let(self):
        self._process_terminal_token()  # "let"
        var_name = self._process_terminal_token()  # variable name
        # handling optional (0 or 1) pieces for an array
        if self.input[self.current_token_index] == ("[", TokenType.SYMBOL):
            self._process_terminal_token()  # "["
            self.compile_expression()   # this should result in the index?
            self._process_terminal_token()  # "]"
        self._process_terminal_token()  # "="
        self.compile_expression()   # the result is at the top of the stack now
        self._process_terminal_token()  # ";"

        category = self.symbol_table.which_category(var_name)
        index = self.symbol_table.which_index(var_name)
        self.vm_writer.write_pop(category_to_memory_segment_mapping[category], index)

    def compile_while(self):
        unique_id = uuid4()
        while_begin_label = f"while-begin-{unique_id}"
        while_completed_label = f"while-completed-{unique_id}"

        self.vm_writer.write_label(while_begin_label)

        self._process_terminal_token()  # "while"
        self._process_terminal_token()  # "("

        self.compile_expression()   # the result of expression should be at the top
        self.vm_writer.write_arithmetic(ArithmeticCommand.NOT)  # !(expression)
        # if !(expression) = -1, then (expression) = 0 -> should exit the loop
        self.vm_writer.write_if_goto(while_completed_label)

        self._process_terminal_token()  # ")"
        self._process_terminal_token()  # "{"

        # when while condition is met 
        self.compile_statements()
        self.vm_writer.write_goto(while_begin_label)    # should go back to the beginning of while

        self._process_terminal_token()  # "}"

        self.vm_writer.write_label(while_completed_label)

    def compile_return(self):
        self._process_terminal_token()  # "return"
        # 0 or 1 expression can follow after the "return" keyword
        if self.input[self.current_token_index] != (";", TokenType.SYMBOL):
            self.compile_expression()
        self._process_terminal_token()  # ";"
        self.vm_writer.write_return()

    def compile_if(self):
        unique_id = uuid4()
        if_true_label_name = f"if-true-{unique_id}"
        if_false_label_name = f"if-false-{unique_id}"
        if_completed_label_name = f"if-completed-{unique_id}"

        self._process_terminal_token()  # "if"
        self._process_terminal_token()  # "("

        self.compile_expression()   # the result of expression should be at the top of the stack
        self.vm_writer.write_arithmetic(ArithmeticCommand.NOT)  # this gives !(expression)
        # if !(expression) = -1, it means (expression) = 0, so we need to hit the else statement
        self.vm_writer.write_if_goto(if_false_label_name)   

        self._process_terminal_token()  # ")"
        self._process_terminal_token()  # "{"

        # when if was true, we will be here
        self.vm_writer.write_label(if_true_label_name)
        self.compile_statements()
        self.vm_writer.write_goto(if_completed_label_name)  # to ensure we don't hit the else statement

        self._process_terminal_token()  # "}"

        if self.input[self.current_token_index] == ("else", TokenType.KEYWORD):
            self._process_terminal_token()  # "else"
            self._process_terminal_token()  # "{"

            # when if was false, we will be here
            self.vm_writer.write_label(if_false_label_name)
            self.compile_statements()

            self._process_terminal_token()  # "}"

        self.vm_writer.write_label(if_completed_label_name)

    def compile_expression(self):
        self.compile_term()
        token, type = self.input[self.current_token_index]
        while token in ["+", "-", "*", "/", "&", "|", "<", ">", "="] and type == TokenType.SYMBOL:
            self._process_terminal_token()  # operator
            self.compile_term()

            if token == "*":
                self.vm_writer.write_call("Math.multiply", 2)
            elif token == "/":
                self.vm_writer.write_call("Math.divide", 2)
            else:
                mapping = {
                    "+": ArithmeticCommand.ADD,
                    "-": ArithmeticCommand.SUB,
                    "&": ArithmeticCommand.AND,
                    "|": ArithmeticCommand.OR,
                    "<": ArithmeticCommand.LT,
                    ">": ArithmeticCommand.GT,
                    "=": ArithmeticCommand.EQ,
                }
                self.vm_writer.write_arithmetic(mapping[token])
            
            token, type = self.input[self.current_token_index]

    def compile_term(self):
        token, type = self.input[self.current_token_index]
        if type == TokenType.INT_CONST:
            int_value = self._process_terminal_token() 
            self.vm_writer.write_push(MemorySegment.CONSTANT, int_value)

        elif type == TokenType.STR_CONST:
            self._process_terminal_token() 
            # TODO: is string treated like an array of chars?
        
        elif type == TokenType.KEYWORD and token in ["true", "false", "null", "this"]:
            keyword = self._process_terminal_token() 

            if keyword == "true":
                self.vm_writer.write_push(MemorySegment.CONSTANT, 1)
                self.vm_writer.write_arithmetic(ArithmeticCommand.NEG)  # we constant "segment" does not have negative numbers
            elif keyword in ["false", "null"]:
                self.vm_writer.write_push(MemorySegment.CONSTANT, 0)
            else:
                self.vm_writer.write_push(MemorySegment.ARG, 0)
        
        elif type == TokenType.SYMBOL:
            if token in ["-", "~"]:
                self._process_terminal_token() 
                self.compile_term()

                if token == "-":
                    self.vm_writer.write_arithmetic(ArithmeticCommand.NEG)
                else:
                    self.vm_writer.write_arithmetic(ArithmeticCommand.NOT)
            
            elif token == "(":
                self._process_terminal_token()  #"("
                self.compile_expression()
                self._process_terminal_token()  #")"
            
            else:
                raise ValueError(f"{token} is not a valid term")
        
        elif type == TokenType.IDENTIFIER:
            lookahead_token, lookahead_type = self.input[self.current_token_index + 1] 
            if lookahead_type == TokenType.SYMBOL and lookahead_token in ["(", "."]:
                self._compile_subroutine_call()

            else:   # just variable or variable array
                var_name = self._process_terminal_token() 
                category = self.symbol_table.which_category(var_name)
                index = self.symbol_table.which_index(var_name)
                self.vm_writer.write_push(category_to_memory_segment_mapping[category], index)

                if self.input[self.current_token_index] == ("[", TokenType.SYMBOL):
                    self._process_terminal_token()  # "["
                    self.compile_expression()
                    self._process_terminal_token()  # "]"
        
        else:
            raise ValueError(f"{token} is not a valid term")

    def compile_expression_list(self) -> int:
        num_args = 0

        while self.input[self.current_token_index] != (")", TokenType.SYMBOL):
            self.compile_expression()
            num_args += 1
            if self.input[self.current_token_index] == (",", TokenType.SYMBOL):
                self._process_terminal_token()

        return num_args