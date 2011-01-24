# dioid settings
#
# a idempotent semiring for combinatorial settings,
# with two operation:
#  + : DS x DS -> DS, a union of different values (for the same keys).
#  * : DS x DS -> DS, a cartesian product of values for different keys,
#                     e.g., nested for-loops.
#  and neutral elements 0 = []       (the empty set)
#                       1 = [dict()] (the set containing an empty dictionary)

def sum(dss):
    result = DS()
    for ds in dss:
        result += ds
    return result

def product(dss):
    result = DS()
    result.set.append({})
    for ds in dss:
        result *= ds
    return result

def DS(key=None, value=None):
    if isinstance(key, tuple):
        for values in value:
            # print 'values', values
            # print 'zip', zip(key, values)
            # print 'map', [DS(k, v) for k,v in zip(key, values)]
            return sum(product( [DS(k, v) for k,v in zip(key, values)] ) for values in value)
    elif hasattr(value, '__iter__'):
        return sum((DioidSettings(key, v) for v in value))
    else:
        return DioidSettings(key, value)

class DioidSettings(object):
    """Contains a set of dictionaries, and implements + and *"""

    def __init__(self, key=None, value=None):
        self.set = []
        if not key is None:
            d = dict()
            d[key] = value
            self.set.append(d)

    def __str__(self):
        if self.set == []:
            return '[ 0 ]'
        elif self.set == [{}]:
            return '[ 1 ]'
        else:
            return '[\n ' + '\n '.join(str(s) for s in self.set) + '\n]'

    def __add__(self, other):
        result = DioidSettings()
        result.set = self.set + other.set
        return result

    def __mul__(self, other):
        result = DioidSettings()
        for sd in self.set:
            for od in other.set:
                rd = {}
                rd.update(sd)
                rd.update(od)
                # make unicity test for idempotent multiplication
                if not rd in result.set:
                    result.set.append(rd)
        return result

    def __eq__(self, other):
        return self.set == other.set

# neutral element w.r.t. +
zero = sum([])

# neutral element w.r.t. *
one = product([])
