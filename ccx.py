# coding: utf-8

import sys
import re
import os
import operator

import ccxdata
# import expand

# UTILITY_DIR = "c:/home/cc-utility/"
UTILITY_DIR = "/Users/noriok/cc-utility/"

def get_utility_code(tokenset, defset):
  r = []

  utils = [nm for nm in os.listdir(UTILITY_DIR) if not nm.endswith("~")]

  b = True
  while b:
    b = False
    for name in utils:
      if name in tokenset and name not in defset:
        b = True
        f = open(UTILITY_DIR + name)
        lines = f.readlines()
        f.close()
        tokenset.update(get_tokenset(lines))
        defset.update([name])

        # 参照するコード定義の前にコードを追加しなければならない
        r.insert(0, "".join(lines).strip())
        r.insert(1, "\n")

  return r
    
#  for uname in [nm for nm in os.listdir(UTILITY_DIR) if not nm.endswith("~")]:
#    # utility codeの中で、別のutility codeを参照することもある。
#    # 全てのutilityの名前が解決するまで繰り返す
#    if uname in tokenset and uname not in defset:
#      f = open(UTILITY_DIR + uname)
#      # r.append("".join(f.readlines()).strip())
#      r.append(f.read().strip())
#      r.append("¥n")
#      f.close()
#  return r

def error(msg): # [fix]
  # エラーは、コードの先頭に入れておいて、g++のコンパイルエラーとして表示する
  sys.stderr.write(msg + '¥n')
  sys.exit(1)

#def get_fun_declr(lines): # return set
def get_defs(lines):
  # function declaration
  re_defun = re.compile("^[a-zA-Z][:_a-z<>,A-Z0-9 ]* ([a-zA-Z0-9_ ]+)\(.*(,|{)$")
  # class declaration
  re_defclass = re.compile("^class ([a-zA-Z0-9_]+).+{$")

  defset = set([])
  for s in lines:
    if s[0] in " }#\n": continue
    n = s.find("//")
    if n != -1:
      # 関数定義を探しているのだから、//が文字列の中かどうか気にする必要なし
      s = s[:n].rstrip()
    m = re_defun.match(s)
    if m:
      defset.add(m.group(1))
    m = re_defclass.match(s)
    if m:
      defset.add(m.group(1))

  return defset

def required_headers(tokenset):
  hs = set(["iostream"])
  for tok in ccxdata.header_name_map:
    if tok in tokenset:
      h = ccxdata.header_name_map[tok]
      if h.endswith(".h"):
        h = "c" + h[:-2]
      hs.add(h)
  return hs

def required_typedef(tokenset): # [fix]
  r = []
  if "vi" in tokenset:
    r.append(["vector<int>", "vi", ["vector"]])
  if "vs" in tokenset:
    r.append(["vector<string>", "vs", ["vector", "string"]])

  if "uint" in tokenset:
    r.append(["unsigned int", "uint", []])
  if "ull" in tokenset:
    r.append(["unsigned long long", "ull", []])
  if "ll" in tokenset:
    r.append(["long long", "ll", []])

  return r

def main(lines):
  # remove:  #include ...
  #          using ...
  #          typedef ...
  #          (empty line)
  while lines and (lines[0].startswith("#include") or
                   lines[0].startswith("#define") or
                   lines[0].startswith("using") or
                   lines[0].startswith("typedef") or
                   lines[0] == "\n"):
    lines.pop(0)

  tokenset = get_tokenset(lines)

  code = get_utility_code(tokenset, get_defs(lines))
  code.extend(lines)

  # code = expand.expand(code)

  # tokenset = get_tokenset(code)

  header_set = required_headers(tokenset)

  # return tuple list (3 elements)
  # (original, alias, header-list)
  typedef_list = required_typedef(tokenset)
  for header_list in map(operator.itemgetter(2), typedef_list):
    for h in header_list:
      header_set.add(h)
  
  # output
  for h in sorted(header_set):
    print "#include <%s>" % h
  print "using namespace std;"
  
  if "de" in tokenset:
    print "#define de(a) cout << #a << ':' << (a) << endl"
  if "de2" in tokenset:
    print "#define de2(a,b) cout << #a << ':' << (a) << ' ' << #b << ':' << (b) << endl"
  if "de3" in tokenset:
    print "#define de3(a,b,c) cout << #a << ':' << (a) << ' ' << #b << ':' << (b) << ' ' << #c << ':' << (c) << endl"
  if "For" in tokenset:
    print "#define For(i,x) for (int i=0; i<(int)(x); i++)"
#  if "FOR" in tokenset:
#    print "#define FOR(i,a,b) for (int i=(a); i<(int)(b); i++)"
#  if "For1" in tokenset:
#    print "#define For1(i, x) for (int i = 1; i <= (int)(x); i++)"
  if "each" in tokenset:
    print "#define each(p,v) for (__typeof((v).end()) p=(v).begin();p!=(v).end();++p)"
  if "PI" in tokenset:
    print "#define PI (2 * acos(0))"
#  if "deb" in tokenset:
#    print "#define deb(...) fprintf(stderr, __VA_ARGS__)"
#  if "Size" in tokenset:
#    print "#define Size(a) sizeof(a) / sizeof(a[0])"
  if "mp" in tokenset:
    print "#define mp make_pair"
#  if "cfor" in tokenset:
#    print "#define cfor(c,s) for (int i_=0,c=s[0]; c != 0; c=s[++i_])"
#  if "clr" in tokenset:
#    print "#define clr(a) memset(a,0,sizeof(a))"
  if "max3" in tokenset:
    print "#define max3(a,b,c) max(a,max(b,c))"
  if "max4" in tokenset:
    print "#define max4(a,b,c,d) max(a,max(b,max(c,d)))"
#  if "max5" in tokenset:
#    print "#define max5(a,b,c,d,e) max(a,max(b,max(c,max(d,e))))"
  if "min3" in tokenset:
    print "#define min3(a,b,c) min(a,min(b,c))"
  if "min4" in tokenset:
    print "#define min4(a,b,c,d) min(a,min(b,min(c,d)))"
#  if "min5" in tokenset:
#    print "#define min5(a,b,c,d,e) min(a,min(b,min(c,min(d,e))))"
#  if "LOWERCASE" in tokenset:
#    print '#define LOWERCASE "abcdefghijklmnopqrstuvwxyz"'
#  if "UPPERCASE" in tokenset:
#    print '#define UPPERCASE "ABCDEFGHIJKLMNOPQRSTUVWXYZ"'
  print

  if typedef_list:
    for original, alias, _ in typedef_list:
      print "typedef %s %s;" % (original, alias)
    print

  for s in code:
    s = s.rstrip()
    if s.startswith("#include") or s.startswith("using"):
      assert False, s
    print s

def get_tokenset(lines):
  s = "¥n".join(lines)
  r = []
  for token in re.findall("[a-zA-Z0-9_]+", s):
    r.append(token)

  return set(r)

if __name__ == "__main__":
  if len(sys.argv) == 1:
    main(sys.stdin.readlines())
  else:
    f = open(sys.argv[1])
    main(f.readlines())
    f.close()
