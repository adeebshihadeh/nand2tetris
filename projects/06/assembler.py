#!/usr/bin/env python3
import sys

# simple assembler for hack asm

def str_int(n):
  return str(int(n))

def build_symbol_table(asm):
  ret = {"SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4, "SCREEN": 16384,
          "KBD": 24576}
  ret.update({("R" + str(n)): n for n in range(16)})
  labels = [l.split("(")[1].split(")")[0] for l in asm if "(" in l]

  idx, addr = 0, 16
  for i in asm:
    if "(" in i:
      ret[i.split("(")[1].split(")")[0]] = idx
    else:
      if "@" in i and not i[i.index("@")+1].isdigit():
        sym = i.split("@")[1]
        if sym not in ret and sym not in labels:
          ret[sym] = addr
          addr += 1
      idx += 1
  return ret

# hack asm to binary
def assemble(asm):
  # sanitize asm input for comments, whitespace, etc.
  asm = [l.strip().split("//")[0] for l in asm]
  asm = list(filter(lambda x : len(x), asm))
  st = build_symbol_table(asm)

  ret = list()
  for i in asm:
    # skip label lines
    if "(" in i: continue

    if "@" in i: # a instruction
      if not i[i.index("@")+1].isdigit():
        val = st[i.split("@")[1]]
      else: # constant
        val = int(i.split("@")[1])
      ret.append("0" + bin(val)[2:].zfill(15))
    else: # c instruction
      a = "1" if "=" in i and "M" in i[i.index("=")+1:] else "0"

      comp = "000000"
      if "=" in i or ";" in i:
        # no need to distinguish between A and M for these bits
        eq = i.split("=")[-1].split(";")[0].replace("M", "A")

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

