# -*- coding: utf-8 -*-
#
# Copyright (c) 2019~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from pytest import raises

from sortrule import SortRules

def test_sortrule_sort_with_default():
    sr = SortRules()
    assert sr.sort([1, 2, 3, 4]) == [1, 2, 3, 4]

def _assert_from_pairs(pairs, *examples):
    sr = SortRules()
    for pair in pairs:
        sr.has_order(*pair)
    for example in examples:
        ret = sr.sort(example)
        print(ret)
        for f, s in pairs:
            assert ret.index(f) < ret.index(s), (f, s)

def test_sortrule_sort_with_has_order():
    pairs = [
        (1, 4), (4, 2), (4, 3), (3, 5)
    ]
    _assert_from_pairs(pairs, [1, 2, 3, 4, 5, 6])

def test_sortrule_can_detect_loop_1():
    sr = SortRules()

    with raises(TypeError):
        sr.has_order(1, 1)

def test_sortrule_can_detect_loop_2():
    sr = SortRules()

    sr.has_order(1, 2)
    sr.has_order(2, 3)

    with raises(TypeError):
        sr.has_order(3, 1)

def test_sortrule_can_detect_recursion():
    sr = SortRules()
    sr.has_order(1, 2)
    sr.has_order(2, 3)
    sr.has_order(3, 4)
    with raises(TypeError):
        sr.has_order(4, 1)
