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
    PARAMETER_LIST = "parameterList"
    SUBROUTINE_BODY = "subroutineBody"
    VARIABLE_DECLARATION = "varDec"
    STATEMENTS = "statements"
    LET_STATEMENT = "letStatement"
    IF_STATEMENT = "ifStatement"
    WHILE_STATEMENT = "whileStatement"
    DO_STATEMENT = "doStatement"
    RETURN_STATEMENT = "returnStatement"
    EXPRESSION = "expression"
    EXPRESSION_LIST = "expressionList"
    TERM = "term"



class CompilationEngine:
    def __init__(self, token_stream: List[Tuple[str]], output_stream: List[str]):
       self.input = token_stream
       self.output = output_stream
       self.current_token_index = 0

    def _process_terminal_token(self):
        token, type = self.input[self.current_token_index]
        self.output.append(f"<{type}> {token} </{type}>")
        #print(f"<{type}> {token} </{type}>")
        self.current_token_index += 1

    def _compile_subroutine_call(self):
        # look one token ahead to determine if this subroutine call is a method or not
        if self.input[self.current_token_index + 1] == (".", TokenType.SYMBOL):
            self._process_terminal_token()  # class name or variable name
            self._process_terminal_token()  # "."
        self._process_terminal_token()  # subroutine name
        self._process_terminal_token()  # "("
        self.compile_expression_list()
        self._process_terminal_token()  # ")"

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
        self._process_terminal_token()  # "static" or "field"
        self._process_terminal_token()  # type
        self._process_terminal_token()  # variable name

        # handling optional (0 or more) piece
        while self.input[self.current_token_index] == (",", TokenType.SYMBOL):
            self._process_terminal_token()  # ","
            self._process_terminal_token()  # variable name
        
        self._process_terminal_token()  # ";"
        self.output.append(f"</{ProgramConstructType.CLASS_VAR_DECLARATION}>")
        
    def compile_subroutine(self):
        self.output.append(f"<{ProgramConstructType.SUBROUTINE_DECLARATION}>")
        self._process_terminal_token()  # "constructor", "function" or "method"
        self._process_terminal_token()  # "void" or type
        self._process_terminal_token()  # subroutine name
        self._process_terminal_token()  # "("
        self.compile_parameter_list()
        self._process_terminal_token()  # ")"
        self.compile_subroutine_body()
        self.output.append(f"</{ProgramConstructType.SUBROUTINE_DECLARATION}>")

    def compile_parameter_list(self):
        self.output.append(f"<{ProgramConstructType.PARAMETER_LIST}>")
        token, type = self.input[self.current_token_index]
        # check if there is at least one parameter
        while token in ["int", "char", "boolean"] or type == TokenType.IDENTIFIER:
            self._process_terminal_token()  # type
            self._process_terminal_token()  # variable name

            if self.input[self.current_token_index] == (",", TokenType.SYMBOL):
                self._process_terminal_token()  # ","

            token, type = self.input[self.current_token_index]
        self.output.append(f"</{ProgramConstructType.PARAMETER_LIST}>")

    def compile_subroutine_body(self):
        self.output.append(f"<{ProgramConstructType.SUBROUTINE_BODY}>")
        self._process_terminal_token()  # "{"
        # 0 or more variable declaration
        while self.input[self.current_token_index] == ("var", TokenType.KEYWORD): 
            self.compile_var_declaration()  
        self.compile_statements()
        self._process_terminal_token()  # "}"
        self.output.append(f"</{ProgramConstructType.SUBROUTINE_BODY}>")

    def compile_var_declaration(self):
        self.output.append(f"<{ProgramConstructType.VARIABLE_DECLARATION}>")
        self._process_terminal_token()  # "var"
        self._process_terminal_token()  # type
        self._process_terminal_token()  # variable name

        # handling optional (0 or more) piece
        while self.input[self.current_token_index] == (",", TokenType.SYMBOL):
            self._process_terminal_token()  # ","
            self._process_terminal_token()  # variable name
        
        self._process_terminal_token()  # ";"
        self.output.append(f"</{ProgramConstructType.VARIABLE_DECLARATION}>")

    def compile_statements(self):
        self.output.append(f"<{ProgramConstructType.STATEMENTS}>")
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

        self.output.append(f"</{ProgramConstructType.STATEMENTS}>")

    def compile_do(self):
        self.output.append(f"<{ProgramConstructType.DO_STATEMENT}>")
        self._process_terminal_token()  # "do"
        self._compile_subroutine_call()
        self._process_terminal_token()  # ";"
        self.output.append(f"</{ProgramConstructType.DO_STATEMENT}>")

    def compile_let(self):
        self.output.append(f"<{ProgramConstructType.LET_STATEMENT}>")
        self._process_terminal_token()  # "let"
        self._process_terminal_token()  # variable name
        # handling optional (0 or 1) pieces
        if self.input[self.current_token_index] == ("[", TokenType.SYMBOL):
            self._process_terminal_token()  # "["
            self.compile_expression()
            self._process_terminal_token()  # "]"
        self._process_terminal_token()  # "="
        self.compile_expression()
        self._process_terminal_token()  # ";"
        self.output.append(f"</{ProgramConstructType.LET_STATEMENT}>")

    def compile_while(self):
        self.output.append(f"<{ProgramConstructType.WHILE_STATEMENT}>")
        self._process_terminal_token()  # "while"
        self._process_terminal_token()  # "("
        self.compile_expression()
        self._process_terminal_token()  # ")"
        self._process_terminal_token()  # "{"
        self.compile_statements()
        self._process_terminal_token()  # "}"
        self.output.append(f"</{ProgramConstructType.WHILE_STATEMENT}>")

    def compile_return(self):
        self.output.append(f"<{ProgramConstructType.RETURN_STATEMENT}>")
        self._process_terminal_token()  # "return"
        # 0 or 1 expression can follow after the "return" keyword
        if self.input[self.current_token_index] != (";", TokenType.SYMBOL):
            self.compile_expression()
        self._process_terminal_token()  # ";"
        self.output.append(f"</{ProgramConstructType.RETURN_STATEMENT}>")

    def compile_if(self):
        self.output.append(f"<{ProgramConstructType.IF_STATEMENT}>")
        self._process_terminal_token()  # "if"
        self._process_terminal_token()  # "("
        self.compile_expression()
        self._process_terminal_token()  # ")"
        self._process_terminal_token()  # "{"
        self.compile_statements()
        self._process_terminal_token()  # "}"
        if self.input[self.current_token_index] == ("else", TokenType.KEYWORD):
            self._process_terminal_token()  # "else"
            self._process_terminal_token()  # "{"
            self.compile_statements()
            self._process_terminal_token()  # "}"
        self.output.append(f"</{ProgramConstructType.IF_STATEMENT}>")

    def compile_expression(self):
        self.output.append(f"<{ProgramConstructType.EXPRESSION}>")
        self.compile_term()
        token, type = self.input[self.current_token_index]
        while token in ["+", "-", "*", "/", "&", "|", "<", ">", "="] and type == TokenType.SYMBOL:
            self._process_terminal_token()  # operator
            self.compile_term()
            token, type = self.input[self.current_token_index]
        self.output.append(f"</{ProgramConstructType.EXPRESSION}>")

    def compile_term(self):
        self.output.append(f"<{ProgramConstructType.TERM}>")
        token, type = self.input[self.current_token_index]
        if type == TokenType.INT_CONST:
            self._process_terminal_token() 
        elif type == TokenType.STR_CONST:
            self._process_terminal_token() 
        elif type == TokenType.KEYWORD and token in ["true", "false", "null", "this"]:
            self._process_terminal_token() 
        elif type == TokenType.SYMBOL:
            if token in ["-", "~"]:
                self._process_terminal_token() 
                self.compile_term()
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
                self._process_terminal_token() 

                if self.input[self.current_token_index] == ("[", TokenType.SYMBOL):
                    self._process_terminal_token()  # "["
                    self.compile_expression()
                    self._process_terminal_token()  # "]"
        else:
            raise ValueError(f"{token} is not a valid term")
        self.output.append(f"</{ProgramConstructType.TERM}>")

    def compile_expression_list(self):
        self.output.append(f"<{ProgramConstructType.EXPRESSION_LIST}>")
        while self.input[self.current_token_index] != (")", TokenType.SYMBOL):
            self.compile_expression()
            if self.input[self.current_token_index] == (",", TokenType.SYMBOL):
                self._process_terminal_token()
        self.output.append(f"</{ProgramConstructType.EXPRESSION_LIST}>")