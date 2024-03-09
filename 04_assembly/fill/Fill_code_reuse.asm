// Duplicate code less compared to Fill.asm.
// It stores a color to use in colour variable.
// Since the boiler-plate code to fill the screen is identical
// regardless of the colour, just need to grab the right colour
// from the variable.
(INPUT)
@KBD
D=M

@WHITE
D, JEQ
@BLACK 
0, JMP

(SET_WHITE)
@colour
M=0
@FILL
0; JEQ	

(SET_BLACK)
@colour
M=-1
@FILL
0; JEQ

(FILL)
@i
M=0

(LOOP) // the first entire row
@i
D=M
@8192	// 8192 draws the whole screen
D=D-A
@INPUT
D; JGE

@i
D=M
@SCREEN
D=D+A
@CURRENT_SCREEN_SEGMENT
M=D
@colour
D=M
@CURRENT_SCREEN_SEGMENT
A=M
M=D
@i
M=M+1
@LOOP
0; JMP

(END)
@END
0; JMP