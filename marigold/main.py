from parser import parser
from compiler import Compiler
from lambdas import *
import sys
import click

sys.setrecursionlimit(1000000)

def main():
    with open('src/main.mg') as f:
        tree = parser.parse(f.read())

        print(tree.pretty())

        c = Compiler().transform(tree)

        print("\nCode to run:",c)

        print('-'*10,'OUTPUT','-'*10)

        exec(c)

if __name__ == '__main__':
    main()