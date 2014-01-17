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

if __name__ == "__main__":

    s1 = {Var("x"): 5, Var("y"): True}
    s2 = {Var("y"): 5, Var("x"): Var("y")}

    assert walk(Var("x"), s1) == 5
    assert walk(Var("x"), s2) == 5
