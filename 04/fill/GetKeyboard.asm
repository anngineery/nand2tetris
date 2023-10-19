// Read keyboard input and store the colour for sprint in R0
(INPUT)
@KBD
D=M

@WHITE
D, JEQ
@BLACK 
0, JMP

(WHITE)
@R0
M=0
@INPUT
0; JEQ	

(BLACK)
@R0
M=-1
@INPUT
0; JEQ
