"""
Jack syntax analyzer that converts the high-level Jack language into the intermediate VM language.
It does not handle error reporting as it assumes all input conforms to Jack language grammar perfectly.
The input to JackAnalyzer can be a single file (x.jack) or a directory that contains 1+ jack files. 
For each .jack file, an output file should have the same name with .xml extension.

Seperation of Responsibilities:
- Tokenizer's only responsibility is to break down the input file into tokens.
- CompilationEngine's only responsbility is to structure token streams into a proper program
    structure using the language grammar specification.
- JackAnalyzer handles orchestration and file handling (including XML string formatting). Essentially, whatever is temporary and will be replaced by the actual code writer soon is done by JackAnalyzer so the transition is smooth.
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
        compiled_output = []    # will be filled out by the compilation engine
        output_file_name = file.with_suffix(".xml")
        tokenizer = Tokenizer(file)

        # first, the tokenizer extracts the stream of tokens from the input file
        while tokenizer.has_more_tokens():
            token, type = tokenizer.get_token_and_type()
            token_stream.append((token, type))
            tokenizer.advance()

        # second, the compilation engine structures tokens into a program
        engine = CompilationEngine(token_stream, compiled_output)
        engine.compile_class()

        # third, the final xml is generated
        with open(output_file_name, "w") as file:
            for line in compiled_output:
                # convert some symbols used by XMLs to display properly
                if line == "<symbol> < </symbol>":
                    line = "<symbol> &lt; </symbol>"
                elif line == "<symbol> > </symbol>":
                    line = "<symbol> &gt; </symbol>"
                elif line == "<symbol> \" </symbol>":
                    line = "<symbol> &quot; </symbol>"
                elif line == "<symbol> & </symbol>":
                    line = "<symbol> &amp; </symbol>"

                file.write(line + "\n") # I don't bother to use XMLTree and stuff, because this portion will be replaced by code writing anyway