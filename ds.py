# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# dioid settings                                                              #
#                                                                             #
# 2011 - Robert Schwarz <schwarz@zib.de>                                      #
#                                                                             #
# A semiring for combinatorial settings, with two operations:                 #
#  + : DS x DS -> DS, a concatenation of different values (for the same keys) #
#  * : DS x DS -> DS, a cartesian product of values for different keys,       #
#                     e.g., nested for-loops.                                 #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import itertools

def DS(key=None, value=None):
    if isinstance(key, tuple):
        return DSSum(DSProduct(DS(k, v) for k,v in zip(key, vs)) for vs in value)
    elif hasattr(value, '__iter__'):
        return DSSum((DioidSettings(key, v) for v in value))
    else:
        return DioidSettings(key, value)

class DioidSettings(object):
    """Contains a set of dictionaries, and implements + and *"""

    def __init__(self, key=None, value=None):
        self.d = None
        if not key is None:
            self.d = {}
            if not value is None:
                self.d[key] = value

    def __str__(self):
        return str(list(self))

    def __add__(self, other):
        return DSSum([self, other])

    def __mul__(self, other):
        return DSProduct([self, other])

    def __iter__(self):
        if not self.d is None:
            yield self.d


class DSSum(DioidSettings):
    """Represents a sum of two DioidSettings"""

    def __init__(self, summands):
        self.summands = list(summands)

    def __iter__(self):
        for s in self.summands:
            for d in s:
                yield d

class DSProduct(DioidSettings):
    """Represents a product of two DioidSettings"""

    def __init__(self, factors):
        self.factors = list(factors)

    def __iter__(self):
        for p in itertools.product(*self.factors):
            d = {}
            for f in p:
                d.update(f)
            yield d
