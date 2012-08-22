#!/usr/bin/env python

from kanren import *


s1 = {Var("x"): 5, Var("y"): True}
s2 = {Var("y"): 5, Var("x"): Var("y")}


assert lookup(Var("x"), s1) == 5
assert lookup(Var("x"), s2) == Var("y")

assert repr(lookup(Var("x"), {})) == "<x>"
assert lookup(5, {}) == 5

assert walk(Var("x"), s1) == 5
assert walk(Var("x"), s2) == 5


s3 = {Var("x"): Var("y")}
assert occurs_check(Var("y"), Var("x"), s3) == True
assert occurs_check(Var("y"), 5, s3) == False
assert occurs_check(Var("x"), Var("x"), {}) == True


assert ext_s_check(Var("y"), Var("x"), s3) == False
assert ext_s_check(Var("y"), 5, s3) == {Var("y"): 5, Var("x"): Var("y")}
assert ext_s_check(Var("x"), Var("x"), {}) == False


assert unify_check(None, 1, {}) == False
assert unify_check(None, Var("x"), {}) == {Var("x"): None}
assert unify_check(None, [1, Var("x")], {}) == False
assert unify_check(1, None, {}) == False
assert unify_check(1, 1, {}) == {}
assert unify_check(1, 2, {}) == False
assert unify_check(1, Var("x"), {}) == {Var("x"): 1}
assert unify_check(1, [], {}) == False
assert unify_check(Var("x"), 1, {}) == {Var("x"): 1}
assert unify_check(Var("x"), Var("y"), {}) == {Var("x"): Var("y")}
assert unify_check(Var("x"), [], {}) == {Var("x"): []}
assert unify_check(Var("x"), [1, 2, 3], {}) == {Var("x"): [1, 2, 3]}
assert unify_check([1, 2, 3], [1, 2, 3], {}) == {}
assert unify_check([1, 2, 3], [3, 2, 1], {}) == False
assert unify_check([Var("x"), Var("y")], [1, 2], {}) == {Var("x"): 1, Var("y"): 2}
assert unify_check([[1, 2], [3, 4]], [[1, 2], [3, 4]], {}) == {}
assert unify_check([[Var("x"), 2], [3, 4]], [[1, 2], [3, 4]], {}) == {Var("x"): 1}

assert unify_check([1, 2, 3, 4], [1, 2, Var("x")], {}) == False
# however
assert unify_check([1, [2, [3, 4]]], [1, [2, Var("x")]], {}) == {Var("x"): [3, 4]}

assert unify_check({}, {}, {}) == {}

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


s = {Var("z"): 6, Var("y"): 5, Var("x"): [Var("y"), Var("z")]}
assert walk(Var("x"), s) == [Var("y"), Var("z")]
assert walk_star(Var("x"), s) == [5, 6]


assert reify([5, Var("x"), [True, Var("y"), Var("x")], Var("z")], {}) == [5, "_0", [True, "_1", "_0"], "_2"]


assert eq(1, 1)({}) == [{}]
assert eq(1, 2)({}) == []


assert eq_no_check(1, 1)({}) == [{}]
assert eq_no_check(1, 2)({}) == []


assert map_inf(1, None, ()) == ()
assert map_inf(3, lambda i: i, (1, lambda: (2, lambda: 3))) == (1, (2, (3,)))
assert map_inf(2, lambda i: i, (1, lambda: (2, lambda: 3))) == (1, (2,))
assert map_inf(1, lambda i: i, (1, lambda: (2, lambda: 3))) == (1,)
assert map_inf(0, lambda i: i, (1, lambda: (2, lambda: 3))) == (1,)  # is this correct?
assert map_inf(None, lambda i: i, (1, lambda: (2, lambda: 3))) == (1, (2, (3,)))


print("all tests passed.")
