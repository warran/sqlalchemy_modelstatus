# -*- encoding: utf-8 -*-

from itertools import chain


def nested_values(dictionary):
    recursive = lambda d: nested_values(d) \
        if isinstance(d, dict) else d
    nested_vals = [recursive(v) for v in dictionary.values()]

    return flatten_iterable(nested_vals)


def flatten_iterable(nested_iterable):
    recursive = lambda i: flatten_iterable(i) \
        if hasattr(i, '__iter__') \
        else [i]
    nested_iterable = [recursive(e) for e in nested_iterable]
    return chain(*nested_iterable)
