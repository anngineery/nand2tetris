# nand2tetris
[Build a Modern Computer from First Principles: From Nand to Tetris](https://www.nand2tetris.org/) offered by Hebrew University of Jerusalem

# Objective
Build a fully functioning general purpose computer, both hardware and software components, from scratch

# What I have learned from the course
## Week 1
Project: implement boolean logic of 15 elementary logic gates using Hardware Description Language (HDL)

### 2 ways to describe a boolean function:
1. Boolean formula
2. Truth table
   
Going from (1) -> (2): substitute possible input values and evaluate the output\
Going from (2) -> (1): construct a disjunctive normal form formula and simplify the expression using boolean identities

### Boolean Identities
[table](http://www.cs.ucc.ie/osullb/cs1101/labs/08a/identities.jpg)

### Important & Interesting Theorem
Any boolean function can be represetned only using AND, NOT and OR gates\
--> Any boolean function can be represetned only using AND and NOT gates
  > Proof: X or Y = NOT (NOT X AND NOT Y) --  De Morgan's Law

--> Any boolean function can be represetned only using NAND gates
  > Proof: \
  > NOT X = NOT (X AND X) = X NAND X \
  > X AND Y = NOT (NOT (X AND Y)) = NOT (X NAND Y)

### Interface VS Implementation of a Gate
| Interface    | Implementation |
| -------- | ------- |
| *how* does it do it? | *what* is it supposed to do? |
| Not unique (multiple implementations possible for a gate) | unique (only 1 for a gate) |

[Logic gate diagrams](https://logancollinsblog.files.wordpress.com/2020/06/table1.png?w=340&h=619)

### Miscellaneous 
- Bus: multiple bits that are manipulated together as one entity
- HDL: functional/declarative language. It does not describe procedures/executions but a static structure of a chip, so the order of statements is not important

## Week 2
Project: build Arithmetic Logic Unit (ALU) 

### Numbers we can represent with n bits
If all positive: 0 ~ 2<sup>n</sup>-1\
If including negative numbers (using 2's complement): 
- positive range: 0 ~ 2<sup>n-1</sup>-1   --> MSB = 0
- negative range: -2<sup>n-1</sup> ~ -1   --> MSB = 1

### 2's Complement
If there is a n-bit binary number, -x is represented as 2<sup>n</sup>-x \
So how do we compute -x? -x = 2<sup>n</sup>-x = 1 + (2<sup>n</sup>-1) - x --> just flip bits of x and add 1\
[Why using 2's complement to represent negative works well](https://math.stackexchange.com/questions/1920772/why-twos-complement-works)? Essentially turn subtraction into addition

### Adding two binary numbers
Overflow occurs when there is a carry from the MSB. This gets ignored by computer effectively making it arithmetic modulo of 2<sup>n</sup>

### Adders
- Half Adder: add 2 input bits and outputs a sum and a carry bit
- Full Adder: add 3 input bits and outputs a sum and a carry bit
