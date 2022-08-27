// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
//
// This program only needs to handle arguments that satisfy
// R0 >= 0, R1 >= 0, and R0*R1 < 32768.

// initialise R2 0
@R2
M=0

// count = R1
@R1
D=M
@count
M=D

(LOOP)
// check if count is equal to 0
@count
D=M
@END
D;JEQ

// add R0 to R2
@R0
D=M
@R2
M=M+D

// decrease count by 1
@count
M=M-1

// return to start of loop
@LOOP
0;JMP

// end of program
(END)
@END
0;JMP
