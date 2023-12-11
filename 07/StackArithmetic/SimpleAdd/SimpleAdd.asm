@7
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

