# -*- coding: utf-8 -*-
#
# Copyright (c) 2019~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from .abc import INode, INodeSet, IReadonlyNode, IOrderCodeCache

class CachedNode(IReadonlyNode):
    __slots__ = ('_node', '_value')

    def __init__(self, node):
        self._node = node

    def get_order_code(self, cache: IOrderCodeCache):
        return cache.get_order_code(self._node)


class SortRuleNode(INode):
    __slots__ = ('_node_set', '_before_me')

    def __init__(self, node_set: INodeSet):
        self._node_set = node_set
        self._before_me = set()

    def __repr__(self):
        return f'SortRuleNode({self._before_me})'

    def has_before(self, value):
        '''
        declare value should before than self.
        '''
        if self is value:
            raise TypeError
        if self in value.get_before_chain():
            raise TypeError

        self._before_me.add(value)

    def get_before(self):
        return frozenset(self._before_me)

    def get_before_chain(self):
        node_set = self._node_set
        ret = set()
        ret.update(self._before_me)
        for item in self._before_me:
            ret.update(item.get_before_chain())
        return frozenset(ret)

    def get_order_code(self, cache: IOrderCodeCache):
        return sum(cache.get_order_code(x) for x in self._before_me) + 1
