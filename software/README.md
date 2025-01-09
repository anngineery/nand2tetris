# Assembler
More information about the assembly language can be found [here](https://github.com/anngineery/nand2tetris?tab=readme-ov-file#hack-assembly-language--machine-code)

## How would a real-world assembler differ from this assembler?
It may be able to handle:
- more sophisticated symbols (ex) pointer arithmetic, etc
- macro commands

## Testing
A working assembler is provided by the course. This output was compared against that of my assembler to ensure the correctness.

# Virtual Machine
This is the second half of 2-tier compilation process. The VM converts the intermediate language (also called VM language) into the Hack assembly language.
## Specs
- stack-based
  ```
  push x --> stack[sp] = x; sp++
  pop    --> sp--; return stack[sp]
  ```
- function-based (a program consists of functions and each function has its stand-alone code and is separately handled)
- supported data types: int, bool, pointers (all are 16 bits)
- manages stack & heap
   - stack: working memory of VM operations; push/pop always involves the stack
   - heap: dedicated RAM area for storing objects and arrays
- 4 types of commands:
  1. arithmetic
	```
	type 1: command
	type 2: command arg1
	type 3: command arg1 arg2
	```
  2. memory access
  	- 8 segments: constant, local, argument, this, that, temp, pointer, static
  	  `push/pop segment_name index`
  3. program flow
	- unconditionl: `goto` label
	- conditional: `if-goto` label
  4. function calling
	- `function <func_name> <num_local_vars>`
	- `call <function_name> <num_args>`: the caller already pushed <num_args> arguments to the stack
	- `return`

## Testing
Process VM programs and run the resulting assembly files on the CPU Emulator to see it does what it's supposed to (the VM programs, test scripts that handle the initialization of things and the CPU Emulator are supplied by the course). As a debugging tool, the VM Emulator, which helps understand what happens in the input VM file visually, was also supplied.

# Compiler
This is the first half of 2-tier compilation process. The compiler converts the Jack language (high-level language) into the intermediate language (also called VM language).
## Booting Process
The compiler's expected to create 1 Main.vm file, which includes 1 VM function called `main`. Given this, the VM implementation is expected to set the SP to 256 and call `Sys.Init`, an argument-less OS function at the start. This `Sys.Init` in turns calls `Main.main` and the infinite loop at the end. Recall that the HACK platform is set up in a way that when it resets, it starts executing the instruction from ROM[0] and so on.

## Compilation Steps
1. Syntax analysis: objetive is to understand the structure of a program
	1. Lexical analysis: grouping a steam of characters into tokens that have meanings (aka tokenizing or scanning)
	2. parsing: attempting to match the resulting tokens to the syntax rules (grammars) of the language to see if it conforms
2. Code generation: 
   1. Handling (simple) variables
   2. Handling expressions
   3. Handling flow of control (if and while statements)
   4. Handling Objects
   5. Handling Arrays

## Tokens in Jack Language
1. keyword
2. symbols
3. integer constant
4. string constant
5. identifier

## Grammars
a set of rules that describe how tokens can be put together to create valid language constructs

## Parser Logic
The parser uses recursive descent parsing without backtracking. It's a top-down approach that is well suited for nested structure Jack language has

## Jack Program Compilation
- Each class is compiled separately
- within one class, each subroutine is looked at individually and they don't interfere with one another

## Testing
Feed in Jack program files and run the resulting VM files on the VM Emulator to see if the expected and actual results are identical (the test files and the VM Emulator were supplied by the course). The input Jack programs involve a lot features of the language to ensure the compiler can compile them correctly. Some examples are:
- arithmetic expressions
- various statements (if, while, do , let, return)
- function calls
- object oriented features (constructors, methods, fields, etc)
- arrays
- strings
- objects and static variables

# Operating System
Provide low-level services such as accessing the hardware resources (RAM, keyboard, screen, etc) and libraries for common math operations, string processing operations, etc.

## What is included
1. Math
2. Array
3. Memory
4. Screen
5. Output
6. String
7. Keyboard
8. Sys

## Testing
Compile the OS files along with a test .jack file that utilizes these OS functions with the provided compiler. Then run the output file generated in the VM Emulator to see it does what it is supposed to do
