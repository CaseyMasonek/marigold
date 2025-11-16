# Booleans
TRUE = lambda a: lambda b: a
FALSE = lambda a: lambda b: b

true = lambda a: lambda b: a
false = lambda a: lambda b: b

def encode_bool(b):
    return TRUE if b else FALSE

def decode_bool(l):
    return l == TRUE

# Boolean operators
NOT = lambda b: b(FALSE)(TRUE)
AND = lambda a: lambda b: a(b)(FALSE)
OR = lambda a: lambda b: a(TRUE)(b)

# Numbers
ZERO = lambda f: lambda x: x
ONE = lambda f: lambda x: f(x)
SUCC = lambda n: lambda f: lambda x: f(n(f)(x))

TWO = SUCC(ONE)
THREE = SUCC(TWO)
FOUR = SUCC(THREE)

def encode_int(i):
    count = ZERO

    for _ in range(i):
        count = SUCC(count)

    return count

def decode_int(l):
    try:
        return l(lambda n: n + 1)(0)
    except:
        return l
    
# Arithmetic
ADD = lambda a: lambda b: a(SUCC)(b)
MULT = lambda a: lambda b: a(lambda x: b(SUCC)(x))(ZERO)

# Pairs
PAIR = lambda h: lambda t: lambda f: f(h)(t)
FIRST = lambda p: p(TRUE)
SECOND = lambda p: p(FALSE)

def encode_pair(t):
    return PAIR(encode_int(t[0]))(encode_int(t[1]))

def decode_pair(p):
    return decode_int(FIRST(p)),decode_int(SECOND(p))

SHIFT_AND_INCREMENT = lambda p: PAIR(SECOND(p))(SUCC(SECOND(p))) # for pred
PRED = lambda n: FIRST(n(SHIFT_AND_INCREMENT)(PAIR(ZERO)(ZERO)))
SUB = lambda a: lambda b: b(PRED)(a)

# Basic conditions
ISZERO = lambda n: n(lambda _: FALSE)(TRUE)
EQ = lambda a: lambda b: AND(ISZERO(SUB(a)(b)))(ISZERO(SUB(b)(a)))
LT =  lambda a: lambda b: AND(ISZERO(SUB(a)(b)))(NOT(ISZERO(SUB(b)(a))))
GT =  lambda a: lambda b: AND(NOT(ISZERO(SUB(a)(b))))(ISZERO(SUB(b)(a)))
LTE = lambda a: lambda b: ISZERO(SUB(a)(b))
GTE = lambda a: lambda b: ISZERO(SUB(b)(a))

# Fixed point combinator
Z = lambda f: (lambda x: f(lambda v: x(x)(v)))(lambda x: f(lambda v: x(x)(v)))

# Pair lists
PNIL = PAIR(TRUE)(TRUE)
PISNIL = FIRST
PCONS = lambda h: lambda t: PAIR(FALSE)(PAIR(h)(t))
PHEAD = lambda l: FIRST(SECOND(l))
PTAIL = lambda l: SECOND(SECOND(l))

PSUM = Z(lambda f: lambda l: (
    PISNIL(l)
    (lambda _: ZERO)
    (lambda _: ADD(PHEAD(l))(f(PTAIL(l))))
    (PNIL)
))

PLEN = Z(lambda f: lambda l: (
    PISNIL(l)
    (lambda _: ZERO)
    (lambda _: SUCC(f(PTAIL(l))))
    (PNIL) # dummy value
))

PRANGE = lambda n: Z(lambda f: lambda x: (
    ISZERO(x)
    (lambda _: NIL)
    (lambda _: CONS(SUB(n)(x))(f(PRED(x))))
    (NIL)
))(n)

PINDEX = lambda l: lambda n: PHEAD(n(PTAIL)(l))

def encode_plist(l):
    if not l:
        return PNIL
    first = encode_int(l[0])
    return PCONS(first)(encode_plist(l[1:]))

def decode_plist(l):
    return Z(lambda f: lambda x: (
        PISNIL(x)
        (lambda _: [])
        (lambda _: [decode_int(PHEAD(x))] + f(PTAIL(x)))
        (PNIL)
    ))(l)

# Right fold lists
NIL = FALSE
CONS = lambda h: lambda t: lambda f: lambda x: f(h)(t(f)(x))
ISNIL = lambda l: l(lambda h: lambda t: FALSE) (TRUE)
LEN = lambda l: l(lambda h:(lambda r: SUCC(r))) (ZERO)
SUM = lambda l: l(lambda h: lambda r: ADD(r)(h))(ZERO)
HEAD = lambda l: l(lambda h: lambda r: h) (FALSE)
TAIL = lambda l: lambda c: lambda n: l(lambda h: lambda r: lambda g: g(h)(r(c))) (lambda _: n) (FALSE)

TO_LIST = Z(lambda f: lambda l: (
    PISNIL(l)
    (lambda _: NIL)
    (lambda _: CONS(PHEAD(l))(f(PTAIL(l))))
    (NIL)
))

RANGE = lambda n: Z(lambda f: lambda x: (
    ISZERO(x)
    (lambda _: NIL)
    (lambda _: CONS(SUB(n)(x))(f(PRED(x))))
    (NIL)
))(n)

INDEX = lambda l: lambda i: HEAD(i(TAIL)(l))

REVERSE = lambda l: RANGE(LEN(l))(lambda h: lambda r: (CONS(INDEX(l)(SUB(PRED(LEN(l)))(h)))(r)))(NIL)

FOLD = lambda l: lambda f: lambda x: REVERSE(REVERSE(l)(f)(x))

MAP = lambda l: lambda f: l(lambda h: lambda r: CONS(f(h))(r))(NIL)

FILTER = lambda l: lambda c: l(lambda h: lambda r: (c(h)(CONS(h)(r))(r)))(NIL)

UPDATE = lambda l: lambda i: lambda v: RANGE(LEN(l))(lambda h: lambda r: EQ(h)(i)(CONS(v)(r))(CONS(INDEX(l)(h))(r)))(NIL)

SAME = lambda a: lambda b: MAP(RANGE(LEN(a)))(lambda i: EQ(INDEX(a)(i))(INDEX(b)(i)))(lambda h: lambda r: h(r)(FALSE))(TRUE)

GETINDEX = lambda l: lambda i: Z(lambda f: lambda x: (
    EQ(HEAD(x))(i)
    (lambda _: ZERO)
    (lambda _: SUCC(f(TAIL(x)))
    ))(NIL)
)(l)

def encode_list(l):
    if not l:
        return NIL
    first = encode_int(l[0])
    return CONS(first)(encode_list(l[1:]))

def decode_list(l):
    return l(lambda h: lambda acc: [decode_int(h)] + acc)([])

def decode_nested_list(l):
    return decode_other_list(l,decode_list)

def decode_nested_nested_list(l):
    return(decode_other_list(l,decode_nested_list))

def decode_other_list(l,decoder):
    return l(lambda h: lambda acc: [decoder(h)] + acc)([])

# Modulo and floor division

MODSLOW = ( # First mod idea I came up with, but it's really slow
    lambda a: lambda b: EQ(a)(b)(ZERO)(
    Z(lambda f: lambda x:
        LT(x)(b)
        (lambda _: x)
        (lambda _: f(SUB(x)(b)))
        (NIL)
    )(a)
))

MOD = lambda a: lambda b: SECOND(
    a(lambda p:
        EQ(SECOND(p))(PRED(b))
        (PAIR(SUCC(FIRST(p)))(ZERO))
        (PAIR(FIRST(p))(SUCC(SECOND(p))))
    )
(PAIR(ZERO)(ZERO)))



DIV = lambda a: lambda b: FIRST(
    a(lambda p:
        EQ(SECOND(p))(PRED(b))
        (PAIR(SUCC(FIRST(p)))(ZERO))
        (PAIR(FIRST(p))(SUCC(SECOND(p))))
    )
(PAIR(ZERO)(ZERO)))

FACTORIAL = Z(lambda f: lambda n: (
    ISZERO(n)
    (lambda _: ONE)
    (lambda _: MULT(n)(f(PRED(n))))
    (NIL)
))

def encode_str(s):
    l = []
    for char in s:
        l.append(ord(char))
    return encode_list(l)

def decode_str(s):
    l = decode_list(s)
    s = ""
    for i in l:
        s += chr(i)
    return s

TEN = lambda f: lambda x: f(f(f(f(f(f(f(f(f(x)))))))))

HASHFN = lambda s: MOD(SUM(s))(TEN)

HASH = TEN(lambda r: CONS(NIL)(r))(NIL)

GETBUCKET = lambda h: lambda k: INDEX(h)(HASHFN(k))

GET = lambda h: lambda k: (
    SECOND(INDEX(FILTER(GETBUCKET(h)(k))(lambda p: SAME(FIRST(p))(k)))(ZERO))
)

EXISTS = lambda h: lambda k: (
    ISNIL(INDEX(FILTER(GETBUCKET(h)(k))(lambda p: SAME(FIRST(p))(k)))(ZERO))
)

PUT = lambda h: lambda k: lambda v: UPDATE(h)( # Update the hash
    HASHFN(k) # At the index of hash(k)
)(
    CONS( # To be a list of
        PAIR(k)(v) # A pair with the key and value  
    )(
        GETBUCKET(h)(k) # And the rest of the bucket
    )
)

REPLACEMENT_INDEX = lambda h: lambda k: Z(lambda f: lambda x:(
    SAME(FIRST(HEAD(x)))(k)
    (lambda _: ZERO)
    (lambda _: SUCC(f(TAIL(x))))
    (NIL)
))(GETBUCKET(h)(k))

REPLACE = lambda h: lambda k: lambda v: UPDATE(h)(
    HASHFN(k)
)(
    UPDATE(GETBUCKET(h)(k))
    (REPLACEMENT_INDEX(h)(k))
    (PAIR(k)(v))
)

SET = lambda h: lambda k: lambda v: (
    EQ(GET(h)(k))(ONE)
    (PUT(h)(k)(v))
    (REPLACE(h)(k)(v))
)

def encode_hash(d):
    h = HASH
    for k,v in d.items:
        h = PUT(h)(k)(v)
    return h

def decode_hash(x,decode_key=decode_str,decode_value=decode_int):
    d = {}
    l = decode_other_list(x,lambda l: decode_other_list(l,lambda p: (decode_key(FIRST(p)),decode_value(SECOND(p)))))
    
    for i in l:
        for j in i:
            d.update({j[0]:j[1]})
            
    return d

def putint(i):
    print(decode_int(i))

def askint(s):
    return encode_int(int(input(decode_str(s))))

def put(s):
    print(decode_str(s))

def ask(s):
    return encode_str(input(decode_str(s)))

def putbool(b):
    print(decode_bool(b))

def puthash(h):
    print(decode_hash(h))

def putlist(l):
    print(decode_list(l))