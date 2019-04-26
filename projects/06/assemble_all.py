#!/usr/bin/env python3
from subprocess import check_output

# assemble all hack assembly files found and save them to current dir

if __name__ == "__main__":
  af = check_output("find * | grep .asm", shell=True).decode().split("\n")[:-1]
  for f in af:
    ff = f.replace(".asm", ".hack").split("/")[-1]
    try:
      print(f"assembling {f}")
      check_output(f"./assembler.py {f} > {ff}", shell=True)
    except:
      pass

