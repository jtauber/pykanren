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


# as with python for minikanren, there is no need for ext-s as
# (ext-s x v s) just becomes s[x] = v

# again, unify stays the same as the python for minikanren

def unify(u, v, s):
    u = walk(u, s)
    v = walk(v, s)
    if isinstance(u, var) and isinstance(v, var) and u == v:
        return s
    elif isinstance(u, var):
        s[u] = v
        return s
    elif isinstance(v, var):
        s[v] = u
        return s
    elif isinstance(u, list) and isinstance(v, list):
        # if we only implemented lists as cons, we could do
        # s = unify(u[0], v[0], s)
        # return s and unify(u[1:], v[1:], s)
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


# for now we're going to treat mzero as [] and (unit x) as [x]

def eq(u, v):
    def goal(state):
        s = unify(u, v, state[0])
        if s is not False:
            return [(s, state[1])]
        else:
            return []

    return goal


def call_fresh(f):
    def goal(state):
        c = state[1]
        return f(var(c))((state[0], c + 1))

    return goal


EMPTY_STATE = ({}, 0)


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
    assert unify(var(0), [1, 2, 3], {}) == {var(0): [1, 2, 3]}
    assert unify([1, 2, 3], [1, 2, 3], {}) == {}
    assert unify([1, 2, 3], [3, 2, 1], {}) == False
    assert unify([var(0), var(1)], [1, 2], {}) == {var(0): 1, var(1): 2}
    assert unify([[1, 2], [3, 4]], [[1, 2], [3, 4]], {}) == {}
    assert unify([[var(0), 2], [3, 4]], [[1, 2], [3, 4]], {}) == {var(0): 1}

    assert unify([1, 2, 3, 4], [1, 2, var(0)], {}) == False
    # however
    assert unify([1, [2, [3, 4]]], [1, [2, var(0)]], {}) == {var(0): [3, 4]}

    assert unify({}, {}, {}) == {}

    assert eq(1,1)(EMPTY_STATE) == [EMPTY_STATE]
    assert eq(1,2)(EMPTY_STATE) == []

    assert call_fresh(lambda q: eq(q, 5))(EMPTY_STATE) == [({var(0): 5}, 1)]
