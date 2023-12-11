@111
D = A

@SP
A = M
M = D   // insert the constant

@SP
M = M + 1   // increment SP

@333
D = A

@SP
A = M
M = D   // insert the constant

@SP
M = M + 1   // increment SP

@888
D = A

@SP
A = M
M = D   // insert the constant

@SP
M = M + 1   // increment SP

@SP
M = M - 1   // decrement the pointer
A = M
D = M

@StaticTest.8
M = D                    


@SP
M = M - 1   // decrement the pointer
A = M
D = M

@StaticTest.3
M = D                    


@SP
M = M - 1   // decrement the pointer
A = M
D = M

@StaticTest.1
M = D                    


@StaticTest.3
D = M

@SP
A = M
M = D   // insert the constant

@SP
M = M + 1   // increment SP

@StaticTest.1
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

@StaticTest.8
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
D = M + D    // add two operands 

@SP
M = M + 1   // Increment the SP (ahead of time)
A = M - 1   // insert the result to where SP used to point at
M = D

(infinite_loop)
@infinite_loop
0; JMP