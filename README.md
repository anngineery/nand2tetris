# nand2tetris
[Build a Modern Computer from First Principles: From Nand to Tetris](https://www.nand2tetris.org/) offered by Hebrew University of Jerusalem

# Objective
Build a fully functioning general purpose computer, both hardware and software components, from scratch.\
This computer follows [Von Neumann Architecture](https://www.computerscience.gcse.guru/wp-content/uploads/2016/04/Von-Neumann-Architecture-Diagram.jpg).

## Week 1
Project: implement boolean logic of 15 elementary logic gates using Hardware Description Language (HDL)

## Week 2
Project: build Arithmetic Logic Unit (ALU) 

## Week 3
Project: build Random Access Memory (RAM) 

### Building Blocks of RAM and Important Terms
1. Clock
   - oscillator that generates signals alternating between 0 and 1 at a fixed rate
   - 1 cycle = 1 discrete time unit (for simplicity, although time is actually continuous); A cycle should be long enough to account for propagation delays and to signals to stabilize
   - a small triangle symbol on a chip diagram indicates that it takes clock input
2. Flip-flop: there are many types, but we are focusing on Data Flip-flop (DFF) here
   - it "moves" input from time t to output at time t+1 (aka remembers the previous state): `out[t] = in[t-1]`
   - takes 1-bit input, clock output and generates 1-bit output
   - **important: It remembers the state for only 1 time unit** 
3. 1-bit Register
   - a storage device that can remember the input *forever* unless it is told to load a new value
   - takes 1-bit input, load bit and clock input. Generates 1-bit output
   - `if load[t-1] == 1, out[t] = in[t-1]; else: out[t] = out[t-1]`
   - how to build 1-bit register using DFF: [diagram](https://i.stack.imgur.com/XjmZNm.png)
      - output is either in[t-1] or output[t-1] depending on the load bit --> requires a mux
      - `else` portion requires a feedback loop
   - register's state = the value currently stored "inside" the register
   - width (w) = # of bits it holds (for multi-bit register)
   - word = the content of multi-bit register
   - register is the most basic element of memory
4. RAM
   - a main memory of computer that stores both data and instructions
   - a sequence of n registers that are individually addressable (address range: 0 ~ n-1)
   - width of address bit (k) = log2(n)
   - only one register is in action at any given time
   - takes input of width `w`, address bits of size `k`, a load bit and the clock input. Output size is also `w`
   - to read register `i`: set address=`i` and probe output. The output should be the state of register `i`
   - to write `v` to register `i`: set address=`i`, in=`v`, load=1. The state of register `i` becomes `v` and from the next cycle onward, out=`v`
   - why called "random access"? Irrespective of the size of memory, meaning # of registers inside, any chosen register can be access in the same amount of time
5. Program Counter (PC)
   - contains the address of instruction that needs to be executed next
   - Three possible control settings:
      - reset (fetch the first instruction): PC = 0
      - increment (fetch the next instruction): PC++
      - goto (skip to instruction n): PC = n
   - has three control bits (reset, inc, load) along with input bits and the clock input

## Week 4
Project: Writing programs with assembly language

### HACK Computer HW
![Architecture diagram](hack_computer_arch.png)
- ~~Von Neumann architecture~~ (I think it is closer to Harvard architecture. See [here](https://courses.cs.washington.edu/courses/cse490h1/19wi/exhibit/john-von-neumann-1.html)): same computer can be used for different objectives based on the program it's running (universality of computer)
- Memory address space: 15 bits -> have 2^15 (32768 = 32k) locations in the memory 
- 16-bit machine -> meaning, word size is 16 bits. Registers store 16-bit values and data/instructions in the memory are also 16 bits
- Registers:
   - D register: inside CPU
   - A register: inside CPU
   - M register: inside RAM. Represent RAM register addressed by A. There can only be one `M` at a time. (i.e. `M = RAM[A]`)
- Screen (output device):
   - 512 * 256 pixels. Since each pixel is 1 bit (turn on/off), we need 131072 bits to represent the full screen
   - Each memory location can hold 16 bits. 131072/16 = 8192 = 8*1024 locations should be allocated
   - 16 bits * 32 = 512 bits --> 1 row is spread across 32 consecutive addresses
   - Remember that word size (the atomic unit) is 16 bits, therefore we cannot access an individual bit but access the whole word
   - (ex) want to access screen(r, c) -> The target word is: RAM[16384 + r * 32 + c/16]. Within that word, (c % 16)th bit is the one we want
- Keyboard (input device):
   - Single word memory map located at address 24576
   - When a key is pressed, 16 bit ASCII code. When key is not pressed, the whole word is 0
 
### HACK Computer Instructions
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

### HACK Computer Symbols
Predefined symbols for a special subset of RAM addresses
1. Virtual registers: R0-R15 (equivalent to M[0]-M[15]
2. Predefined pointers: SP(R0), LCL(R1), ARG(R2), THIS(R3), THAT(R4)
3. I/O pointers: SCREEN(=M[16384]), KBD(=M[24576]) NOTE - 16384 and 24576 are base addresses of the memory map

**Label symbols** are user-defined symbols used to label destinations of `goto` commands. It can only be defined once and can be used anywhere in the program even before the definition.
**Variable symbols** - assembler chooses an unique memory address starting M[16]

### Syntax Conventions & File Format
- Binary code file: .hack extension, each line = sequence of 16 0s and 1s = 1 machine instruction
- Assembly language file: .asm extension, each line = either an A instruction, C instruction or a symbol declaration (Note that symbol declaration is a pseudo-command that does not generate an equivalent machine code. It only causes the assembler to assign the label `symbol` to the memory location of the instruction that follows `(symbol)` statement)
- Constants: positive #s written in decimal format
- Symbols: cannot start with a digit, but can consist of digits, letters, underscores, dots, dollar signs and colons
- Comments: `//`
- Whitespace: can be used for better readability, but get ignored by the assembler
- Case Convention (HACK is case-sensitive!):
   - Assembly mnemonics -> all caps
   - Labels -> all caps
   - Variables -> lower case
- End the program with an infinite loop, otherwise the program will keep going

## Week 5
Project: Build a full Hack Computer System that can run Hack assembly language programs (week 4) using components built from week 1-3 

### Universal Turing Machine and Von Neumann Architecture
Universal turing machine is a theoretical concept of a machine that can do everything enabled through software (stored program). An architecture that implements this is Von Neumann Architecture, which is explained extensively below.

#### Component 1: Memory
- physical perspective: an array of registers
- logical perspective: store data and instructions. To a computer, their type is indistinguishable.
- there are 2 variants depending on how the memory is structured:
   1. data and memory in the same physical memory unit
   2. they are kept in different memory units, thus have distinct address spaces -> known as the **Harvard Architecture**
- side note: Why is RAM (Random Access Memory) called RAM? It means no matter which register you access (irrespective of the memory size and the register's location in it), the access time is the same.  

#### Component 2: CPU
- responsible for executing the instructions loaded in memory -> fetch-decode-execute on repeat
- An instruction specifies (1) what operation to perform, (2) which registers need to be read/write and (3) which instruction needs to be fetch for execution in the next cycle
- consists of ALU, registers and control unit
- 2 different design approaches for performance: (1) Complex Instruction Set Computing (CISC) or (2) Reduced Instruction Set Computing (RISC)
##### ALU
- what ALU can do depends on the needs budget, energy, cost, etc
- any function not supported by ALU can be later done in software, but it will be slower
##### Register
- fast, efficient processing speed is vital to CPU. Therefore, it is beneficial to store store the intermediate results locally close to the ALU. A typical CPU has a dozens of registers
- why is it faster than memory access? Only a few of them there, so we only need a few bits to address them. With that, we can do an operation like `someCpuRegister = 0` in 1 instruction as opposed to using 1 instruction just to pass the address and another one to supply the operation instruction
- registers used in CPU:
   1. data register: temporary storage for intermediate computation result. Similar to a temp variable in SW
   2. address register: store memory address to operate on. Output of this register (which represents a memory address) feeds into the addr input of a memory device. But it can also be used as an extra data register
   3. program counter (PC): keep the address of the next instruction to run. Although the name says a "register", it is not _just_ a register. It contains muxes to handle different inputs and has more control bits (reset, load and increment) than a regular register. 
##### Control Unit
- an instruction should be decoded once it is fetched in order to be executed.
- the decoded info should be used to signal necessary hardware components (ALU, registers, memory) to get the job done

#### Component 3: I/O Devices
- Memory-mapped I/O is an abstraction used to help the computer be device-agnosotic. Each device is allocated a designated area in the memory (the memory map) and looks like a regular memory segment to the CPU
- CPU and I/O device should have an agreed upon rules to follow:
  1. I/O device should be mapped to 1D array of memory structure. So in the case of a screen, which has 2D structure naturally, needs to be flattened
  2. I/O device needs to provide an interaction protocol so that CPU can access the device. (ex) keyboard - which binary code to use for each key? This is where standards make our lives easier!)
- In modern computer, we don't write bits to memory directly to control I/O devices. Instead, for example, the CPU sends instructions to a graphics card that controls the screen

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

