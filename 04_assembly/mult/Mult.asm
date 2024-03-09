// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
//
// This program only needs to handle arguments that satisfy
// R0 >= 0, R1 >= 0, and R0*R1 < 32768.

// Put your code here.

// This machine language does not support multiplication so I have to use loop + addition
// pseudo code:
// i = 0
// for i < R1:
// 	R2 += R0
// 	i += 1

@i
M = 0

@R2
M = 0

//if R1 is 0, then go to END
@R1
D=M
@END
D; JEQ

(LOOP)
// R2 += R0
@R0
D=M
@R2
M=D+M	

// increment i
@i
M=M+1	

//condition check: if i - R1 < 0 then jump to (LOOP)
D=M
@R1
D=D-M
@LOOP
D;JLT

(END)
// infinite loop
@END
0;JMP