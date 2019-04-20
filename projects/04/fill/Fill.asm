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


(LOOP)
  // screen buffer goes from @SCREEN to @KBD
  @KBD
  D=A
  @CUR_SCREEN
  M=D

  // kbd state can change while writing to screen, so store in RAM
  @COLOR
  M=0
  @KBD
  D=M
  @FILL_SCREEN
  D;JEQ
  @COLOR
  M=!M

  (FILL_SCREEN)
    // check if we've written to the whole buffer
    @CUR_SCREEN
    D=M
    @SCREEN
    D=D-A
    @LOOP
    D;JLT

    @COLOR
    D=M
    @CUR_SCREEN
    M=M-1 // decrement
    A=M
    M=D

    @FILL_SCREEN
    0;JMP

@LOOP
0;JMP

