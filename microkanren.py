# same as I did with minikanren
#
# (var c) becomes Var(c)
# (var? x) becomes isinstance(x, Var)
# (var=? x_1 x_2) becomes x_1 == x_2

class Var:
    def __init__(self, symbol):
        self.symbol = symbol

    def __eq__(self, other):
        return isinstance(other, Var) and self.symbol == other.symbol

    def __hash__(self):
        return hash(self.symbol)

    def __repr__(self):
        return "<%s>" % self.symbol


# this also stays the same as the python for minikanren, using a dictionary
# for substitutions

def walk(u, s):
    if isinstance(u, Var):
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
    if isinstance(u, Var) and isinstance(v, Var) and u == v:
        return s
    elif isinstance(u, Var):
        s[u] = v
        return s
    elif isinstance(v, Var):
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


if __name__ == "__main__":

    s1 = {Var("x"): 5, Var("y"): True}
    s2 = {Var("y"): 5, Var("x"): Var("y")}

    assert walk(Var("x"), s1) == 5
    assert walk(Var("x"), s2) == 5

    assert unify(None, 1, {}) == False
    assert unify(None, Var("x"), {}) == {Var("x"): None}
    assert unify(None, [1, Var("x")], {}) == False
    assert unify(1, None, {}) == False
    assert unify(1, 1, {}) == {}
    assert unify(1, 2, {}) == False
    assert unify(1, Var("x"), {}) == {Var("x"): 1}
    assert unify(1, [], {}) == False
    assert unify(Var("x"), 1, {}) == {Var("x"): 1}
    assert unify(Var("x"), Var("y"), {}) == {Var("x"): Var("y")}
    assert unify(Var("x"), [], {}) == {Var("x"): []}
    assert unify(Var("x"), [1, 2, 3], {}) == {Var("x"): [1, 2, 3]}
    assert unify([1, 2, 3], [1, 2, 3], {}) == {}
    assert unify([1, 2, 3], [3, 2, 1], {}) == False
    assert unify([Var("x"), Var("y")], [1, 2], {}) == {Var("x"): 1, Var("y"): 2}
    assert unify([[1, 2], [3, 4]], [[1, 2], [3, 4]], {}) == {}
    assert unify([[Var("x"), 2], [3, 4]], [[1, 2], [3, 4]], {}) == {Var("x"): 1}

    assert unify([1, 2, 3, 4], [1, 2, Var("x")], {}) == False
    # however
    assert unify([1, [2, [3, 4]]], [1, [2, Var("x")]], {}) == {Var("x"): [3, 4]}

    assert unify({}, {}, {}) == {}
