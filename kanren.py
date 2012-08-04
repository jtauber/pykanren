class Var:
    def __init__(self, symbol):
        self.symbol = symbol
    
    def __eq__(self, other):
        return self.symbol == other.symbol
    
    def __hash__(self):
        return hash(self.symbol)
    
    def __repr__(self):
        return "<%s>" % self.symbol


empty_s = {}
s1 = {Var("x"): 5, Var("y"): True}
s2 = {Var("y"): 5, Var("x"): Var("y")}


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


assert lookup(Var("x"), s1) == 5
assert lookup(Var("x"), s2) == Var("y")


def walk(v, s):
    if isinstance(v, Var):
        a = s.get(v)
        if a:
            return walk(a, s)
        else:
            return v
    else:
        return v


assert walk(Var("x"), s1) == 5
assert walk(Var("x"), s2) == 5


def occurs_check(x, v, s):
    v = walk(v, s)
    if isinstance(v, Var):
        return v == x
    # we don't need the pair check yet
    else:
        return False


s3 = {Var("x"): Var("y")}
assert occurs_check(Var("y"), Var("x"), s3) == True
assert occurs_check(Var("y"), 5, s3) == False
assert occurs_check(Var("x"), Var("x"), {}) == True


def extend_s(x, v, s):
    if occurs_check(x, v, s):
        return False
    else:
        s[x] = v
        return s


assert extend_s(Var("y"), Var("x"), s3) == False
assert extend_s(Var("y"), 5, s3) == {Var("y"): 5, Var("x"): Var("y")}
assert extend_s(Var("x"), Var("x"), {}) == False


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


assert unify(None, 1, {}) == False
assert unify(None, Var("x"), {}) == {Var("x"): None}
assert unify(1, None, {}) == False
assert unify(1, 1, {}) == {}
assert unify(1, 2, {}) == False
assert unify(1, Var("x"), {}) == {Var("x"): 1}
assert unify(Var("x"), 1, {}) == {Var("x"): 1}
assert unify(Var("x"), Var("y"), {}) == {Var("x"): Var("y")}


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


assert unify_no_check(None, 1, {}) == False
assert unify_no_check(None, Var("x"), {}) == {Var("x"): None}
assert unify_no_check(1, None, {}) == False
assert unify_no_check(1, 1, {}) == {}
assert unify_no_check(1, 2, {}) == False
assert unify_no_check(1, Var("x"), {}) == {Var("x"): 1}
assert unify_no_check(Var("x"), 1, {}) == {Var("x"): 1}
assert unify_no_check(Var("x"), Var("y"), {}) == {Var("x"): Var("y")}
