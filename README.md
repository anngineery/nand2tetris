# Objective
Build a fully functioning general-purpose computer, both hardware and software components, from scratch. This computer implments Harvard Architecture.

# Part 1: Hardware
Using a mock Hardware Description Language (HDL), implement the boolean logic for 15 elementary logic gates, an ALU, RAM, and finally integrate them all to build the HACK computer platform

# Part 2: Software
Implement:
1. an assembler (Hack assembly code --> machine code)
2. a VM translator (Intermediate language/VM language --> Hack assembly)
3. a compiler (Jack high-level langauge --> intermediate language/VM language)
4. Operating System libraries used by Jack programs

# HACK Computer
## General Specs 
- 16-bit machine
- 15-bit memory address space (32K RAM)
- D register (for data) and A register (for address) in CPU. M register represents RAM register addressed by A (i.e. `M = RAM[A]`)
- Peripherals (Memory-mapped I/O):
	- Screen: 512 * 256 pixels; address starts from 16384
 	- Keyboard: single word memory map located at address 24576

## Hack Assembly Language & Machine Code
### Instructions
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

### Symbols
Predefined symbols for a special subset of RAM addresses
1. Virtual registers: R0-R15 (equivalent to M[0]-M[15]
2. Predefined pointers: SP(R0), LCL(R1), ARG(R2), THIS(R3), THAT(R4)
3. I/O pointers: SCREEN(=M[16384]), KBD(=M[24576]) NOTE - 16384 and 24576 are base addresses of the memory map

**Label symbols** are user-defined symbols used to label destinations of `goto` commands. It can only be defined once and can be used anywhere in the program even before the definition.\
**Variable symbols** - assembler chooses an unique memory address starting M[16]

### Syntax Conventions & File Format
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

# Inspiration
[Build a Modern Computer from First Principles: From Nand to Tetris](https://www.nand2tetris.org/) offered by Hebrew University of Jerusalem. This is a project-based course and all the code uploaded here is my original work.
