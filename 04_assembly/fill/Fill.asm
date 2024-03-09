// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.
// pseudo code:
// while True:
// 	if keyboard == 0:
// 		paint_white()
// 	else:
//		paint_black()
//
// def paint():
//	for i < 8192:
//		screen[i] = 0 or 1

(INPUT)
@KBD
D=M

@WHITE
D, JEQ
@BLACK 
0, JMP

(WHITE)
@i
M=0

(WHITE_LOOP) // the first entire row
@i
D=M
@8192	// 8192 draws the whole screen
D=D-A
@INPUT
D; JGE

@i
D=M
@SCREEN
A=D+A	// accessing screen segment
M=0
@i
M=M+1
@WHITE_LOOP
0; JMP


(BLACK)
@i
M=0

(BLACK_LOOP) // the first entire row
@i
D=M
@8192	// 8192 draws the whole screen
D=D-A
@INPUT
D; JGE

@i
D=M
@SCREEN
A=D+A	// accessing screen segment
M=-1
@i
M=M+1
@BLACK_LOOP
0; JMP






