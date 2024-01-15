"""
Jack syntax analyzer that converts the high-level Jack language into the intermediate VM language.
It does not handle error reporting as it assumes all input conforms to Jack language grammar perfectly.
The input to JackAnalyzer can be a single file (x.jack) or
a directory that contains 1+ jack files. 
For each jack file, an output file called x.xml should be created.
"""
from pathlib import Path
import sys
from compiler.tokenizer import Tokenizer
from typing import List


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
        output_file_name = file.with_suffix(".xml")
        tokenizer = Tokenizer(file) # is it the full path?
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