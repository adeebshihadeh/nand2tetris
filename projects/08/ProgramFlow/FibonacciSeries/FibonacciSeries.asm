@1
D=A
@ARG
D=M+D
@XXX
M=D
@XXX
A=M
D=M
@SP
A=M
M=D
@SP
M=M+1


@R4
D=A
@XXX
M=D
@SP
M=M-1
A=M
D=M
@XXX
A=M
M=D


@0
D=A
@SP
A=M
M=D
@SP
M=M+1


@0
D=A
@THAT
D=M+D
@XXX
M=D
@SP
M=M-1
A=M
D=M
@XXX
A=M
M=D


@1
D=A
@SP
A=M
M=D
@SP
M=M+1


@1
D=A
@THAT
D=M+D
@XXX
M=D
@SP
M=M-1
A=M
D=M
@XXX
A=M
M=D


@0
D=A
@ARG
D=M+D
@XXX
M=D
@XXX
A=M
D=M
@SP
A=M
M=D
@SP
M=M+1


@2
D=A
@SP
A=M
M=D
@SP
M=M+1


@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
A=M
D=A-D
@SP
A=M
M=D
@SP
M=M+1


@0
D=A
@ARG
D=M+D
@XXX
M=D
@SP
M=M-1
A=M
D=M
@XXX
A=M
M=D


(MAIN_LOOP_START)


@0
D=A
@ARG
D=M+D
@XXX
M=D
@XXX
A=M
D=M
@SP
A=M
M=D
@SP
M=M+1


@SP
M=M-1
A=M
D=M
@COMPUTE_ELEMENT
D;JNE


@END_PROGRAM
0;JMP


(COMPUTE_ELEMENT)


@0
D=A
@THAT
D=M+D
@XXX
M=D
@XXX
A=M
D=M
@SP
A=M
M=D
@SP
M=M+1


@1
D=A
@THAT
D=M+D
@XXX
M=D
@XXX
A=M
D=M
@SP
A=M
M=D
@SP
M=M+1


@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
A=M
D=D+A
@SP
A=M
M=D
@SP
M=M+1


@2
D=A
@THAT
D=M+D
@XXX
M=D
@SP
M=M-1
A=M
D=M
@XXX
A=M
M=D


@R4
D=A
@XXX
M=D
@XXX
A=M
D=M
@SP
A=M
M=D
@SP
M=M+1


@1
D=A
@SP
A=M
M=D
@SP
M=M+1


@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
A=M
D=D+A
@SP
A=M
M=D
@SP
M=M+1


@R4
D=A
@XXX
M=D
@SP
M=M-1
A=M
D=M
@XXX
A=M
M=D


@0
D=A
@ARG
D=M+D
@XXX
M=D
@XXX
A=M
D=M
@SP
A=M
M=D
@SP
M=M+1


@1
D=A
@SP
A=M
M=D
@SP
M=M+1


@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
A=M
D=A-D
@SP
A=M
M=D
@SP
M=M+1


@0
D=A
@ARG
D=M+D
@XXX
M=D
@SP
M=M-1
A=M
D=M
@XXX
A=M
M=D


@MAIN_LOOP_START
0;JMP


(END_PROGRAM)

