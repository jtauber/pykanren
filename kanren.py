class Var:
    def __init__(self, symbol):
        self.symbol = symbol
    
    def __eq__(self, other):
        return isinstance(other, Var) and self.symbol == other.symbol
    
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
    elif isinstance(v, list):
        if len(v) == 0:
            return False
        elif len(v) == 1:
            return occurs_check(x, v[0], s)
        else:
            return occurs_check(x, v[0], s) or occurs_check(x, v[1:], s)
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
    elif isinstance(u, list) and isinstance(v, list):
        if len(u) != len(v):
            return False
        elif len(u) == 1 and len(v) == 1:
            return unify(u[0], v[0], s)
        else:
            s = unify(u[0], v[0], s)
            if s is False:
                return False
            else:
                return unify(u[1:], v[1:], s)
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
    elif isinstance(u, list) and isinstance(v, list):
        if len(u) != len(v):
            return False
        elif len(u) == 1 and len(v) == 1:
            return unify_no_check(u[0], v[0], s)
        else:
            s = unify_no_check(u[0], v[0], s)
            if s is False:
                return False
            else:
                return unify_no_check(u[1:], v[1:], s)
    elif u == v:
        return s
    else:
        return False


def walk_star(v, s):
    v = walk(v, s)
    if isinstance(v, Var):
        return v
    if isinstance(v, list):
        return [walk_star(v[0], s)] if len(v) == 1 else [walk_star(v[0], s)] + walk_star(v[1:], s)
    else:
        return v


def reify_name(n):
    return "_%s" % n


def reify_s(v, s):
    v = walk(v, s)
    if isinstance(v, Var):
        return extend_s(v, reify_name(len(s)), s)
    elif isinstance(v, list):
        return reify_s(v[0], s) if len(v) == 1 else reify_s(v[1:], reify_s(v[0], s))
    else:
        return s


def reify(v, s):
    v = walk_star(v, s)
    return walk_star(v, reify_s(v, {}))


def eq(u, v):
    def goal(a):
        s = unify(u, v, a)
        if s is False:
            return []
        else:
            return [s]
    return goal


def eq_no_check(u, v):
    def goal(a):
        s = unify_no_check(u, v, a)
        if s is False:
            return []
        else:
            return [s]
    return goal
