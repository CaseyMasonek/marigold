from lark import Lark, v_args, Transformer, Visitor

grammar = r"""
# Top level rule
start: item*

?item: module # An item is either a module
     | moduleitem # OR an item in a module

# Modules contain module items
module: "module" name "{" moduleitem* "}"

# Module items are either 
?moduleitem: block # A block of code
           | function # A function
           | recursive_function # A recursive function
           | if_exp # Or an if statement

# Functions
function: "def" name "(" args? ")" "{" fnblock "}" 
recursive_function: "defr" name "(" args ")" "{" fnblock "}"

?args: /[a-zA-Z_,]+/

# If statements
if_exp: "if" "(" value ")" (value|pblock) "else" (value|pblock)

# Code blocks
?block: (_blockitem)*
_blockitem: line ";" | if_exp
?pblock: "{" block "}"
fnblock: block

?line: value
     | val

# Varible assignment
val: "val" name "=" value

# Atomics
?atomic: reference
      | nat
      | "(" value ")"
      | _lambda
      | string
      | list

# Values
?value: atomic
     | application
     | _expression
     | pipe

# Pipelines
?pipe: pipe ("|>" call)* 
    | atomic

call: value value*

# Expressions/operators
_expression: add | sub | mul | div | lt | gt | eq | ne

add: atomic "+" atomic
sub: atomic "-" atomic
mul: atomic "*" atomic
div: atomic "/" atomic
lt : atomic "<" atomic
lte: atomic "<=" atomic
gt : atomic ">" atomic
gte: atomic ">=" atomic
eq : atomic "==" atomic
ne : atomic "!=" atomic

# Datatypes
list: "[" csv "]"
csv: (atomic ","?)*
nat: /[0-9]+/

# Lambdas
_lambda: lambda_exp | lambda_block
lambda_exp: "@" locals "." term
lambda_block: "@" locals "." "{" fnblock "}"
term: value
locals: local+
local: /[A-Za-z]/

# Other
reference: name
?application: atomic (value)*

# Common/misc
?name: /(?!^def$)[A-Za-z_]+/

string: ESCAPED_STRING

%import common.WS
%ignore WS
%import common.ESCAPED_STRING
"""

parser = Lark(grammar,parser="earley")
