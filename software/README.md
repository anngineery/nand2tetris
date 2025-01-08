# Virtual Machine
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

# Compiler
## Booting Process
The compiler's expected to create 1 Main.vm file, which includes 1 VM function called `main`. Given this, the VM implementation is expected to set the SP to 256 and call `Sys.Init`, an argument-less OS function at the start. This `Sys.Init` in turns calls `Main.main` and the infinite loop at the end. Recall that the HACK platform is set up in a way that when it resets, it starts executing the instruction from ROM[0] and so on.

## Typical components of a Compiler
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
