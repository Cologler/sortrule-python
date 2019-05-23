# -*- coding: utf-8 -*-
#
# Copyright (c) 2019~2999 - Cologler <skyoflw@gmail.com>
# ----------
# a simple sort system
# ----------

from typing import Generic, TypeVar
from abc import ABC, abstractmethod

from .utils import MixDict

class IOrderCodeCache(ABC):
    @abstractmethod
    def get_order_code(self, node):
        raise NotImplementedError


TNode = TypeVar('TNode')


class IReadonlyNode(ABC):
    __slots__ = ()

    @abstractmethod
    def get_order_code(self, node_set):
        raise NotImplementedError


class INode(IReadonlyNode):
    __slots__ = ()

    def has_before(self, value):
        '''declare value should before than this one.'''
        raise NotImplementedError

    @abstractmethod
    def get_before_chain(self):
        raise NotImplementedError


class EmptyNode(INode):
    __slots__ = ()
    _empty_set = frozenset()

    def __repr__(self):
        return 'Empty()'

    def get_before_chain(self):
        return self._empty_set

    def get_order_code(self, _):
        return 1

empty = EmptyNode()


class IKeySelector(ABC):
    @abstractmethod
    def get_key(self, item):
        raise NotImplementedError


class INodeSet(ABC, Generic[TNode]):
    def __init__(self):
        self._data = MixDict()

    def get_node(self, key, create=False) -> TNode:
        try:
            return self._data[key]
        except KeyError:
            pass

        if create:
            return self._create_node(key)
        else:
            return empty

    @abstractmethod
    def _create_node(self, key) -> TNode:
        raise NotImplementedError

    @abstractmethod
    def get_key_selector(self):
        raise NotImplementedError
