// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

(START)

// get KBD and initialise screen output value
@KBD
D=M
@value
M=0

// set screen value to black if KBD is not zero
@KBD_IS_ZERO
D;JEQ
@value
M=-1
(KBD_IS_ZERO)

// initialise index and address
@count
M=0
@SCREEN
D=A
@address
M=D

// loop over the screen registers and set all to value
(LOOP)
@value
D=M
@address
A=M
M=D

// increase address and count by 1
@address
M=M+1
@count
M=M+1

// jump to start if count is equal to 8192
@8192
D=A
@count
D=D-M
@START
D;JEQ

@LOOP
0;JMP


