# generate granularity lattice
import json
from Lock import Lock


def get_finest_locks(filename):
    with open(filename, 'r') as f:
        tokens = json.load(f)

    locks = {}
    for t in tokens:
        for c in t['conflicts']:
            lockname = '_'.join(sorted([t['name'], c['conflict']]))
            if not lockname in locks:
                lock = Lock(lockname)
                lock.ops[c['conflict']] = ''
                lock.ops[t['name']] = ''
                lock.param = c['param']
                locks[lockname] = lock
    #             print(lockname, lock.ops, lock.param)
    # print(len(locks))
    return locks


def get_coarsening(first, locklist):
    result = {}
    first_ops = set(first.ops.keys())
    coarsened_index = -1
    for i, each in enumerate(locklist):
        coarsened = False
        if coarsened_index < 0 and each.param == first.param:
            each_ops = set(each.ops.keys())
            common = each_ops.intersection(first_ops)
            if common:
                # print('can coarsen', first.name, each.name)
                lockname = '_'.join(sorted(each_ops.union(first_ops)))
                if not lockname in result:
                    result[lockname] = Lock(lockname)
                result[lockname].ops = {**(each.ops), **(first.ops)}
                result[lockname].param = first.param
                coarsened = True
                coarsened_index = i
        if not coarsened:
            result[each.name] = each
    return result, coarsened_index


def get_coarsenings(finest):
    locks = []
    lst = [v for v in finest.values()]
    prev = []
    while lst:
        first = lst.pop(0)
        remains = [v for v in lst]
        dealt = []
        while remains:
            coarsened, coarsening_index = get_coarsening(first, remains)
            for each in prev:
                coarsened[each.name] = each
            for each in dealt:
                coarsened[each.name] = each
            if coarsening_index >= 0:
                coarsened_lock = remains.pop(coarsening_index)
                locks += [coarsened]
                dealt += [coarsened_lock]
            else:
                break
        prev += [first]
    return locks


def get_level(prev_level):
    level = []
    for each in prev_level:
        level += get_coarsenings(each)
    return level


def remove_duplicates(levels):
    result = []
    base = {}
    i = 0
    for level in levels:
        base[i] = set()
        cleaned_level = []
        for combo in level:
            name = '+'.join(sorted([v.name for v in combo.values()]))
            if not name in base[i]:
                base[i].add(name)
                cleaned_level += [combo]
        result += [cleaned_level]
    return result


def generate_lattice(filename):
    levels = []
    finest = get_finest_locks(filename)
    levels += [[finest]]

    total_levels = len(finest)
    # print('finest', len(finest))
    base = [finest]
    while total_levels > 1:
        next_level = get_level(base)
        # print('level', next_level)
        levels += [next_level]
        base = next_level
        total_levels -= 1

    cleaned_levels = remove_duplicates(levels)
    return cleaned_levels

