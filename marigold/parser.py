from lark import Lark, v_args, Transformer, Visitor

grammar = r"""
# Top level rule
start: item* 

?item: module
     | normalitem

?normalitem: block # A block of code
           | function # A function
           | _recursive_function -> recursive_function # A recursive function
           | if_exp # Or an if statement
           | comment
           | unpack

comment: "#" /[^#]/* "#" 

import_exp: "import" name ";"

# Modules contain module items
module: "module" name "{" moduleitem* "}"

?moduleitem: mval
           | comment
           | mfunc
           | mrfunc
           | munpack

mval: name "=" value ";"
mfunc: "def" name "(" args? ")" "{" fnblock "}" 
mrfunc: "defr" name "(" args ")" "{" fnblock "}" 
munpack: "unpack" name ";"


# Functions
function: "def" name "(" args? ")" "{" fnblock "}" 
_recursive_function: "defr" name "(" args ")" "{" fnblock "}"

?args: /[a-zA-Z_,]+/

# If statements
if_exp: "if" "(" value ")" (value|pblock) elif_exp* "else" (value|pblock)
elif_exp: "elif" "(" value ")" (value|pblock)
unpack: "unpack" name ";"

# Code blocks
?block: (_blockitem)*
_blockitem: line ";" | if_exp | comment
?pblock: "{" block "}"
fnblock: block

?line: guard
     | value
     | val
     | valchange


# Varible assignment
val: name "=" value
?valchange: addeq | subeq | muleq | diveq | pipeeq | modeq

# Atomics
?atomic: reference
      | nat
      | "(" value ")"
      | _lambda
      | string
      | list
      | hashmap
      | pair

pair: "(" atomic "," atomic ")"
hashmap: "{" (string ":" atomic (","|"}"))+

guard: "guard" "(" value ")" value

# Values
?value: atomic
     | application
     | _expression
     | pipeline

# Pipelines
pipeline: value (pipe)+
pipe: "|" atomic atomic*

call: value value*

# Expressions/operators
_expression: add | sub | mul | div | lt | gt | eq | ne | and_exp | or_exp | succ | pred 
           | atomic | mod | not_exp

add: atomic "+" atomic
sub: atomic "-" atomic
mul: atomic "*" atomic
div: atomic "//" atomic
mod: atomic "%" atomic
lt : atomic "<" atomic
lte: atomic "<=" atomic
gt : atomic ">" atomic
gte: atomic ">=" atomic
eq : value "==" value
ne : atomic "!=" atomic
and_exp: value "&&" atomic
or_exp: value "||" atomic
not_exp: "!" value
succ: atomic "++"
pred: atomic "--"
concat: atomic "<>" atomic

addeq: name "+=" atomic
subeq: name "-=" atomic
muleq: name "*=" atomic
diveq: name "//=" atomic
modeq: name "%=" atomic
pipeeq: name "|=" atomic*

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
reference: /(?!(elif|unpack|import)\b)[A-Za-z_.]+/
?application: (value)* atomic

# Common/misc
?name: /[A-Za-z_]+/

string: ESCAPED_STRING

%import common.WS
%ignore WS
%import common.ESCAPED_STRING
%ignore " "
"""

parser = Lark(grammar,parser="earley")
