// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)


(MULT)
  // set R2 to 0
  @R2
  M=0
(MULT_LOOP)
  // check if R0 is 0
  @R0
  D=M
  @END
  D;JLE
  // decrement R0
  @R0
  M=M-1
  // add R1 to R2
  // and store in R2
  @R1
  D=M
  @R2
  M=D+M
  // loop back to start
  @MULT_LOOP
  0;JMP
(END)
  @END
  0;JMP


