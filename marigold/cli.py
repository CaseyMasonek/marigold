from parser import parser
from compiler import Compiler
from lambdas import *
import sys
import typer

app = typer.Typer()

sys.setrecursionlimit(1000000)

@app.command()
def run(path:str):
    with open(path) as f:
        tree = parser.parse(f.read())

        print(tree.pretty())

        c = Compiler(path).transform(tree)
        
        print("\nCode to run:",c)

        print('-'*10,'OUTPUT','-'*10)

        exec(c)

if __name__ == '__main__':
    app()