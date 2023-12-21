// initialize pointer registers
@256
D = A
@SP
M = D
@LCL
M = -1
@ARG
M = -1
@THIS
M = -1
@THAT
M = -1

@RET_FROM_SYS.INIT_0
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

@SYS.INIT
0; JMP

(RET_FROM_SYS.INIT_0)

(INF_LOOP)
@INF_LOOP
0; JMP

(CLASS1.SET)
@i
MD = 0

(CLASS1.SET$INIT_LCL)
@0
D = D - A   // D = i - arg_num

@CLASS1.SET$END_LCL
D; JGE

@SP
M = M + 1   // increment SP ahead of time
A = M - 1
M = 0   // init to zero

@i
MD = M + 1

@CLASS1.SET$INIT_LCL
0; JMP

(CLASS1.SET$END_LCL)

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
M = M - 1   // decrement the pointer
A = M
D = M

@Class1.0
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
M = M - 1   // decrement the pointer
A = M
D = M

@Class1.1
M = D                    


@0
D = A

@SP
A = M
M = D   // insert the constant

@SP
M = M + 1   // increment SP

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

(CLASS1.GET)
@i
MD = 0

(CLASS1.GET$INIT_LCL)
@0
D = D - A   // D = i - arg_num

@CLASS1.GET$END_LCL
D; JGE

@SP
M = M + 1   // increment SP ahead of time
A = M - 1
M = 0   // init to zero

@i
MD = M + 1

@CLASS1.GET$INIT_LCL
0; JMP

(CLASS1.GET$END_LCL)

@Class1.0
D = M

@SP
A = M
M = D   // insert the constant

@SP
M = M + 1   // increment SP

@Class1.1
D = M

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

(CLASS2.SET)
@i
MD = 0

(CLASS2.SET$INIT_LCL)
@0
D = D - A   // D = i - arg_num

@CLASS2.SET$END_LCL
D; JGE

@SP
M = M + 1   // increment SP ahead of time
A = M - 1
M = 0   // init to zero

@i
MD = M + 1

@CLASS2.SET$INIT_LCL
0; JMP

(CLASS2.SET$END_LCL)

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
M = M - 1   // decrement the pointer
A = M
D = M

@Class2.0
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
M = M - 1   // decrement the pointer
A = M
D = M

@Class2.1
M = D                    


@0
D = A

@SP
A = M
M = D   // insert the constant

@SP
M = M + 1   // increment SP

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

(CLASS2.GET)
@i
MD = 0

(CLASS2.GET$INIT_LCL)
@0
D = D - A   // D = i - arg_num

@CLASS2.GET$END_LCL
D; JGE

@SP
M = M + 1   // increment SP ahead of time
A = M - 1
M = 0   // init to zero

@i
MD = M + 1

@CLASS2.GET$INIT_LCL
0; JMP

(CLASS2.GET$END_LCL)

@Class2.0
D = M

@SP
A = M
M = D   // insert the constant

@SP
M = M + 1   // increment SP

@Class2.1
D = M

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

@6
D = A

@SP
A = M
M = D   // insert the constant

@SP
M = M + 1   // increment SP

@8
D = A

@SP
A = M
M = D   // insert the constant

@SP
M = M + 1   // increment SP

@RET_FROM_CLASS1.SET_28
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
@2
D = D + A   // D = 5 + arg_num
@ARG
M = M - D   // ARG = SP - (5 + arg_num)

@CLASS1.SET
0; JMP

(RET_FROM_CLASS1.SET_28)

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

@23
D = A

@SP
A = M
M = D   // insert the constant

@SP
M = M + 1   // increment SP

@15
D = A

@SP
A = M
M = D   // insert the constant

@SP
M = M + 1   // increment SP

@RET_FROM_CLASS2.SET_33
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
@2
D = D + A   // D = 5 + arg_num
@ARG
M = M - D   // ARG = SP - (5 + arg_num)

@CLASS2.SET
0; JMP

(RET_FROM_CLASS2.SET_33)

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

@RET_FROM_CLASS1.GET_36
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

@CLASS1.GET
0; JMP

(RET_FROM_CLASS1.GET_36)

@RET_FROM_CLASS2.GET_38
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

@CLASS2.GET
0; JMP

(RET_FROM_CLASS2.GET_38)

(WHILE)

@WHILE
0;JMP

