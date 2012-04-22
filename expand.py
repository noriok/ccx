# coding: sjis

# from itertools import *
import re
import sys

# �R�}���h�͕K��1�s�B���̍s�ɂ̓R�}���h�ȊO�̏��͑��݂��Ȃ�(����̂̓R�}���h�����̂�)

def expand_for(arg):
  brace = ""
  if arg[-1] == "{":
    arg.pop()
    brace = " {"

  n = len(arg)
  if n == 1:
    var = "i"
    end = arg[0]
  elif n == 2:
    var = arg[0]
    end = arg[1]
  else:
    assert False

  if end.endswith(".size()"):
    end = "(int)" + end

  return "for (int %s = 0; %s < %s; %s++)%s" % (var, var, end, var, brace)

def expand(lines):
  write = sys.stdout.write
  re_for = re.compile("( +)for ([^(].*)$")

  r = []
  for s in lines:
    m = re_for.match(s)
    if m:
      indent = m.group(1)
      r.append(indent + expand_for(m.group(2).split()))
      continue

    # more command ...


    # not exist command
    r.append(s.rstrip())

  return r

if __name__ == "__main__":
  # import doctest
  # doctest.testmod()
  pass
