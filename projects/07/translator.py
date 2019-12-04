#!/usr/bin/env python3

import os
import sys

# VM translator, .vm -> .asm

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
    # TODO: better input sanitizing?
    # sanitize vm input. remove empty lines & lines with only comments
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
    if l[0] in ["add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"]:
      cmd_type = self.C_ARITHMETIC
      arg1 = l[0]
    elif l[0] in ["push", "pop"]:
      cmd_type = self.C_PUSH if l[0] == "push" else self.C_POP
      arg1 = l[1]
      arg2 = int(l[2])
    else:
      raise Exception("NOT IMPLEMENTED: " + repr(l[0]))

    return cmd_type, arg1, arg2

  def hasMoreCommands(self):
    return self.cur_line < (len(self.src) - 1)


class CodeWriter:

  # snippets
  SP_DEC = "@SP\nM=M-1\n"
  SP_INC= "@SP\nM=M+1\n"

  def __init__(self):
    self.fn = None
    self.to_write = ""

  def setFileName(self, fn):
    self.fn = fn
    self.to_write = ""

  def close(self):
    open(self.fn, "w").write(self.to_write)
    self.to_write = ""

  def writeArithmetic(self, cmd):
    ret = ""

    # add
    ret += self.SP_DEC
    ret += "A=M\n"
    ret += "D=M\n"
    ret += self.SP_DEC
    ret += "A=M\n"
    ret += "A=M\n"

    ret += "D=D+A\n"

    ret += "@SP\n"
    ret += "A=M\n"
    ret += "M=D\n"
    ret += self.SP_INC

    self.to_write += ret  + "\n\n" # two newlines for debugging
    return ret

  def writePushPop(self, cmd, seg, idx):
    ret = ""

    # push a constant
    ret += "@" + str(idx) + "\n"
    ret += "D=A\n"
    ret += "@SP\n"
    ret += "A=M\n"
    ret += "M=D\n"
    ret += self.SP_INC

    self.to_write += ret + "\n\n" # two newlines for debugging
    #return ret


def translate(in_fn, out_fn):
  p = Parser(in_fn)
  cw = CodeWriter()

  cw.setFileName(out_fn)

  while p.hasMoreCommands():
    p.advance()
    cmd, arg1, arg2 = p.parse()

    if cmd == Parser.C_ARITHMETIC:
      cw.writeArithmetic(p.src[p.cur_line])
    elif cmd in [Parser.C_PUSH, Parser.C_POP]:
      cw.writePushPop(cmd, arg1, arg2)
    else:
      raise NotImplementedError

  cw.close()

if __name__ == "__main__":

  if len(sys.argv) != 2:
    print("\tusage: %s <code.vm or dir_with_dotvm_files/>" % sys.argv[0])
    exit(0)

  arg = sys.argv[1]

  # TODO: accept a dir instead of file
  translate(arg, arg.replace(".vm", ".asm"))


