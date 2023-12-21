(SYS.INIT)
@i
MD = 0

(SYS.INIT$INIT_LCL)
@0
D = D - A   // D = i - arg_num

@SYS.INIT$END_LCL
D; JGE

@SP
M = M + 1   // increment SP ahead of time
A = M - 1
M = 0   // init to zero

@i
MD = M + 1

@SYS.INIT$INIT_LCL
0; JMP

(SYS.INIT$END_LCL)

@4000
D = A

@SP
A = M
M = D   // insert the constant

@SP
M = M + 1   // increment SP

@0
D = A

@THIS
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

@5000
D = A

@SP
A = M
M = D   // insert the constant

@SP
M = M + 1   // increment SP

@1
D = A

@THIS
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

@RET_FROM_SYS.MAIN_5
D = A
@SP
M = M + 1   // increment SP ahead of time
A = M - 1
M = D   // push return address

@LCL
D = M
@SP
M = M + 1   // increment SP ahead of time
A = M - 1
M = D   // save LCL

@ARG
D = M
@SP
M = M + 1   // increment SP ahead of time
A = M - 1
M = D   // save ARG

@THIS
D = M
@SP
M = M + 1   // increment SP ahead of time
A = M - 1
M = D   //save THIS

@THAT
D = M
@SP
M = M + 1   // increment SP ahead of time
A = M - 1
M = D   //save THAT

@SP
D = M
@LCL
M = D   // LCL = SP
@ARG
M = D   // ARG = SP
@5 
D = A
@0
D = D + A   // D = 5 + arg_num
@ARG
M = M - D   // ARG = SP - (5 + arg_num)

@SYS.MAIN
0; JMP

(RET_FROM_SYS.MAIN_5)

@1
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

(LOOP)

@LOOP
0;JMP

(SYS.MAIN)
@i
MD = 0

(SYS.MAIN$INIT_LCL)
@5
D = D - A   // D = i - arg_num

@SYS.MAIN$END_LCL
D; JGE

@SP
M = M + 1   // increment SP ahead of time
A = M - 1
M = 0   // init to zero

@i
MD = M + 1

@SYS.MAIN$INIT_LCL
0; JMP

(SYS.MAIN$END_LCL)

@4001
D = A

@SP
A = M
M = D   // insert the constant

@SP
M = M + 1   // increment SP

@0
D = A

@THIS
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

@5001
D = A

@SP
A = M
M = D   // insert the constant

@SP
M = M + 1   // increment SP

@1
D = A

@THIS
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

@200
D = A

@SP
A = M
M = D   // insert the constant

@SP
M = M + 1   // increment SP

@1
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

@40
D = A

@SP
A = M
M = D   // insert the constant

@SP
M = M + 1   // increment SP

@2
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

@6
D = A

@SP
A = M
M = D   // insert the constant

@SP
M = M + 1   // increment SP

@3
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

@123
D = A

@SP
A = M
M = D   // insert the constant

@SP
M = M + 1   // increment SP

@RET_FROM_SYS.ADD12_22
D = A
@SP
M = M + 1   // increment SP ahead of time
A = M - 1
M = D   // push return address

@LCL
D = M
@SP
M = M + 1   // increment SP ahead of time
A = M - 1
M = D   // save LCL

@ARG
D = M
@SP
M = M + 1   // increment SP ahead of time
A = M - 1
M = D   // save ARG

@THIS
D = M
@SP
M = M + 1   // increment SP ahead of time
A = M - 1
M = D   //save THIS

@THAT
D = M
@SP
M = M + 1   // increment SP ahead of time
A = M - 1
M = D   //save THAT

@SP
D = M
@LCL
M = D   // LCL = SP
@ARG
M = D   // ARG = SP
@5 
D = A
@1
D = D + A   // D = 5 + arg_num
@ARG
M = M - D   // ARG = SP - (5 + arg_num)

@SYS.ADD12
0; JMP

(RET_FROM_SYS.ADD12_22)

@0
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

@1
D = A

@LCL
A = D + M // compute the base addr + index, aka target addr
D = M      // get the target val

@SP
M = M + 1   // increment SP ahead of time
A = M - 1
M = D      // place the value where SP was originally pointing at

@2
D = A

@LCL
A = D + M // compute the base addr + index, aka target addr
D = M      // get the target val

@SP
M = M + 1   // increment SP ahead of time
A = M - 1
M = D      // place the value where SP was originally pointing at

@3
D = A

@LCL
A = D + M // compute the base addr + index, aka target addr
D = M      // get the target val

@SP
M = M + 1   // increment SP ahead of time
A = M - 1
M = D      // place the value where SP was originally pointing at

@4
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

@LCL
D = M

@frame 
M = D   // frame = LCL
@5
D = A
@frame 
AM = M - D   // frame = LCL - 5
D = M
@return_address
M = D   // return address need to be saved in a temp variable
// this is because for argumentless func, memory address that hold
// return address is the same as where ARG is pointing
// so when ARG 0 gets overriden with the return value, return address gets wiped out

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
AM = M + 1
D = M   // D = *(frame - 4)
@LCL
M = D

@frame 
AM = M + 1
D = M   // D = *(frame - 3)
@ARG
M = D

@frame 
AM = M + 1
D = M   // D = *(frame - 2)
@THIS
M = D

@frame 
AM = M + 1
D = M   // D = *(frame - 1)
@THAT
M = D

@return_address 
A = M
0; JMP

(SYS.ADD12)
@i
MD = 0

(SYS.ADD12$INIT_LCL)
@0
D = D - A   // D = i - arg_num

@SYS.ADD12$END_LCL
D; JGE

@SP
M = M + 1   // increment SP ahead of time
A = M - 1
M = 0   // init to zero

@i
MD = M + 1

@SYS.ADD12$INIT_LCL
0; JMP

(SYS.ADD12$END_LCL)

@4002
D = A

@SP
A = M
M = D   // insert the constant

@SP
M = M + 1   // increment SP

@0
D = A

@THIS
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

@5002
D = A

@SP
A = M
M = D   // insert the constant

@SP
M = M + 1   // increment SP

@1
D = A

@THIS
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

@ARG
A = D + M // compute the base addr + index, aka target addr
D = M      // get the target val

@SP
M = M + 1   // increment SP ahead of time
A = M - 1
M = D      // place the value where SP was originally pointing at

@12
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
D = D + M    // add two operands 

@SP
M = M + 1   // Increment the SP (ahead of time)
A = M - 1   // insert the result to where SP used to point at
M = D

@LCL
D = M

@frame 
M = D   // frame = LCL
@5
D = A
@frame 
AM = M - D   // frame = LCL - 5
D = M
@return_address
M = D   // return address need to be saved in a temp variable
// this is because for argumentless func, memory address that hold
// return address is the same as where ARG is pointing
// so when ARG 0 gets overriden with the return value, return address gets wiped out

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
AM = M + 1
D = M   // D = *(frame - 4)
@LCL
M = D

@frame 
AM = M + 1
D = M   // D = *(frame - 3)
@ARG
M = D

@frame 
AM = M + 1
D = M   // D = *(frame - 2)
@THIS
M = D

@frame 
AM = M + 1
D = M   // D = *(frame - 1)
@THAT
M = D

@return_address 
A = M
0; JMP

