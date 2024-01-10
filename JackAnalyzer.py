"""
Jack syntax analyzer that converts the high-level Jack language into the intermediate VM language.
It does not handle error reporting as it assumes all input conforms to Jack language grammar perfectly.
"""
from enum import Enum
from pathlib import Path
import sys, re
from typing import List, Tuple


def get_input_files(path: Path) -> List[Path]:
    files = []

    if path.is_dir():
        for child in path.iterdir():
            if ".jack" in child.name:
                files.append(child)
    else:
        files.append(path)

    return files


class TokenType(str, Enum):
    KEYWORD = "KEYWORD"
    SYMBOL = "SYMBOL"
    IDENTIFIER = "IDENTIFIER"
    INT_CONST = "INT_CONST"
    STR_CONST = "STR_CONST"

class Tokenizer:
    """
    Break down a given input into a stream of tokens (removes white spaces and comments) 
    and classify them into one of 5 lexical categories.
    """
    keyword_list = ["CLASS", "METHOD", "FUNCTION", "CONSTRUCTOR", "INT", "BOOLEAN", "CHAR", "VOID", "VAR", "STATIC", "FIELD", "LET", "DO", "IF", "ELSE", "WHILE", "RETURN", "TRUE", "FALSE", "NULL", "THIS"]
    symbol_list = ["(", ")", "{", "}", "[", "]", ".", ",", ";", "+", "-", "*", "/", "|", "<", ">", "=", "~"]
    int_const_range = (0, 32767)

    def __init__(self, fp: Path):
        self.fp = fp
        self.current_token_index = None
        self.total_token_num = 0
        self.token_array = []
        self.quote_open = False

        with open(fp, "r") as file:
            current_line = file.readline()

            while current_line != "":     # if it's empty string, it's EOF
                current_line = current_line.strip()    # strip leading and trailing spaces including \n
                # ignore an empty line or an comment (// or /** text */ or /* text */)
                if not (current_line == "" or current_line.startswith("//") or re.match(r"/\*\*[\s\S]*\*/|/\*[\s\S]*\*", current_line) != None):
                    current_line = current_line.split("//")[0]  # get rid of inline comment if there is one
                    # split at every symbols + whitespace (splitting at whitespace separate keywords out) + double quote
                    tokens = re.split(r"([\"\s\(\)\{\}\[\]\.\,\+\-\*\|;/&<>=~])", current_line)

                    for token in tokens:
                        token = token.strip()   # this is necessary sa re.split result has random empty strings, spaces, etc
                        if token != "":
                            self.token_array.append(token)
                            self.total_token_num += 1

                    # TODO: handle multi-line comments
                current_line = file.readline()

        self.current_token_index = 0

    def has_more_tokens(self) -> bool:
        return True if self.current_token_index < self.total_token_num else False

    def advance(self):
        self.current_token_index += 1

    def get_token_and_type(self) -> Tuple[str, TokenType]:
        current_token = self.token_array[self.current_token_index]

        # if it is a quote that we encounter, flip `quote_open` flag and move 1 token forward
        # as we do not consider quotes as a token
        if current_token == "\"":
            self.quote_open = not self.quote_open
            self.current_token_index += 1
            return self.get_token_and_type()
    
        # as long as it is inside quotes, everything is considered a string constant
        if self.quote_open:
            return current_token, TokenType.STR_CONST
        
        # if it wasn't wrapped in quotes, then we can classify based on the content itself
        if current_token.upper() in Tokenizer.keyword_list:
            return current_token, TokenType.KEYWORD
        elif current_token in Tokenizer.symbol_list:
            return current_token, TokenType.SYMBOL
        elif current_token.isdigit() and self.int_const_range[0] <= int(current_token) <= self.int_const_range[1]:
            return current_token, TokenType.INT_CONST
        else: 
            return current_token, TokenType.IDENTIFIER



class CompilationEngine:
    # TODO
    pass

# goal for today is to complete the tokenizer logic 

if __name__ == "__main__":
    """
    The input to JackAnalyzer can be a single file (x.jack) or
    a directory that contains 1+ jack files. 
    For each jack file, an output file called x.xml should be created.
    """
    fp = Path(sys.argv[1])
    files_to_translate = get_input_files(fp)

    for file in files_to_translate:
        output_file_name = file.with_suffix(".xml")
        tokenizer = Tokenizer(file) # is it the full path?
        #print(tokenizer.token_array)

        while tokenizer.has_more_tokens():
            token, type = tokenizer.get_token_and_type()
            print(token, type)
            tokenizer.advance()
