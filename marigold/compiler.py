from lark import Transformer, v_args, exceptions, Tree, Token
from builtins import *

def debug(f):
    def inner(*args,**kwargs):
        code = f(*args,**kwargs)

        if type(code) != type(""):
            return code
        
        if (code.count("(") != code.count(")")):
            print(f,code.count("("),code.count(")"))
            print(code)

        return code

    return inner

@debug
def gen_nat_code(n):
    codestr = f"encode_int({n})"

    return codestr

@debug
def gen_str_code(s):
        code = ""

        s = s[1:-1]

        for char in s:
            n = gen_nat_code(ord(char))

            code += f"CONS({n})("
            
        code += "NIL"

        for _ in s:
            code += ")"

        return code

@debug
def gen_pipe_code(pipes,val):
    if len(pipes) == 0:
        return val
    
    pipe = pipes[-1]

    codestr = f"({pipe['fn']})({gen_pipe_code(pipes[:-1],val)})"

    for arg in pipe["args"]:
        codestr += f"({arg})"

    return codestr

@v_args(inline=True)
class Compiler(Transformer):
    def __init__(self):
        self.variables = {}
        self.mvars = {}

    @debug
    def munpack(self,module):
        modvars = self.variables.items()

        modvars = [(k.split(".")[1],v) for k,v in modvars if k.split(".")[0] == module and len(k.split(".")) > 1 and k.split(".")[1] != "Cons"]

        for name,val in modvars:
            print("!!!",name)
            self.mvars[name] = val

        return ""

    @debug
    def import_exp(self,module):
        path = "."

        m = module.split(".")
        path += "/".join(m) + ".mg"

        print(path)

        return ""

    @debug
    def comment(self,*_):
        return ""

    @debug
    def block(self, *items):
        if not items:
            return ""
        
        has_guards = any(isinstance(item, dict) and item.get("type") == "guard" for item in items)
        
        if not has_guards:
            return "\n".join(str(item) for item in items)
        
        lines = ""
        open_parens = 0
        
        for i, item in enumerate(items):
            if isinstance(item, dict) and item.get("type") == "guard":
                cond = item["condition"]
                val = item["val"]
                open_parens += 1
                lines += f"(({cond})(lambda _: {val})(lambda _: "
            else:
                lines += str(item)
                if i < len(items) - 1:
                    lines += "\n"
        
        while open_parens > 0:
            lines += "))(NIL)"
            open_parens -= 1
        
        return lines

    @debug
    def start(self,*items):
        #print(items)

        if type(items) == tuple:
            return "\n".join(items)

        return "\n".join(items.children).strip()
    
    @debug
    def unpack(self,module):
        modvars = self.variables.items()

        modvars = [(k.split(".")[1],v) for k,v in modvars if k.split(".")[0] == module and len(k.split(".")) > 1 and k.split(".")[1] != "Cons"]

        for name,val in modvars:
            print("!!!",name)
            self.variables[name] = val

        return ""

    def module(self,name,*items):
        name = name[::]

        for item in items:
            if type(item) == type(""):
                continue
            self.variables[name + "." + item["name"]] = item["value"]

            if item["name"] == "Cons":
                self.variables[name] = item["value"]

        self.mvars = {}

        return ""

    def mval(self,name,value):
        self.mvars[name.value] = value
        return {'type':'mval',"name":name[::],'value':value}
    
    @debug
    def mfunc(self,name,*rest):
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

        self.mvars[name.value] = term

        return {'type':'mfunc','name':name,'value':term}

    @debug
    def fnblock(self,lines):
        return lines.split("\n")[-1]
    
    @debug
    def guard(self,condition,val):
        return {"type":"guard","condition":condition,"val":val}
    
    @debug
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

    @debug
    def csv(self,*l):
        return l
    
    @debug
    def list(self,csv):
        codestr = "("

        for v in csv:
            codestr += f"CONS({v})("

        codestr += "NIL)"

        for v in csv:
            codestr += ')'


        return codestr;

    @debug
    def pair(self,a,b):
        return f"(PAIR({a})({b}))"

    def hashmap(self,*items):
        key = None
        h = "HASH"

        for item in items:
            if type(item) == type(tuple()):
                break
            if key == None:
                key = item[::]
            else:
                h = f"SET({h})({gen_str_code(key)})({item})"

        #print(h)

        return h

    @debug
    def recursive_function(self,name,arg,block):
        term = f"""(Z(lambda self: lambda {arg}: {block}))"""

        self.variables[name.value] = term

        return ""

    @debug
    def inner_rec(self,name,arg,block):
        term = f"""(Z(lambda self: lambda {arg}: {block}))"""

        name = name[::]

        return {"name":name,"term":term}
    
    @debug
    def if_exp(self,value,then,*rest):
        otherwise = rest[-1]
        elifs = rest[:-1]

        print(otherwise,elifs)

        otherwise = otherwise.strip()

        codestr = f"((({value})(lambda _: {then})"

        else_part = otherwise
        
        for elif_exp in reversed(elifs):
            c,v = elif_exp
            else_part = f"(({c})(lambda _: {v})(lambda _: {else_part})(NIL))"
        
        codestr += "(lambda _:" + else_part + ")"

        codestr += ")(NIL))"

        print(codestr)

        return codestr
    
    @debug
    def elif_exp(self,condition,value):
        return (condition,value)
    
    @debug
    def add(self,a,b):
        #print(a,b)

        return f"(ADD ({a}) ({b}))"
    
    @debug
    def sub(self,a,b):
        #print(f"(SUB {a} {b})")
        return f"(SUB ({a}) ({b}))"
    
    @debug
    def mul(self,a,b):
        return f"(MULT ({a}) ({b}))"

    @debug
    def div(self,a,b):
        return f"(DIV ({a}) ({b}))"
    
    @debug
    def mod(self,a,b):
        return f"(MOD ({a}) ({b}))"

    @debug
    def lt(self,a,b):
        return f"(LT ({a}) ({b}))"

    @debug
    def lte(self,a,b):
        return f"(LTE ({a}) ({b}))"

    @debug
    def gt(self,a,b):
        return f"(GT ({a}) ({b}))"
    
    @debug
    def gte(self,a,b):
        return f"(GTE ({a}) ({b}))"
    
    @debug
    def eq(self,a,b):
        return f"(EQ ({a}) ({b}))"
    
    @debug
    def ne(self,a,b):
        return f"(NOT (EQ ({a}) ({b})))"
    
    @debug
    def and_exp(self,a,b):
        return f"(AND({a})({b}))"
    
    @debug
    def or_exp(self,a,b):
        return f"(OR({a})({b}))"
    
    @debug
    def not_exp(self,a):
        return f"(NOT({a}))"

    @debug
    def succ(self,a):
        return f"(SUCC({a}))"
    
    @debug
    def pred(self,a):
        return f"(PRED({a}))"
    
    @debug
    def addeq(self,name,value):
        self.variables[name.value] = f"(ADD({self.variables[name.value]})({value}))"

        return ""
    
    @debug
    def subeq(self,name,value):
        self.variables[name.value] = f"(SUB({self.variables[name.value]})({value}))"

        return ""
    
    @debug
    def muleq(self,name,value):
        self.variables[name.value] = f"(MULT({self.variables[name.value]})({value}))"

        return ""

    @debug
    def diveq(self,name,value):
        self.variables[name.value] = f"(DIV({self.variables[name.value]})({value}))"

        return ""
    
    @debug
    def modeq(self,name,value):
        self.variables[name.value] = f"(MOD({self.variables[name.value]})({value}))"

        return ""
    
    @debug
    def pipeeq(self,name,*values):
        first = values[0]
        varval = self.variables[name.value]

        codestr = f"(({first})({varval})"

        for value in values[1:]:
            codestr += f"({value})"
        
        codestr += ")"

        self.variables[name.value] = codestr

        return ""
    
    @debug
    def nil(self):
        return "(NIL)"
    
    @debug
    def true(self):
        return "(TRUE)"
    
    @debug
    def false(self):
        return "(FALSE)"

    @debug
    def string(self,s):
        return gen_str_code(s)
    
    @debug
    def lambda_exp(self,locals,term):
        codestr = "("

        for local in locals.children: 
            localname = local.children[0].value

            codestr += f"lambda {localname}: "

        codestr += term.children[0]

        codestr += ")"

        return codestr
    
    @debug
    def lambda_block(self,locals,term):
        codestr = "("

        for local in locals.children: 
            localname = local.children[0].value

            codestr += f"lambda {localname}: "

        codestr += term

        codestr += ")"

        return codestr
    
    @debug
    def call(self,*items):
        return {
            "function": items[0],
            "args": items[1:]
        }
    
    @debug
    def pipeline(self,val,*pipes):
        #print(val)
        pipes = list(pipes)

        return gen_pipe_code(pipes,val)

    @debug
    def pipe(self,fn,*args):
        if type(fn) == Token:
            fn = fn.value

        return {
            "fn":fn,
            "args":args
        }

    @debug
    def application(self,function,value):
        return "(" + function + "(" +  value + "))"
    
    @debug
    def nat(self,num):
        n = int(num.value)

        return gen_nat_code(n)
        
    @debug
    def val(self,name,value):
        self.variables[name.value] = value

        return ""

    @debug
    def reference(self,name):
        if name.value in self.variables.keys():
            return self.variables[name.value]
        if name.value in self.mvars.keys():
            return self.mvars[name.value]
        return name