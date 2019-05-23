# -*- coding: utf-8 -*-
#
# Copyright (c) 2019~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from collections.abc import MutableMapping

class MixDict(MutableMapping):
    __slots__ = ('_d', '_k', '_v')

    def __init__(self):
        self._d = {}
        self._k = []
        self._v = []

    def __getitem__(self, k):
        try:
            return self._d[k]
        except TypeError:
            pass

        try:
            idx = self._k.index(k)
        except ValueError:
            raise KeyError(k)

        return self._v[idx]

    def __setitem__(self, k, v):
        try:
            self._d[k] = v
            return
        except TypeError:
            pass

        try:
            idx = self._k.index(k)
        except ValueError:
            self._k.append(k)
            self._v.append(v)
            return

        self._v[idx] = v

    def __delitem__(self, k):
        try:
            del self._d[k]
            return
        except TypeError:
            pass

        try:
            idx = self._k.index(k)
        except ValueError:
            raise KeyError(k)

        return self._v.pop(idx)

    def __iter__(self):
        yield from self._d
        yield from self._k

    def __len__(self):
        return len(self._d) + len(self._k)
