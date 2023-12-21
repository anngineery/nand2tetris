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

(MAIN.FIBONACCI)
@i
MD = 0

(MAIN.FIBONACCI$INIT_LCL)
@0
D = D - A   // D = i - arg_num

@MAIN.FIBONACCI$END_LCL
D; JGE

@SP
M = M + 1   // increment SP ahead of time
A = M - 1
M = 0   // init to zero

@i
MD = M + 1

@MAIN.FIBONACCI$INIT_LCL
0; JMP

(MAIN.FIBONACCI$END_LCL)

@0
D = A

@ARG
A = D + M // compute the base addr + index, aka target addr
D = M      // get the target val

@SP
M = M + 1   // increment SP ahead of time
A = M - 1
M = D      // place the value where SP was originally pointing at

@2
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

@LT_4
D; JLT

@SP         // 'not less than' portion
M = M + 1   // Increment the SP (ahead of time)
A = M - 1   // insert the result to where SP used to point at
M = 0       // false is 0

@NEXT_4
0; JMP

(LT_4)
@SP         
M = M + 1   // Increment the SP (ahead of time)
A = M - 1   // insert the result to where SP used to point at
M = -1      // true is -1

(NEXT_4) // so that when not equal, we can skip over (EQ_4)

@SP
M = M - 1
A = M
D = M

@IF_TRUE
D;JNE

@IF_FALSE
0;JMP

(IF_TRUE)

@0
D = A

@ARG
A = D + M // compute the base addr + index, aka target addr
D = M      // get the target val

@SP
M = M + 1   // increment SP ahead of time
A = M - 1
M = D      // place the value where SP was originally pointing at

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

(IF_FALSE)

@0
D = A

@ARG
A = D + M // compute the base addr + index, aka target addr
D = M      // get the target val

@SP
M = M + 1   // increment SP ahead of time
A = M - 1
M = D      // place the value where SP was originally pointing at

@2
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

@RET_FROM_MAIN.FIBONACCI_14
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

@MAIN.FIBONACCI
0; JMP

(RET_FROM_MAIN.FIBONACCI_14)

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

@RET_FROM_MAIN.FIBONACCI_19
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

@MAIN.FIBONACCI
0; JMP

(RET_FROM_MAIN.FIBONACCI_19)

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

@4
D = A

@SP
A = M
M = D   // insert the constant

@SP
M = M + 1   // increment SP

@RET_FROM_MAIN.FIBONACCI_25
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

@MAIN.FIBONACCI
0; JMP

(RET_FROM_MAIN.FIBONACCI_25)

(WHILE)

@WHILE
0;JMP

