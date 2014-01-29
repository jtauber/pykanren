# LISP-like cons structures

def cons(a, b):
    return (a, b)

def is_cons(c):
    return isinstance(c, tuple) and len(c) == 2

def car(c):
    return c[0]

def cdr(c):
    return c[1]


# helper function for creating nested cons out of lists

def l(*lst):
    if len(lst) == 1:
        return cons(lst[0], ())
    if len(lst) == 2:
        return cons(*lst)
    else:
        return cons(lst[0], l(*lst[1:]))


# same as I did with minikanren
#
# (var c) becomes var(c)
# (var? x) becomes isinstance(x, var)
# (var=? x_1 x_2) becomes x_1 == x_2

class var:
    def __init__(self, index):
        self.index = index

    def __eq__(self, other):
        return isinstance(other, var) and self.index == other.index

    def __hash__(self):
        return hash(self.index)

    def __repr__(self):
        return "<%s>" % self.index

def is_var(v):
    return isinstance(v, var)


# this also stays the same as the python for minikanren, using a dictionary
# for substitutions

def walk(u, s):
    if isinstance(u, var):
        a = s.get(u)
        if a:
            return walk(a, s)
        else:
            return u
    else:
        return u


def ext_s(x, v, s):
    s = s.copy()
    s[x] = v
    return s


# again, unify stays the same as the python for minikanren

def unify(u, v, s):
    u = walk(u, s)
    v = walk(v, s)
    if is_var(u) and is_var(v) and u == v:
        return s
    elif is_var(u):
        return ext_s(u, v, s)
    elif is_var(v):
        return ext_s(v, u, s)
    elif is_cons(u) and is_cons(v):
        s = unify(car(u), car(v), s)
        t = unify(cdr(u), cdr(v), s)
        return t if t is not False else s
    elif u == v:
        return s
    else:
        return False


# for now we're going to treat mzero as () and (unit x) as (x, ())

def eq(u, v):
    def goal(state):
        s = unify(u, v, car(state))
        if s is not False:
            return ((s, cdr(state)), ())
        else:
            return ()

    return goal


def call_fresh(f):
    def goal(state):
        c = state[1]
        return f(var(c))((car(state), c + 1))

    return goal


EMPTY_STATE = cons({}, 0)


def mplus(stream1, stream2):
    if stream1 == ():
        return stream2
    elif callable(stream1):
        return lambda: mplus(stream2, stream1())
    else:
        return cons(car(stream1), mplus(cdr(stream1), stream2))


def bind(stream, goal):
    if stream == ():
        return ()
    elif callable(stream):
        return lambda: bind(stream(), goal)
    else:
        return mplus(goal(car(stream)), bind(cdr(stream), goal))


def disj(goal_1, goal_2):
    def goal(state):
        return mplus(goal_1(state), goal_2(state))
    return goal


def conj(goal_1, goal_2):
    def goal(state):
        return bind(goal_1(state), goal_2)
    return goal


if __name__ == "__main__":

    s1 = {var(0): 5, var(1): True}
    s2 = {var(1): 5, var(0): var(1)}

    assert walk(var(0), s1) == 5
    assert walk(var(0), s2) == 5

    assert unify(None, 1, {}) == False
    assert unify(None, var(0), {}) == {var(0): None}
    assert unify(None, [1, var(0)], {}) == False
    assert unify(1, None, {}) == False
    assert unify(1, 1, {}) == {}
    assert unify(1, 2, {}) == False
    assert unify(1, var(0), {}) == {var(0): 1}
    assert unify(1, [], {}) == False
    assert unify(var(0), 1, {}) == {var(0): 1}
    assert unify(var(0), var(1), {}) == {var(0): var(1)}
    assert unify(var(0), [], {}) == {var(0): []}
    assert unify(var(0), l(1, 2, 3), {}) == {var(0): l(1, 2, 3)}
    assert unify(l(1, 2, 3), l(1, 2, 3), {}) == {}
    assert unify(l(1, 2, 3), l(3, 2, 1), {}) == False
    assert unify(l(var(0), var(1)), l(1, 2), {}) == {var(0): 1, var(1): 2}
    assert unify(l(l(1, 2), l(3, 4)), l(l(1, 2), l(3, 4)), {}) == {}
    assert unify(l(l(var(0), 2), l(3, 4)), l(l(1, 2), l(3, 4)), {}) == {var(0): 1}

    assert unify((1, (2, (3, 4))), (1, (2, var(0))), {}) == {var(0): (3, 4)}

    assert unify({}, {}, {}) == {}

    assert eq(1,1)(EMPTY_STATE) == (EMPTY_STATE, ())
    assert eq(1,2)(EMPTY_STATE) == ()

    assert call_fresh(lambda q: eq(q, 5))(EMPTY_STATE) == (({var(0): 5}, 1), ())

    assert EMPTY_STATE == ({}, 0)

    assert conj(
        call_fresh(lambda a: eq(a, 7)),
        call_fresh(lambda b: disj(eq(b, 5), eq(b, 6)))
    )(EMPTY_STATE) == (({var(0): 7, var(1): 5}, 2), (({var(0): 7, var(1): 6}, 2), ()))
