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
if_exp: "if" "(" value ")" "{" block "}" "else" "{" block "}"
      | "if" "(" value ")" value "else" value

_blockitem: line ";" | if_exp

?block: (_blockitem)*

fnblock: block

?line: value
     | val

val: "val" name "=" value

?value: atomic
     | application
     | _expression
     | pipe

?pipe: pipe ("|>" call)* 
    | atomic

call: value value*

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

?atomic: reference
      | nat
      | "(" value ")"
      | _lambda
      | string
      | list

list: "[" csv "]"

csv: (atomic ","?)*

_lambda: lambda_exp | lambda_block
      
lambda_exp: "@" locals "." term
lambda_block: "@" locals "." "{" fnblock "}"

term: value
      
reference: name

nat: /[0-9]+/

?application: atomic (value)*

?name: /(?!^def$)[A-Za-z_]+/

locals: local+
local: /[A-Za-z]/

string: ESCAPED_STRING

%import common.WS
%ignore WS
%import common.ESCAPED_STRING
"""

parser = Lark(grammar,parser="earley")
