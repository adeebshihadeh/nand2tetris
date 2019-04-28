#!/usr/bin/env python3
import sys

# simple assembler for hack asm

def str_int(n):
  return str(int(n))

# remove any irrelevant junk
def sanitize(asm):
  ret = list()
  for l in asm:
    l = l.strip()
    l = l.split("//")[0] # strip comments
    if not len(l): continue # ignore blank lines
    if "(" in l: continue # ignore labels for now
    ret.append(l.strip())
  return ret

# hack asm to binary
def assemble(asm):
  ret = list()
  for i in sanitize(asm):
    if "@" in i: # a instruction
      # TODO: handle symbols
      if i[i.index("@")+1].isalpha():
        continue
      else: # constant
        val = int(i.split("@")[1])
      ret.append("0" + bin(val)[2:].zfill(15))
    else: # c instruction
      a = "1" if "=" in i and "M" in i[i.index("=")+1:] else "0"

      comp = "000000"
      if "=" in i or ";" in i:
        # no need to distinguish between A and M for these bits
        eq = i.split("=")[-1].split(";")[0].replace("M", "A")

        # TODO: make c2, c4, & c6 cleaner
        comp = ""
        comp += str_int("D" not in eq) # zero x
        comp += str_int(not (eq == "0" or ("D" in eq and len(eq) <= 2) or
                        eq == "D-1" or "+A" in eq or "-D" in eq or "&" in eq))
        comp += str_int("A" not in eq) # zero y
        comp += str_int(eq == "1" or "+1" in eq or eq == "A-D" or eq == "D-1" or
                        "|" in eq or ("D" in eq and len(eq) <= 2))
        comp += str_int("+" in eq or "-" in eq or eq.isdigit())
        comp += str_int("|" in eq or "!" in eq or "+1" in eq or eq == "1" or
                        "-A" in eq or "-D" in eq)

      dest = "".join([str_int("=" in i and n in i.split("=")[0]) for n in "ADM"])

      jmp = {"GT": "001", "EQ": "010", "GE": "011", "LT": "100", "NE": "101",
              "LE": "110", "MP": "111"}.get(i.split(";J")[-1], "000")

      ret.append("111" + a + comp + dest + jmp)
  return ret

if __name__ == "__main__":
    if len(sys.argv) < 2:
      print(f"usage: {sys.argv[0]} add.asm")
      exit(-1)

    asm = open(sys.argv[1]).readlines()
    for l in assemble(asm):
      print(l)

