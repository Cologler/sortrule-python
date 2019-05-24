# -*- coding: utf-8 -*-
#
# Copyright (c) 2019~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from threading import Lock

from .abc import INodeSet, EmptyNode, IKeySelector, INode, IReadonlyNode, IOrderCodeCache
from .node import SortRuleNode
from .utils import MixDict

class KeySelector(IKeySelector, IOrderCodeCache):
    def __init__(self, src: INodeSet):
        self._order_code_cache = {}
        self._hint = 0
        self._data = src._data.copy()

        for node in self._data.values():
            self.get_order_code(node) # ensure all values cached

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


empty = EmptyNode()


class KeySelectorBuilder(INodeSet):
    def __init__(self):
        self._data = MixDict()

    def get_node(self, key, create=False):
        try:
            return self._data[key]
        except KeyError:
            pass

        if create:
            return self._create_node(key)
        else:
            return empty

    def _create_node(self, key):
        return self._data.setdefault(key, SortRuleNode(self))

    def get_key_selector(self):
        return KeySelector(self)
