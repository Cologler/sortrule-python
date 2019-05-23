# -*- coding: utf-8 -*-
#
# Copyright (c) 2019~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from pytest import raises

from sortrule.utils import MixDict

def test_mixdict_new():
    md = MixDict()
    assert not md
    assert len(md) == 0

def test_mixdict_simple():
    md = MixDict()
    with raises(KeyError):
        md['a']

    md['a'] = 1
    assert md['a'] == 1
    assert len(md) == 1

    del md['a']
    with raises(KeyError):
        md['a']
    assert len(md) == 0

def test_mixdict_with_none():
    md = MixDict()
    with raises(KeyError):
        md[None]

    md[None] = 1
    assert md[None] == 1
    assert len(md) == 1

    del md[None]
    with raises(KeyError):
        md[None]
    assert len(md) == 0
