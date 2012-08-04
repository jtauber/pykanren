#!/usr/bin/env python

from kanren import *


s1 = {Var("x"): 5, Var("y"): True}
s2 = {Var("y"): 5, Var("x"): Var("y")}


assert lookup(Var("x"), s1) == 5
assert lookup(Var("x"), s2) == Var("y")


assert walk(Var("x"), s1) == 5
assert walk(Var("x"), s2) == 5


s3 = {Var("x"): Var("y")}
assert occurs_check(Var("y"), Var("x"), s3) == True
assert occurs_check(Var("y"), 5, s3) == False
assert occurs_check(Var("x"), Var("x"), {}) == True


assert extend_s(Var("y"), Var("x"), s3) == False
assert extend_s(Var("y"), 5, s3) == {Var("y"): 5, Var("x"): Var("y")}
assert extend_s(Var("x"), Var("x"), {}) == False


assert unify(None, 1, {}) == False
assert unify(None, Var("x"), {}) == {Var("x"): None}
assert unify(1, None, {}) == False
assert unify(1, 1, {}) == {}
assert unify(1, 2, {}) == False
assert unify(1, Var("x"), {}) == {Var("x"): 1}
assert unify(Var("x"), 1, {}) == {Var("x"): 1}
assert unify(Var("x"), Var("y"), {}) == {Var("x"): Var("y")}


assert unify_no_check(None, 1, {}) == False
assert unify_no_check(None, Var("x"), {}) == {Var("x"): None}
assert unify_no_check(1, None, {}) == False
assert unify_no_check(1, 1, {}) == {}
assert unify_no_check(1, 2, {}) == False
assert unify_no_check(1, Var("x"), {}) == {Var("x"): 1}
assert unify_no_check(Var("x"), 1, {}) == {Var("x"): 1}
assert unify_no_check(Var("x"), Var("y"), {}) == {Var("x"): Var("y")}


s = {Var("z"): 6, Var("y"): 5, Var("x"): [Var("y"), Var("z")]}
assert walk(Var("x"), s) == [Var("y"), Var("z")]
assert walk_star(Var("x"), s) == [5, 6]


assert reify([5, Var("x"), [True, Var("y"), Var("x")], Var("z")], {}) == [5, "_0", [True, "_1", "_0"], "_2"]
