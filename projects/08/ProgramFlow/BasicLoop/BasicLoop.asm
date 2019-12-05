@0
D=A
@SP
A=M
M=D
@SP
M=M+1


@0
D=A
@LCL
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


(LOOP_START)


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


@0
D=A
@LCL
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


@0
D=A
@LCL
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
@LOOP_START
D;JNE


@0
D=A
@LCL
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


