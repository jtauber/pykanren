#!/usr/bin/env python

from kanren import *  # noqa


s1 = {Var("x"): 5, Var("y"): True}
s2 = {Var("y"): 5, Var("x"): Var("y")}


assert lookup(Var("x"), s1) == 5
assert lookup(Var("x"), s2) == Var("y")

assert repr(lookup(Var("x"), {})) == "<x>"
assert lookup(5, {}) == 5

assert walk(Var("x"), s1) == 5
assert walk(Var("x"), s2) == 5


s3 = {Var("x"): Var("y")}
assert occurs_check(Var("y"), Var("x"), s3) is True
assert occurs_check(Var("y"), 5, s3) is False
assert occurs_check(Var("x"), Var("x"), {}) is True


assert ext_s_check(Var("y"), Var("x"), s3) is False
assert ext_s_check(Var("y"), 5, s3) == {Var("y"): 5, Var("x"): Var("y")}
assert ext_s_check(Var("x"), Var("x"), {}) is False


assert unify_check(None, 1, {}) is False
assert unify_check(None, Var("x"), {}) == {Var("x"): None}
assert unify_check(None, [1, Var("x")], {}) is False
assert unify_check(1, None, {}) is False
assert unify_check(1, 1, {}) == {}
assert unify_check(1, 2, {}) is False
assert unify_check(1, Var("x"), {}) == {Var("x"): 1}
assert unify_check(1, [], {}) is False
assert unify_check(Var("x"), 1, {}) == {Var("x"): 1}
assert unify_check(Var("x"), Var("y"), {}) == {Var("x"): Var("y")}
assert unify_check(Var("x"), [], {}) == {Var("x"): []}
assert unify_check(Var("x"), [1, 2, 3], {}) == {Var("x"): [1, 2, 3]}
assert unify_check([1, 2, 3], [1, 2, 3], {}) == {}
assert unify_check([1, 2, 3], [3, 2, 1], {}) is False
assert unify_check([Var("x"), Var("y")], [1, 2], {}) == {Var("x"): 1, Var("y"): 2}
assert unify_check([[1, 2], [3, 4]], [[1, 2], [3, 4]], {}) == {}
assert unify_check([[Var("x"), 2], [3, 4]], [[1, 2], [3, 4]], {}) == {Var("x"): 1}

assert unify_check([1, 2, 3, 4], [1, 2, Var("x")], {}) is False
# however
assert unify_check([1, [2, [3, 4]]], [1, [2, Var("x")]], {}) == {Var("x"): [3, 4]}

assert unify_check({}, {}, {}) == {}

assert unify(None, 1, {}) is False
assert unify(None, Var("x"), {}) == {Var("x"): None}
assert unify(None, [1, Var("x")], {}) is False
assert unify(1, None, {}) is False
assert unify(1, 1, {}) == {}
assert unify(1, 2, {}) is False
assert unify(1, Var("x"), {}) == {Var("x"): 1}
assert unify(1, [], {}) is False
assert unify(Var("x"), 1, {}) == {Var("x"): 1}
assert unify(Var("x"), Var("y"), {}) == {Var("x"): Var("y")}
assert unify(Var("x"), [], {}) == {Var("x"): []}
assert unify(Var("x"), [1, 2, 3], {}) == {Var("x"): [1, 2, 3]}
assert unify([1, 2, 3], [1, 2, 3], {}) == {}
assert unify([1, 2, 3], [3, 2, 1], {}) is False
assert unify([Var("x"), Var("y")], [1, 2], {}) == {Var("x"): 1, Var("y"): 2}
assert unify([[1, 2], [3, 4]], [[1, 2], [3, 4]], {}) == {}
assert unify([[Var("x"), 2], [3, 4]], [[1, 2], [3, 4]], {}) == {Var("x"): 1}

assert unify([1, 2, 3, 4], [1, 2, Var("x")], {}) is False
# however
assert unify([1, [2, [3, 4]]], [1, [2, Var("x")]], {}) == {Var("x"): [3, 4]}

assert unify({}, {}, {}) == {}


s = {Var("z"): 6, Var("y"): 5, Var("x"): [Var("y"), Var("z")]}
assert walk(Var("x"), s) == [Var("y"), Var("z")]
assert walk_star(Var("x"), s) == [5, 6]


assert reify([5, Var("x"), [True, Var("y"), Var("x")], Var("z")]) == [5, "_0", [True, "_1", "_0"], "_2"]

assert list(eq_check(1, 1)({})) == [{}]
assert list(eq_check(1, 2)({})) == [False]

assert list(eq(1, 1)({})) == [{}]
assert list(eq(1, 2)({})) == [False]


assert list(map_inf(1, None, [])) == []
assert list(map_inf(3, lambda i: i, [1, 2, 3])) == [1, 2, 3]
assert list(map_inf(2, lambda i: i, [1, 2, 3])) == [1, 2]
assert list(map_inf(1, lambda i: i, [1, 2, 3])) == [1]
assert list(map_inf(0, lambda i: i, [1, 2, 3])) == []
assert list(map_inf(None, lambda i: i, [1, 2, 3])) == [1, 2, 3]


assert list(mplus([1, 2, 3], [4, 5])) == [1, 2, 3, 4, 5]
assert list(mplusi([1, 2, 3], [4, 5])) == [1, 4, 2, 5, 3]

assert list(all_()({})) == [{}]
assert list(all_(SUCCESS)({})) == [{}]
assert list(all_(eq(1, 1), eq(2, 2))({})) == [{}]
assert list(all_(eq(1, 2), eq(1, 2))({})) == [False]

assert run(None, "q", FAIL) == ()
assert run(None, "q", eq(True, Var("q"))) == (True,)
assert run(None, "q", eq(False, Var("q"))) == (False,)
assert run(None, "q", FAIL, eq(True, Var("q"))) == ()
assert run(None, "q", SUCCESS, eq(True, Var("q"))) == (True,)
assert run(None, "r", SUCCESS, eq("corn", Var("r"))) == ("corn",)
assert run(None, "r", FAIL, eq("corn", Var("r"))) == ()
assert run(None, "q", SUCCESS, eq(False, Var("q"))) == (False,)  # should return (False,) not ("_0",)

assert run(None, "q", (lambda x: eq(True, x))(False)) == ()
assert run(None, "q", lambda s: (lambda x: all_(eq(True, x), eq(True, Var("q")))(s))(Var("x"))) == (True,)

assert run(None, "x", SUCCESS) == ("_0",)

print("all tests passed.")
