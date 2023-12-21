(SIMPLEFUNCTION.TEST)
@i
MD = 0

(SIMPLEFUNCTION.TEST$INIT_LCL)
@2
D = D - A   // D = i - arg_num

@SIMPLEFUNCTION.TEST$END_LCL
D; JGE

@SP
M = M + 1   // increment SP ahead of time
A = M - 1
M = 0   // init to zero

@i
MD = M + 1

@SIMPLEFUNCTION.TEST$INIT_LCL
0; JMP

(SIMPLEFUNCTION.TEST$END_LCL)

@0
D = A

@LCL
A = D + M // compute the base addr + index, aka target addr
D = M      // get the target val

@SP
M = M + 1   // increment SP ahead of time
A = M - 1
M = D      // place the value where SP was originally pointing at

@1
D = A

@LCL
A = D + M // compute the base addr + index, aka target addr
D = M      // get the target val

@SP
M = M + 1   // increment SP ahead of time
A = M - 1
M = D      // place the value where SP was originally pointing at

@SP
AM = M - 1   // decrement sp, and get the top operand   
D = M       

@SP
AM = M - 1   // decrement sp, and get the bottom operand   
D = M + D    // add two operands 

@SP
M = M + 1   // Increment the SP (ahead of time)
A = M - 1   // insert the result to where SP used to point at
M = D

@SP
A = M - 1   // don't decrement SP, bc it will be the same in the end
M = !M

@0
D = A

@ARG
A = D + M // compute the base addr + index, aka target addr
D = M      // get the target val

@SP
M = M + 1   // increment SP ahead of time
A = M - 1
M = D      // place the value where SP was originally pointing at

@SP
AM = M - 1   // decrement sp, and get the top operand   
D = M       

@SP
AM = M - 1   // decrement sp, and get the bottom operand   
D = M + D    // add two operands 

@SP
M = M + 1   // Increment the SP (ahead of time)
A = M - 1   // insert the result to where SP used to point at
M = D

@1
D = A

@ARG
A = D + M // compute the base addr + index, aka target addr
D = M      // get the target val

@SP
M = M + 1   // increment SP ahead of time
A = M - 1
M = D      // place the value where SP was originally pointing at

@SP
AM = M - 1   // decrement sp, and get the top operand   
D = M       

@SP
AM = M - 1   // decrement sp, and get the bottom operand   
D = M - D    // bottom - top

@SP
M = M + 1   // Increment the SP (ahead of time)
A = M - 1   // insert the result to where SP used to point at
M = D

@LCL
D = M

@frame 
M = D   // frame = LCL
AM = M - 1  // trick: decrement the frame pointer var
D = M   // D = *(frame - 1)
@THAT
M = D

@frame 
AM = M - 1  // trick: decrement frame again
D = M   // D = *(frame - 2)
@THIS
M = D

@SP
A = M - 1 
D = M       // D = pop value
@ARG
A = M
M = D       // *ARG = pop()

@ARG
D = M + 1
@SP
M = D   // SP = ARG + 1

@frame 
AM = M - 1  // trick: decrement frame again
D = M   // D = *(frame - 3)
@ARG
M = D

@frame 
AM = M - 1  // trick: decrement frame again
D = M   // D = *(frame - 4)
@LCL
M = D

@frame 
A = M - 1
A = M   // A = *(frame - 5) = return address
0; JMP

(INF_LOOP)
@INF_LOOP
0; JMP