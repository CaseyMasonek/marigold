def main():
    from marigold.parser import parser
    from marigold.compiler import Compiler
    from marigold.lcode import lambdacode
    import sys

    with open(sys.argv[1]) as f:
        tree = parser.parse(f.read())

        print(tree.pretty())

        c = Compiler('./' + sys.argv[1]).transform(tree)

        print("\nCode to run:",c)

        print('-'*10,'OUTPUT','-'*10)

        namespace = {}
        exec(lambdacode, namespace) 
        exec(c, namespace)