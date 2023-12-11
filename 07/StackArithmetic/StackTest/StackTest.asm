@17
D = A

@SP
A = M
M = D   // insert the constant

@SP
M = M + 1   // increment SP

@17
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

@eq_2
D; JEQ

@SP         // 'not equal' portion
M = M + 1   // Increment the SP (ahead of time)
A = M - 1   // insert the result to where SP used to point at
M = 0       // false is 0

@next_2
0; JMP

(eq_2)
@SP         
M = M + 1   // Increment the SP (ahead of time)
A = M - 1   // insert the result to where SP used to point at
M = -1      // true is -1

(next_2) // so that when not equal, we can skip over (eq_2)

@17
D = A

@SP
A = M
M = D   // insert the constant

@SP
M = M + 1   // increment SP

@16
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

@eq_5
D; JEQ

@SP         // 'not equal' portion
M = M + 1   // Increment the SP (ahead of time)
A = M - 1   // insert the result to where SP used to point at
M = 0       // false is 0

@next_5
0; JMP

(eq_5)
@SP         
M = M + 1   // Increment the SP (ahead of time)
A = M - 1   // insert the result to where SP used to point at
M = -1      // true is -1

(next_5) // so that when not equal, we can skip over (eq_5)

@16
D = A

@SP
A = M
M = D   // insert the constant

@SP
M = M + 1   // increment SP

@17
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

@eq_8
D; JEQ

@SP         // 'not equal' portion
M = M + 1   // Increment the SP (ahead of time)
A = M - 1   // insert the result to where SP used to point at
M = 0       // false is 0

@next_8
0; JMP

(eq_8)
@SP         
M = M + 1   // Increment the SP (ahead of time)
A = M - 1   // insert the result to where SP used to point at
M = -1      // true is -1

(next_8) // so that when not equal, we can skip over (eq_8)

@892
D = A

@SP
A = M
M = D   // insert the constant

@SP
M = M + 1   // increment SP

@891
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

@lt_11
D; JLT

@SP         // 'not less than' portion
M = M + 1   // Increment the SP (ahead of time)
A = M - 1   // insert the result to where SP used to point at
M = 0       // false is 0

@next_11
0; JMP

(lt_11)
@SP         
M = M + 1   // Increment the SP (ahead of time)
A = M - 1   // insert the result to where SP used to point at
M = -1      // true is -1

(next_11) // so that when not equal, we can skip over (eq_11)

@891
D = A

@SP
A = M
M = D   // insert the constant

@SP
M = M + 1   // increment SP

@892
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

@lt_14
D; JLT

@SP         // 'not less than' portion
M = M + 1   // Increment the SP (ahead of time)
A = M - 1   // insert the result to where SP used to point at
M = 0       // false is 0

@next_14
0; JMP

(lt_14)
@SP         
M = M + 1   // Increment the SP (ahead of time)
A = M - 1   // insert the result to where SP used to point at
M = -1      // true is -1

(next_14) // so that when not equal, we can skip over (eq_14)

@891
D = A

@SP
A = M
M = D   // insert the constant

@SP
M = M + 1   // increment SP

@891
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

@lt_17
D; JLT

@SP         // 'not less than' portion
M = M + 1   // Increment the SP (ahead of time)
A = M - 1   // insert the result to where SP used to point at
M = 0       // false is 0

@next_17
0; JMP

(lt_17)
@SP         
M = M + 1   // Increment the SP (ahead of time)
A = M - 1   // insert the result to where SP used to point at
M = -1      // true is -1

(next_17) // so that when not equal, we can skip over (eq_17)

@32767
D = A

@SP
A = M
M = D   // insert the constant

@SP
M = M + 1   // increment SP

@32766
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

@gt_20
D; JGT

@SP         // 'not greater than' portion
M = M + 1   // Increment the SP (ahead of time)
A = M - 1   // insert the result to where SP used to point at
M = 0       // false is 0

@next_20
0; JMP

(gt_20)
@SP         
M = M + 1   // Increment the SP (ahead of time)
A = M - 1   // insert the result to where SP used to point at
M = -1      // true is -1

(next_20) // so that when not equal, we can skip over (eq_20)

@32766
D = A

@SP
A = M
M = D   // insert the constant

@SP
M = M + 1   // increment SP

@32767
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

@gt_23
D; JGT

@SP         // 'not greater than' portion
M = M + 1   // Increment the SP (ahead of time)
A = M - 1   // insert the result to where SP used to point at
M = 0       // false is 0

@next_23
0; JMP

(gt_23)
@SP         
M = M + 1   // Increment the SP (ahead of time)
A = M - 1   // insert the result to where SP used to point at
M = -1      // true is -1

(next_23) // so that when not equal, we can skip over (eq_23)

@32766
D = A

@SP
A = M
M = D   // insert the constant

@SP
M = M + 1   // increment SP

@32766
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

@gt_26
D; JGT

@SP         // 'not greater than' portion
M = M + 1   // Increment the SP (ahead of time)
A = M - 1   // insert the result to where SP used to point at
M = 0       // false is 0

@next_26
0; JMP

(gt_26)
@SP         
M = M + 1   // Increment the SP (ahead of time)
A = M - 1   // insert the result to where SP used to point at
M = -1      // true is -1

(next_26) // so that when not equal, we can skip over (eq_26)

@57
D = A

@SP
A = M
M = D   // insert the constant

@SP
M = M + 1   // increment SP

@31
D = A

@SP
A = M
M = D   // insert the constant

@SP
M = M + 1   // increment SP

@53
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

@112
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

@SP
A = M - 1   // don't decrement SP, bc it will be the same in the end
M = -M

@SP
AM = M - 1   // decrement sp, and get the top operand   
D = M       

@SP
AM = M - 1   // decrement sp, and get the bottom operand   
D = D & M    // AND two operands

@SP
M = M + 1   // Increment the SP (ahead of time)
A = M - 1   // insert the result to where SP used to point at
M = D

@82
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
D = D | M    // OR two operands

@SP
M = M + 1   // Increment the SP (ahead of time)
A = M - 1   // insert the result to where SP used to point at
M = D

@SP
A = M - 1   // don't decrement SP, bc it will be the same in the end
M = !M

(infinite_loop)
@infinite_loop
0; JMP