(FILL)
@i
M=0

(LOOP) // the first entire row
@i
D=M
@8192	// 8192 draws the whole screen
D=D-A
@END
D; JGE

@i
D=M
@SCREEN
A=D+A	// accessing screen segment
M=-1
@i
M=M+1
@LOOP
0; JMP

(END)
@END
0; JMP