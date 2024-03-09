from enum import Enum
from pathlib import Path
import sys, re
from typing import Tuple


class TokenType(str, Enum):
    KEYWORD = "keyword"
    SYMBOL = "symbol"
    IDENTIFIER = "identifier"
    INT_CONST = "integerConstant"
    STR_CONST = "stringConstant"


class Tokenizer:
    """
    Break down a given input into a stream of tokens (removes white spaces and comments) 
    and classify them into one of 5 lexical categories.
    I intentionally avoided using shlex, a built-in library for writing lexical analyzer.
    """
    keyword_list = ["CLASS", "METHOD", "FUNCTION", "CONSTRUCTOR", "INT", "BOOLEAN", "CHAR", "VOID", "VAR", "STATIC", "FIELD", "LET", "DO", "IF", "ELSE", "WHILE", "RETURN", "TRUE", "FALSE", "NULL", "THIS"]
    symbol_list = ["(", ")", "{", "}", "[", "]", ".", ",", ";", "+", "-", "*", "/", "&", "|", "<", ">", "=", "~"]
    int_const_range = (0, 32767)
    string_literal_pattern = r'(\"[^\"]+\")'

    def __init__(self, fp: Path):
        self.fp = fp
        self.current_token_index = None
        self.total_token_num = 0
        self.token_array = []
        self.block_comment_start = False

        with open(fp, "r") as file:
            current_line = file.readline()

            while current_line != "":     # if it's empty string, it's EOF
                current_line = current_line.strip()    # strip leading and trailing spaces including \n
                current_line_tokens = []

                # handling multi-line comments
                if current_line.startswith(("/**", "/*")) ^ current_line.endswith("*/"):
                    self.block_comment_start = not self.block_comment_start
                    
                # ignore an empty line or a full comment (// or /** text */ or /* text */)
                # or while we are processing multi-line comments
                elif current_line != "" and not current_line.startswith("//") and \
                    not (current_line.startswith(("/**", "/*")) and current_line.endswith("*/")) and \
                        not self.block_comment_start:
                    current_line = current_line.split("//")[0]  # get rid of inline comment if there is one
                    # first filter out string literals, because that supersedes other symbols
                    quote_deliminated = re.split(Tokenizer.string_literal_pattern, current_line)

                    # now we deal with spaces, double quotes and stuff
                    for qd in quote_deliminated:
                        if re.match(Tokenizer.string_literal_pattern, qd):
                            current_line_tokens.append(qd)
     
                        else:   # split at every space and symbol
                            current_line_tokens.extend(re.split(r"([\s\(\)\{\}\[\]\.\,\+\-\*\|;/&<>=~])", qd))

                    for token in current_line_tokens:
                        token = token.strip()   # this is necessary as re.split result has random empty strings, spaces, etc
                        if token != "":
                            self.token_array.append(token)
                            self.total_token_num += 1

                current_line = file.readline()

        self.current_token_index = 0

    def has_more_tokens(self) -> bool:
        return True if self.current_token_index < self.total_token_num else False

    def advance(self):
        self.current_token_index += 1

    def get_token_and_type(self) -> Tuple[str, TokenType]:
        current_token = self.token_array[self.current_token_index]

        if re.match(Tokenizer.string_literal_pattern, current_token):
            return current_token[1:-1], TokenType.STR_CONST
        elif current_token.upper() in Tokenizer.keyword_list:
            return current_token, TokenType.KEYWORD
        elif current_token in Tokenizer.symbol_list:
            return current_token, TokenType.SYMBOL
        elif current_token.isdigit() and self.int_const_range[0] <= int(current_token) <= self.int_const_range[1]:
            return current_token, TokenType.INT_CONST
        else: 
            return current_token, TokenType.IDENTIFIER
        

if __name__ == "__main__":
    """
    Tokenizer test program. It generates an output xml, 
    which later can be compared against the expected output using TextComparer tool.

    How to run: python3 tokenizer.py <name of a jack file>
    """
    fp = Path(sys.argv[1])

    output_file_name = fp.with_suffix(".xml")
    tokenizer = Tokenizer(fp) # is it the full path?
    with open(output_file_name, "w") as output_file:
        output_file.write("<tokens>" + "\n")

        while tokenizer.has_more_tokens():
            token, type = tokenizer.get_token_and_type()
            # convert some symbols used by XMLs to display properly
            if token == "<":
                token = "&lt;"
            elif token == ">":
                token = "&gt;"
            elif token == "\"":
                token = "&quot;"
            elif token == "&":
                token = "&amp;"
            output_file.write(f"<{type}>{token}</{type}>" + "\n")
            tokenizer.advance()

        output_file.write("</tokens>" + "\n")
