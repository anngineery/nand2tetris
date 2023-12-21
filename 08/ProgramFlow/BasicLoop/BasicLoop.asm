@0
D = A

@SP
A = M
M = D   // insert the constant

@SP
M = M + 1   // increment SP

@0
D = A

@LCL
D =  D + M  // compute the target addr

@SP
M = M - 1 // decrement the pointer
// store target addr at 'one above' the top of the stack temporarily (will be overriden anyway)
A = M + 1 
M = D
// get the pop value
A = A - 1
D = M
// go back to where we stored the target addr, pop the value there
A = A + 1
A = M
M = D

(LOOP_START)

@0
D = A

@ARG
A = D + M // compute the base addr + index, aka target addr
D = M      // get the target val

@SP
M = M + 1   // increment SP ahead of time
A = M - 1
M = D      // place the value where SP was originally pointing at

@0
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
D = D + M    // add two operands 

@SP
M = M + 1   // Increment the SP (ahead of time)
A = M - 1   // insert the result to where SP used to point at
M = D

@0
D = A

@LCL
D =  D + M  // compute the target addr

@SP
M = M - 1 // decrement the pointer
// store target addr at 'one above' the top of the stack temporarily (will be overriden anyway)
A = M + 1 
M = D
// get the pop value
A = A - 1
D = M
// go back to where we stored the target addr, pop the value there
A = A + 1
A = M
M = D

@0
D = A

@ARG
A = D + M // compute the base addr + index, aka target addr
D = M      // get the target val

@SP
M = M + 1   // increment SP ahead of time
A = M - 1
M = D      // place the value where SP was originally pointing at

@1
D = A

@SP
A = M
M = D   // insert the constant

@SP
M = M + 1   // increment SP

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

@0
D = A

@ARG
D =  D + M  // compute the target addr

@SP
M = M - 1 // decrement the pointer
// store target addr at 'one above' the top of the stack temporarily (will be overriden anyway)
A = M + 1 
M = D
// get the pop value
A = A - 1
D = M
// go back to where we stored the target addr, pop the value there
A = A + 1
A = M
M = D

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
M = M - 1
A = M
D = M

@LOOP_START
D;JNE

@0
D = A

@LCL
A = D + M // compute the base addr + index, aka target addr
D = M      // get the target val

@SP
M = M + 1   // increment SP ahead of time
A = M - 1
M = D      // place the value where SP was originally pointing at

