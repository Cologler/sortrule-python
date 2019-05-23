# -*- coding: utf-8 -*-
#
# Copyright (c) 2019~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from threading import Lock

from .abc import INodeSet, empty, IKeySelector, INode, IReadonlyNode, IOrderCodeCache
from .node import SortRuleNode, CachedNode
from .utils import MixDict

class KeySelector(IKeySelector, IOrderCodeCache):
    def __init__(self, src: INodeSet):
        self._order_code_cache = {}
        self._hint = 0
        self._data = MixDict()
        self._data.update(dict((k, CachedNode(v)) for (k, v) in src._data.items()))

        for node in self._data.values():
            node.get_order_code(self) # ensure all values cached
        assert len(self._data) == len(self._order_code_cache) == self._hint

    def get_key(self, item):
        node = self._data.get(item)
        if node is None:
            code = (1, node)
        else:
            code = (0, node.get_order_code(self))
        return code

    def get_order_code(self, node: IReadonlyNode):
        try:
            return self._order_code_cache[node]
        except KeyError:
            pass

        self._hint += 1
        code = node.get_order_code(self)
        self._order_code_cache[node] = code
        return code


class KeySelectorBuilder(INodeSet[INode]):
    def _create_node(self, key):
        return self._data.setdefault(key, SortRuleNode(self))

    def get_key_selector(self):
        return KeySelector(self)
