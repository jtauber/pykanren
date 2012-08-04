class Var:
    def __init__(self, symbol):
        self.symbol = symbol
    
    def __eq__(self, other):
        return self.symbol == other.symbol
    
    def __hash__(self):
        return hash(self.symbol)
    
    def __repr__(self):
        return "<%s>" % self.symbol


# more idiomatic would be:
#     return s.get(v, v) if isinstance(v, Var) else v
# but this parallels walk below better
def lookup(v, s):
    if isinstance(v, Var):
        a = s.get(v)
        if a:
            return a
        else:
            return v
    else:
        return v


def walk(v, s):
    if isinstance(v, Var):
        a = s.get(v)
        if a:
            return walk(a, s)
        else:
            return v
    else:
        return v


def occurs_check(x, v, s):
    v = walk(v, s)
    if isinstance(v, Var):
        return v == x
    # we don't need the pair check yet
    else:
        return False


def extend_s(x, v, s):
    if occurs_check(x, v, s):
        return False
    else:
        s[x] = v
        return s


def unify(u, v, s):
    u = walk(u, s)
    v = walk(v, s)
    if id(u) == id(v):
        return s
    elif isinstance(u, Var):
        if isinstance(v, Var):
            s[u] = v
            return s
        else:
            return extend_s(u, v, s)
    elif isinstance(v, Var):
        return extend_s(v, u, s)
    # we don't need the pair check yet (???)
    elif u == v:
        return s
    else:
        return False


def unify_no_check(u, v, s):
    u = walk(u, s)
    v = walk(v, s)
    if id(u) == id(v):
        return s
    elif isinstance(u, Var):
        s[u] = v
        return s
    elif isinstance(v, Var):
        s[v] = u
        return s
    # we don't need the pair check yet (???)
    elif u == v:
        return s
    else:
        return False
