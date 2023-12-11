@10
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

@21
D = A

@SP
A = M
M = D   // insert the constant

@SP
M = M + 1   // increment SP

@22
D = A

@SP
A = M
M = D   // insert the constant

@SP
M = M + 1   // increment SP

@2
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

@1
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

@36
D = A

@SP
A = M
M = D   // insert the constant

@SP
M = M + 1   // increment SP

@6
D = A

@THIS
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

@42
D = A

@SP
A = M
M = D   // insert the constant

@SP
M = M + 1   // increment SP

@45
D = A

@SP
A = M
M = D   // insert the constant

@SP
M = M + 1   // increment SP

@5
D = A

@THAT
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

@2
D = A

@THAT
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

@510
D = A

@SP
A = M
M = D   // insert the constant

@SP
M = M + 1   // increment SP

@6
D = A

@R5
D =  D + A  // compute the target addr

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

@LCL
A = D + M // compute the base addr + index, aka target addr
D = M      // get the target val

@SP
M = M + 1   // increment SP ahead of time
A = M - 1
M = D      // place the value where SP was originally pointing at

@5
D = A

@THAT
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

@6
D = A

@THIS
A = D + M // compute the base addr + index, aka target addr
D = M      // get the target val

@SP
M = M + 1   // increment SP ahead of time
A = M - 1
M = D      // place the value where SP was originally pointing at

@6
D = A

@THIS
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
AM = M - 1   // decrement sp, and get the top operand   
D = M       

@SP
AM = M - 1   // decrement sp, and get the bottom operand   
D = M - D    // bottom - top

@SP
M = M + 1   // Increment the SP (ahead of time)
A = M - 1   // insert the result to where SP used to point at
M = D

@6
D = A

@R5
A = D + A // compute the base addr + index, aka target addr
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

(infinite_loop)
@infinite_loop
0; JMP