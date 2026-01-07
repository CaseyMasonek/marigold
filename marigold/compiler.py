from lark import Transformer, v_args, exceptions, Tree, Token
from builtins import *    

def gen_nat_code(n):
    codestr = f"encode_int({n})"

    return codestr

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

def gen_pipe_code(pipes,val):
    if len(pipes) == 0:
        return val
    
    pipe = pipes[-1]

    codestr = f"({pipe["fn"]})({gen_pipe_code(pipes[:-1],val)})"

    for arg in pipe["args"]:
        codestr += f"(({arg}))"

    return codestr

@v_args(inline=True)
class Compiler(Transformer):
    def __init__(self):
        self.variables = {}

    def comment(self,*_):
        return ""

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

    def start(self,*items):
        #print(items)

        if type(items) == tuple:
            return "\n".join(items)

        return "\n".join(items.children).strip()

    def module(self,name,*items):
        name = name[::]

        for item in items:
            self.variables[name + "." + item["name"]] = item["value"]

            if item["name"] == "Cons":
                self.variables[name] = item["value"]

        return ""

    def mval(self,name,value):
        return {'type':'mval',"name":name[::],'value':value}
    
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

        return {'type':'mfunc','name':name,'value':term}

    def fnblock(self,lines):
        return lines.split("\n")[-1]
    
    def guard(self,condition,val):
        return {"type":"guard","condition":condition,"val":val}
    
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

    def recursive_function(self,name,arg,block):
        term = f"""(Z(lambda self: lambda {arg}: {block}))"""

        self.variables[name.value] = term

        return ""

    def inner_rec(self,name,arg,block):
        term = f"""(Z(lambda self: lambda {arg}: {block}))"""

        name = name[::]

        return {"name":name,"term":term}
    
    def if_exp(self,value,then,*rest):
        otherwise = rest[-1]
        elifs = rest[:-1]

        codestr = f"((({value})(lambda _: {then})"

        else_part = otherwise
        
        for elif_exp in reversed(elifs):
            c,v = elif_exp
            else_part = f"(({c})(lambda _: {v})(lambda _: {else_part})(NIL))"
        
        codestr += "(lambda _:" + else_part + ")"

        codestr += ")(NIL))"

        return codestr
    
    def elif_exp(self,condition,value):
        return (condition,value)
    
    def add(self,a,b):
        #print(a,b)

        return f"(ADD ({a}) ({b}))"
    
    def sub(self,a,b):
        #print(f"(SUB {a} {b})")
        return f"(SUB ({a}) ({b}))"
    
    def mul(self,a,b):
        return f"(MULT ({a}) ({b}))"

    def div(self,a,b):
        return f"(DIV ({a}) ({b}))"
    
    def mod(self,a,b):
        return f"(MOD ({a}) ({b}))"

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
    
    def and_exp(self,a,b):
        return f"(AND({a})({b}))"
    
    def or_exp(self,a,b):
        return f"(OR({a})({b}))"
    
    def not_exp(self,a):
        return f"(NOT({a}))"

    def succ(self,a):
        return f"(SUCC({a}))"
    
    def pred(self,a):
        return f"(PRED({a}))"
    
    def addeq(self,name,value):
        self.variables[name.value] = f"(ADD({self.variables[name.value]})({value}))"

        return ""
    
    def subeq(self,name,value):
        self.variables[name.value] = f"(SUB({self.variables[name.value]})({value}))"

        return ""
    
    def muleq(self,name,value):
        self.variables[name.value] = f"(MULT({self.variables[name.value]})({value}))"

        return ""

    def diveq(self,name,value):
        self.variables[name.value] = f"(DIV({self.variables[name.value]})({value}))"

        return ""
    
    def modeq(self,name,value):
        self.variables[name.value] = f"(MOD({self.variables[name.value]})({value}))"

        return ""
    
    def pipeeq(self,name,*values):
        first = values[0]
        varval = self.variables[name.value]

        codestr = f"(({first})({varval})"

        for value in values[1:]:
            codestr += f"({value})"
        
        codestr += ")"

        self.variables[name.value] = codestr

        return ""
    
    def nil(self):
        return "(NIL)"
    
    def true(self):
        return "(TRUE)"
    
    def false(self):
        return "(FALSE)"

    def string(self,s):
        return gen_str_code(s)

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
    
    def pipeline(self,val,*pipes):
        #print(val)
        pipes = list(pipes)

        return gen_pipe_code(pipes,val)

    def pipe(self,fn,*args):
        if type(fn) == Token:
            fn = fn.value

        return {
            "fn":fn,
            "args":args
        }

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