import fire
import os
from textp.parser import parse as parseDSL
from textp.parser import SemanticChecker,Evaluator

def parse(path):
  f = open(path, 'r')
  rawcode = f.read()
  print(rawcode,'\n')
  ast = parseDSL(rawcode)
  print(ast)
  SemanticChecker().visit(ast)
  Evaluator().evaluate(ast)
  return

if __name__ == '__main__':
  fire.Fire({
      'parse': parse
  })