"""
Converts the high-level Jack language into the intermediate VM language.
It does not handle error reporting as it assumes all input conforms to Jack language grammar perfectly.
The input can be a single file (x.jack) or a directory that contains 1+ jack files. 
For each .jack file, an output file should have the same name with .xml extension.

Seperation of Responsibilities:
- Tokenizer's only responsibility is to break down the input file into tokens.
- Compilation engine's only responsbility is to structure token streams into a proper program
    structure using the language grammar specification.
"""
from pathlib import Path
import sys
from tokenizer import Tokenizer
from compilation_engine import CompilationEngine
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


if __name__ == "__main__":
    fp = Path(sys.argv[1])
    files_to_translate = get_input_files(fp)

    for file in files_to_translate:
        token_stream: List[Tuple[str]] = [] # will be filled out by the tokenizer
        output_file_name = file.with_suffix(".vm")
        tokenizer = Tokenizer(file)

        # first, the tokenizer extracts the stream of tokens from the input file
        while tokenizer.has_more_tokens():
            token, type = tokenizer.get_token_and_type()
            token_stream.append((token, type))
            tokenizer.advance()

        # second, the compilation engine processes the tokens and write a VM program
        engine = CompilationEngine(token_stream, output_file_name)
        engine.compile_class()
