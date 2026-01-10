def main():
    from marigold.parser import parser
    from marigold.compiler import Compiler
    from marigold.lcode import lambdacode
    import sys
    import os

    if (sys.argv[1]) == "new":
        if (len(sys.argv) < 3):
            print("Missing required argument: project name")
            return

        project_dir = sys.argv[2]

        os.makedirs(project_dir, exist_ok=True)

        with open(project_dir + "/main.mg","w") as f:
            f.write('put "Hello, World!";')

        with open(project_dir + "/pkginfo.json","w") as f:
            f.write(f"""{{
    "packageName": "{project_dir}",
    "requirements": []
}}""")
        
        return


    with open(sys.argv[1]) as f:
        tree = parser.parse(f.read())
        
        if '-d' in sys.argv:
            print(tree.pretty())

        c = Compiler('./' + sys.argv[1]).transform(tree)
        
        if '-d' in sys.argv:
            print("\nCode to run:",c)

        if '-d' in sys.argv:
            print('-'*10,'OUTPUT','-'*10)

        namespace = {}
        exec(lambdacode, namespace) 
        exec(c, namespace)