#!/usr/bin/env python3

import os
import sys

class Parser:
  C_ARITHMETIC = 0
  C_PUSH = 1
  C_POP = 2
  C_LABEL = 3
  C_GOTO = 4
  C_IF = 5
  C_FUNCTION = 6
  C_RETURN = 7
  C_CALL = 8

  def __init__(self, fn):
    # remove empty lines & lines with only comments
    self.src = [l for l in open(fn).readlines() if len(l.strip()) and not l.strip().startswith("//")]
    self.cur_line = -1

  def advance(self):
    self.cur_line += 1

  def parse(self):
    arg1 = None
    arg2 = None

    # arg1 not used for C_RETURN
    # arg2 only used if cmd is C_PUSH, C_POP, C_FUNCTON, or C_CALL

    l = self.src[self.cur_line].strip().split(" ")
    if l[0] in ("add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"):
      cmd_type = self.C_ARITHMETIC
      arg1 = l[0]
    elif l[0] in ("push", "pop"):
      cmd_type = self.C_PUSH if l[0] == "push" else self.C_POP
      arg1 = l[1]
      arg2 = int(l[2])
    else:
      raise Exception("NOT IMPLEMENTED: " + repr(l[0]))

    return cmd_type, arg1, arg2

  def hasMoreCommands(self):
    return self.cur_line < (len(self.src) - 1)


class CodeWriter:
  DEC_SP = "@SP\nM=M-1\n"
  INC_SP= "@SP\nM=M+1\n"
  POP_INTO_D = "%sA=M\nD=M\n" % DEC_SP
  POP_INTO_A = "%sA=M\nA=M\n" % DEC_SP
  PUSH_D = "@SP\nA=M\nM=D\n%s" % INC_SP

  def __init__(self):
    self.fn = None
    self.to_write = ""
    self.cond_cnt = 0

  def setFileName(self, fn):
    self.fn = fn
    self.to_write = ""
    self.cond_cnt = 0

  def close(self):
    open(self.fn, "w").write(self.to_write)
    self.to_write = ""
    self.cond_cnt = 0

  def writeArithmetic(self, cmd):
    ret = ""

    # pop operand off stack
    ret += self.POP_INTO_D

    if cmd == "neg":
      ret += "D=-D\n"
    elif cmd == "not":
      ret += "D=!D\n"
    else:
      # pop another operand off the stack
      ret += self.POP_INTO_A

      # do the operation and store in D reg
      if cmd == "add":
        ret += "D=D+A\n"
      elif cmd == "sub":
        ret += "D=A-D\n"
      elif cmd == "and":
        ret += "D=D&A\n"
      elif cmd == "or":
        ret += "D=D|A\n"
      else:
        cond = {"eq": "JEQ", "gt": "JGT", "lt": "JLT"}.get(cmd)

        ret += "D=A-D\n"

        # TODO: clean this up
        ret += "@COND_TRUE_%d\n" % self.cond_cnt
        ret += "D;%s\n" % cond
        ret += "D=0\n" # 0 is false
        ret += "@COND_END_%d\n" % self.cond_cnt
        ret += "0;JMP\n"
        ret += "(COND_TRUE_%s)\n" % self.cond_cnt
        ret += "D=-1\n" # -1 is true
        ret += "(COND_END_%d)\n" % self.cond_cnt

        self.cond_cnt += 1

    # push result onto stack
    ret += self.PUSH_D

    self.to_write += ret  + "\n\n" # two newlines for debugging

  def writePushPop(self, cmd, seg, idx):
    ret = ""

    if seg == "constant":
      assert cmd != Parser.C_POP
      ret += "@%d\n" % idx
      ret += "D=A\n"
      ret += self.PUSH_D
    else:
      if seg in ("temp", "pointer", "static"):
        offset = {"temp": 5, "pointer": 3, "static": 16}.get(seg)
        ret += "@R%d\n" % (idx + offset)

        # HACK: make this cleaner
        ret += "D=A\n@XXX\nM=D\n"
      else:
        # optimize and skip this if idx is 0?
        ret += "@%d\n" % idx
        ret += "D=A\n"

        s = {"local": "LCL", "this": "THIS", "that": "THAT", "argument": "ARG"}.get(seg)
        ret += "@%s\n" % s
        ret += "D=M+D\n"
        ret += "@XXX\n"
        ret += "M=D\n"

      if cmd == Parser.C_POP:
        ret += self.POP_INTO_D
        ret += "@XXX\nA=M\n"
        ret += "M=D\n"
      else:
        ret += "@XXX\nA=M\n"
        ret += "D=M\n"
        ret += self.PUSH_D

    self.to_write += ret + "\n\n" # two newlines for debugging


def translate(in_fn, out_fn):
  p = Parser(in_fn)
  cw = CodeWriter()

  cw.setFileName(out_fn)

  while p.hasMoreCommands():
    p.advance()
    cmd, arg1, arg2 = p.parse()

    if cmd == Parser.C_ARITHMETIC:
      cw.writeArithmetic(arg1)
    elif cmd in (Parser.C_PUSH, Parser.C_POP):
      cw.writePushPop(cmd, arg1, arg2)
    else:
      raise NotImplementedError

  cw.close()

if __name__ == "__main__":
  if len(sys.argv) != 2:
    print("\tusage: %s program.vm" % sys.argv[0])
    exit(0)

  translate(sys.argv[1], sys.argv[1].replace(".vm", ".asm"))

