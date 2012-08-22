# comments in this file referring to minikanren are specifically to
#     http://kanren.cvs.sourceforge.net/kanren/kanren/mini/mk.scm
# which is the implementation used in the 2nd printing of The Reasoned Schemer


# minikanren implements this as a scheme vector
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
#
# note: this appears in Byrd's thesis but not minikanren source
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
        # slightly simpler than minikanren because of dicts and .get()
        a = s.get(v)
        if a:
            return walk(a, s)
        else:
            return v
    else:
        return v


# ext-s has no corresponding function as we can just do s[x] = v


def unify(u, v, s):
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


def ext_s_check(x, v, s):
    if occurs_check(x, v, s):
        return False
    else:
        s[x] = v
        return s


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


def unify_check(u, v, s):
    u = walk(u, s)
    v = walk(v, s)
    if id(u) == id(v):
        return s
    elif isinstance(u, Var):
        if isinstance(v, Var):
            s[u] = v
            return s
        else:
            return ext_s_check(u, v, s)
    elif isinstance(v, Var):
        return ext_s_check(v, u, s)
    elif isinstance(u, list) and isinstance(v, list):
        if len(u) != len(v):
            return False
        elif len(u) == 1 and len(v) == 1:
            return unify_check(u[0], v[0], s)
        else:
            s = unify_check(u[0], v[0], s)
            if s is False:
                return False
            else:
                return unify_check(u[1:], v[1:], s)
    elif u == v:
        return s
    else:
        return False


def walk_star(v, s):
    v = walk(v, s)
    if isinstance(v, Var):
        return v
    # minikanren actually tests for a pair but we'll support lists
    if isinstance(v, list):
        # the special casing of len(v) == 1 is one case where it's more
        # complex in python than in the original
        return [walk_star(v[0], s)] if len(v) == 1 else [walk_star(v[0], s)] + walk_star(v[1:], s)
    else:
        return v


def reify_s(v, s):
    v = walk(v, s)
    if isinstance(v, Var):
        s[v] = reify_name(len(s))
        return s
    # minikanren actually tests for a pair but we'll support lists
    elif isinstance(v, list):
        # the special casing of len(v) == 1 is one case where it's more
        # complex in python than in the original
        return reify_s(v[0], s) if len(v) == 1 else reify_s(v[1:], reify_s(v[0], s))
    else:
        return s


def reify_name(n):
    return "_%s" % n


def reify(v, s):
    v = walk_star(v, s)
    # we just use {} for minikanren's empty-s
    return walk_star(v, reify_s(v, {}))


# @@@ work in progress from this point on


# This assumes a literal translation of the streams in minikanren as a pair of
# item and function returning the rest of the stream, so the stream of numbers
# 1, 2, 3 is (1, lambda: (2, lambda: 3)). The return value is similarly a
# Scheme-like (1, (2, (3,))) for the list [1, 2, 3].
# This will change to be more Pythonic once I work out how to change
# everything else that is based on this approach.
def map_inf(n, p, a_inf):
    if not a_inf:
        return ()
    elif not (isinstance(a_inf, tuple) and callable(a_inf[1])):
        return (p(a_inf),)
    else:
        if n is None:
            return (p(a_inf[0]), map_inf(n, p, a_inf[1]()))
        elif n > 1:
            return (p(a_inf[0]), map_inf(n - 1, p, a_inf[1]()))
        else:
            return (p(a_inf[0]),)


from itertools import islice, imap


# here's a pythonic version
# it assumes a_inf is an iterable and returns a list
def pythonic_map_inf(n, p, a_inf):
    return list(islice(imap(p, a_inf), n))


# chains two streams
def mplus(a_inf, f):
    if not a_inf:
        return f()
    elif not (isinstance(a_inf, tuple) and callable(a_inf[1])):
        return (a_inf, f)
    else:
        return (a_inf[0], lambda: mplus(a_inf[1](), f))


# interleaves two streams
def mplusi(a_inf, f):
    if not a_inf:
        return f()
    elif not (isinstance(a_inf, tuple) and callable(a_inf[1])):
        return (a_inf, f)
    else:
        return (a_inf[0], lambda: mplusi(f(), a_inf[1]))


def bind(a_inf, g):
    if not a_inf:
        return False
    elif not (isinstance(a_inf, tuple) and callable(a_inf[1])):
        return g(a_inf)
    else:
        return mplus(g(a_inf[0]), lambda: bind(a_inf[1](), g))


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
        s = unify(u, v, a)
        if s is False:
            return []
        else:
            return [s]
    return goal
