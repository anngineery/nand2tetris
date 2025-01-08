# Objective
Build a fully functioning general-purpose computer, both hardware and software components, from scratch. This computer implments Harvard Architecture.

# HACK Computer
## General Specs 
- 16-bit machine
- 15-bit memory address space (32K RAM)
- D register (for data) and A register (for address) in CPU. M register represents RAM register addressed by A (i.e. `M = RAM[A]`)
- Peripherals (Memory-mapped I/O):
	- Screen: 512 * 256 pixels; address starts from 16384
 	- Keyboard: single word memory map located at address 24576
  
## Instructions
- A (addressing) instructions: set A register to 15-bit value that represents a memory address
   - Syntax: (symbolic representation) `@value` | (binary representation) `0vvv vvvv vvvv vvvv`
   - Purpose:
        1. Only way to enter a constant into computer
        2. Prerequisite step for the next C instruction designed to manipulate the data memory
        3. Prerequisite step for a jump (branching), because it specifies the jump destination
- C (conditional) instructions: control the flow of the program
   - Syntax: `dest = comp; jump`
      - destination: where to store the computed value
      - compute: what to compute
      - jump: what instruction to execute next
   - Purpose:
      - allow repetitions (loops), conditional statements and subroutine calling

## Symbols
Predefined symbols for a special subset of RAM addresses
1. Virtual registers: R0-R15 (equivalent to M[0]-M[15]
2. Predefined pointers: SP(R0), LCL(R1), ARG(R2), THIS(R3), THAT(R4)
3. I/O pointers: SCREEN(=M[16384]), KBD(=M[24576]) NOTE - 16384 and 24576 are base addresses of the memory map

**Label symbols** are user-defined symbols used to label destinations of `goto` commands. It can only be defined once and can be used anywhere in the program even before the definition.
**Variable symbols** - assembler chooses an unique memory address starting M[16]

## Syntax Conventions & File Format
- Binary code file: .hack extension, each line = 1 machine instruction
- Assembly language file: .asm extension, each line = either an A instruction, C instruction or a symbol declaration
- Constants: positive #s written in decimal format
- Symbols: cannot start with a digit, but can consist of digits, letters, underscores, dots, dollar signs and colons
- Comments: `//`
- Whitespace: can be used for better readability, but get ignored
- Case Convention (HACK is case-sensitive!):
   - Assembly mnemonics -> all caps
   - Labels -> all caps
   - Variables -> lower case
- End the program with an infinite loop, otherwise the program will keep going


# Part 1: Hardware
Using a mock Hardware Description Language (HDL), implement the boolean logic for 15 elementary logic gates, an ALU, RAM, and finally integrate them all to build the HACK computer platform

# Part 2: Software


# Inspiration
[Build a Modern Computer from First Principles: From Nand to Tetris](https://www.nand2tetris.org/) offered by Hebrew University of Jerusalem. This is a project-based course and all the code uploaded here is written by me.


## Week 5
Project: Build a full Hack Computer System that can run Hack assembly language programs (week 4) using components built from week 1-3 

## Week 7 + 8
Project: Building a VM translator (part 1 - only handles arithmetic and memory segment access operations, part 2 - add branching and subroutine calling to Week 7's version)
     
### Stack-based VM
- Our VM translator will put operands and results of VM operations in a stack
- What is a stack? An abstract data structure that has 2 possible operations: push & pop (LIFO; always fetch from or push to the top of the stack)
- How to implement a stack? The easiest way is to have an array called stack + Stack Pointer variable that points to the top of the stack
  ```
  push x --> stack[sp] = x; sp++
  pop    --> sp--; return stack[sp]
  ```
- A surprising thing is that any arithmetic operation or boolean evaluation can be expressed in a sequence of operations on stack
   - push operands to the stack
   - pop them
   - do the operation
   - push the result to the stack
- Once we deal with subroutines, stack becomes even more useful. The "calling chain" of functions have LIFO pattern (last called funciton executes and returns first), which is the same as the property of a stack

### Our VM Specification
- stack-based
- function-based (a program consists of functions and each function has its stand-alone code and is separately handled)
- supported data types: 16 bits. can be int, bool, pointers
- manages 2 implicit data structures and VM commands change their states
   - stack: working memory of VM operations; push/pop always involves the stack
   - heap: dedicated RAM area for storing objects and arrays
- 4 types of commands:
  1. arithmetic
  2. memory access
  3. program flow *(Week 8)*
  4. function calling *(Week 8)*
 
#### Arithmetic Commands
- syntax:
```
type 1: command
type 2: command arg1
type 3: command arg1 arg2
```
#### Memory Access Commands
- stack machine is equipped with 8 segments: constant, local, argument, this, that, temp, pointer, static
- this is how we let go of symbolic variables (variable names in HLL)
- syntax: `push/pop segment_name index`

#### Branching Commands
introduces non-linear program flow
1. unconditionl: `goto` label
2. conditional: `if-goto` label
   - have to push an expression to evaluate beforehand
   - if NOT evaluates to zero then jump

#### Function Calling Commands
- `function <func_name> <num_local_vars>`
- `call <function_name> <num_args>`: the caller already pushed <num_args> arguments to the stack
- `return`

### Booting Process
The compiler's expected to create 1 Main.vm file, which includes 1 VM function called `main`. Given this, the VM implementation is expected to set the SP to 256 and call `Sys.Init`, an argument-less OS function at the start. This `Sys.Init` in turns calls `Main.main` and the infinite loop at the end. Recall that the HACK platform is set up in a way that when it resets, it starts executing the instruction from ROM[0] and so on.

## Week 10 + 11
Project: build a full blown compiler
### Typical components of a Compiler
1. Syntax analysis: objetive is to understand the structure of a program; in our case, the result is JackAnalyzer 
	1. Lexical analysis: also known as tokenizing or scanning; grouping a steam of character into tokens that have meanings
	2. parsing: attempting to match the resulting tokens to the syntax rules (grammars) of the language to see if it conforms
2. Code generation: 
   1. Handling (simple) variables
   2. Handling expressions
   3. Handling flow of control (if and while statements)
   4. Handling Objects
   5. Handling Arrays

Note that different languages have different set of tokens. (ex) In C, ++ is a valid token. But in Python it will become two +  tokens
Programming Language Specification must document the language's allowable tokens.
### Tokens in Jack Language
1. keyword
2. symbols
3. integer constant
4. string constant
5. identifier
### Grammars
Having a bunch of valid tokens do not mean it is a working program. The order of tokens is important. The grammar is a set of rules that describe how tokens can be put together to create valid language constructs
### Parser Logic
Our parser uses recursive descent parsing without backtracking. It's a top-down approach that is well suited for nested structure Jack language has. Most of the time, we only need to know the current token to figure out what language construct we are dealing with (LL(0)?) with very few exceptions. (while coding up the parser logic, there were some cases where I had to look 1 token ahead)
### Jack Program Compilation
- Each class is compiled separately
- within one class, each subroutine is looked at individually and they don't interfere with one another

