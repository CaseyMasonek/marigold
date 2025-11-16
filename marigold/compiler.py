from lark import Transformer, v_args, exceptions, Tree
from builtins import *    

def gen_nat_code(n):
    codestr = "(lambda f: lambda x:"

    for _ in range(n):
        codestr += 'f('

    codestr += 'x'

    for _ in range(n):
        codestr += ')'

    codestr += ')'

    return codestr

@v_args(inline=True)
class Compiler(Transformer):
    def __init__(self,lang="python"):
        self.variables = {}
        self.lang = lang

    def anonfn(self,arg):
        match self.lang:
            case "python":
                return f"(lambda {arg}: "
            case "js":
                return f"({arg} => "

    def block(self,*items):
        return "\n".join(items)

    def start(self,*items):
        if type(items) == tuple:
            return "\n".join(items)

        return "\n".join(items.children)
    
    def module(self, name, block):
        return block

    def fnblock(self,lines):
        return lines.split("\n")[-1]
    
    def function(self,name,*rest):
        if len(rest) == 2:
            args,block = rest
        else:
            block = rest[0]
            args = ""

        term = "("

        if args == "":
            term += "(lambda _: "

        for arg in args.split(','):
            term += f"(lambda {arg}: "

        term += block + ")"

        if args == "":
            term += ")"

        for arg in args.split(','):
            term += f")"

        self.variables[name.value] = term

        return ""
    #eeffoc

    def csv(self,*l):
        return l
    
    def list(self,csv):
        codestr = "("

        for v in csv:
            codestr += f"CONS({v})("

        codestr += "NIL)"

        for v in csv:
            codestr += ')'


        return codestr;

    def recursive_function(self,name,arg,block):
        term = f"""(Z(lambda self: lambda {arg}: {block}))"""

        self.variables[name.value] = term

        return ""
    
    def if_exp(self,value,then,otherwise):
        return f"((({value})(lambda _: {then})(lambda _: {otherwise}))(NIL))"
    
    def add(self,a,b):
        print(a,b)

        return f"(ADD ({a}) ({b}))"
    
    def sub(self,a,b):
        print(f"(SUB {a} {b})")
        return f"(SUB ({a}) ({b}))"
    
    def mul(self,a,b):
        return f"(MULT ({a}) ({b}))"

    def div(self,a,b):
        return f"(DIV ({a}) ({b}))"

    def lt(self,a,b):
        return f"(LT ({a}) ({b}))"

    def lte(self,a,b):
        return f"(LTE ({a}) ({b}))"

    def gt(self,a,b):
        return f"(GT ({a}) ({b}))"
    
    def gte(self,a,b):
        return f"(GTE ({a}) ({b}))"
    
    def eq(self,a,b):
        return f"(EQ ({a}) ({b}))"
    
    def ne(self,a,b):
        return f"(NOT (EQ ({a}) ({b})))"

    def string(self,s):
        code = ""

        s = s[1:-1]

        for char in s:
            n = gen_nat_code(ord(char))

            code += f"CONS({n})("
            
        code += "NIL"

        for _ in s:
            code += ")"

        return code

    def lambda_exp(self,locals,term):
        codestr = "("

        for local in locals.children: 
            localname = local.children[0].value

            codestr += f"lambda {localname}: "

        codestr += term.children[0]

        codestr += ")"

        return codestr
    
    def lambda_block(self,locals,term):
        codestr = "("

        for local in locals.children: 
            localname = local.children[0].value

            codestr += f"lambda {localname}: "

        codestr += term

        codestr += ")"

        return codestr
    
    def call(self,*items):
        return {
            "function": items[0],
            "args": items[1:]
        }
    
    def pipe(self,value,call=None):
        if call == None:
            return value

        fn = call["function"]
        args = call["args"]

        codestr = f"(({fn})({value})"

        for arg in args:
            codestr += f"({arg})"

        codestr += ")"

        return codestr

    def application(self,function,value):
        return "(" + function + "(" +  value + "))"
    
    def nat(self,num):
        n = int(num.value)

        return gen_nat_code(n)
        
    def val(self,name,value):
        self.variables[name.value] = value

        return ""

    def reference(self,name):
        if name.value in self.variables.keys():
            return self.variables[name.value]
        return name