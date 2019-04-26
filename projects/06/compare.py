#!/usr/bin/env python3
import sys

# compare two hack files for debugging assembler output

def print_row(a, b):
  print("|".join([i.ljust(2) for i in a])  + "\t\t" + "|".join([i.ljust(2) for i in b]))

if __name__ == "__main__":
  if len(sys.argv) < 3:
    print(f"usage: {sys.argv[0]} add.hack add2.hack")
    exit(-1)

  f1 = open(sys.argv[1]).readlines()
  f2 = open(sys.argv[2]).readlines()

  a = ["i", "x", "x", "a", "c1", "c2", "c3", "c4", "c5",
        "c6", "d1", "d2", "d3", "j1", "j2", "j3"]

  # print header
  print_row(a, a)
  print_row(["=="]*len(a), ["=="]*len(a))

  for i, j in zip(f1, f2):
    print_row(i.strip(), j.strip())

  comp = {}
  for i, (j, jj) in enumerate(zip(zip(*f1), zip(*f2))):
    if i >=  16: continue
    comp[a[i]] = int(j == jj) if a[i] not in comp else int(j == jj)*comp[a[i]]

  for k, v in comp.items():
    if not v:
      print(k, bool(v))

