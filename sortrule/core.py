# -*- coding: utf-8 -*-
#
# Copyright (c) 2019~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from .nodeset import KeySelectorBuilder

class SortRules:
    def __init__(self):
        self._selector_builder = KeySelectorBuilder()
        self._cached_key = None

    def has_order(self, first, second):
        ''' declare has orders. '''
        self._cached_key = None
        first_node = self._selector_builder.get_node(first, True)
        second_node = self._selector_builder.get_node(second, True)
        second_node.has_before(first_node)

    def has_orders(self, iterable):
        '''
        declare has orders.

        equals:

        ``` py
        has_order(item_1, item_2)
        has_order(item_2, item_3)
        ...
        ```
        '''
        items = list(iterable)
        if len(items) < 2:
            raise ValueError

        for pair in zip(items, items[1:]):
            self.has_order(*pair)

    def has_order_pairs(self, iterable):
        '''
        declare has orders.

        equals:

        ``` py
        for pair in iterable:
            has_order(*pair)
        ```
        '''
        for pair in iterable:
            self.has_order(*pair)

    def get_key(self):
        '''
        use a frozen state to build the `key` function that can use in `sorted` function.
        '''
        if self._cached_key is None:
            selector = self._selector_builder.get_key_selector()
            self._cached_key = selector.get_key
        return self._cached_key

    def sort(self, iterable) -> list:
        '''
        use the rules to sort the `iterable`
        '''
        return sorted(iterable, key=self.get_key())
