import os
import json
from Lock import Lock

configurations = [['exclusive', 'exclusive'], ['exclusive', 'shared'], ['shared', 'exclusive']]

def get_conflict_graph(dirname, appname, lock):
    with open(os.path.join(dirname, appname+'.json'), 'r') as f:
        tokens = json.load(f)

    conflict_graph = {} # vertex to list of edges
    for t in tokens:
        for c in t['conflicts']:
            if t['name'] in lock and c['conflict'] in lock:
                # relevant conflict relation, add to conflict graph
                if not t['name'] in conflict_graph:
                    conflict_graph[t['name']] = set()
                conflict_graph[t['name']].add(c['conflict'])
                if not c['conflict'] in conflict_graph:
                    conflict_graph[c['conflict']] = set()
                conflict_graph[c['conflict']].add(t['name'])
    return conflict_graph


# divides the graph into two parts
def get_parts(lock, dirname, appname):
    conflict_graph = get_conflict_graph(dirname, appname, lock)
    cover = {}
    cover[0] = set()
    cover[1] = set()
    for u in conflict_graph:
        for v in conflict_graph[u]:
            if u in cover[0]:
                cover[1].add(v)
            elif u in cover[1]:
                cover[0].add(v)
            elif v in cover[0]:
                cover[1].add(u)
            elif v in cover[1]:
                cover[0].add(u)
            else:
                # u and v are unassigned
                cover[0].add(u)
                cover[1].add(v)
    return cover


def get_mode_configurations(locklist, prev, dirname, appname):
    # print('locklist', locklist)
    if not locklist:
        return prev

    locks = []
    for each in configurations:
        newlock = Lock(locklist[0].name)
        # newlock.mode = each
        parts = get_parts(locklist[0].name, dirname, appname)
        for op in locklist[0].ops:
            if op in parts[0]:
                newlock.ops[op] = each[0]
            elif op in parts[1]:
                newlock.ops[op] = each[1]
            else:
                raise Exception('unassigned op', op)
        newlock.placement = locklist[0].placement
        newlock.param = locklist[0].param
        locks += [newlock]
    
    if prev:
        result = []
        for new in locks:
            for each in prev:
                result += [each + [new]]
    else:
        result = [[l] for l in locks]
    return get_mode_configurations(locklist[1:], result, dirname, appname)


# for each lock, generate possible modes. for 2 op locks = ee, es, se. for more than that, minimum vertex coverage problem
# then generate all possible permutations, again 3 ** n
def generate_mode(locklist, dirname, appname, gran):
    result = get_mode_configurations(locklist, [], dirname, appname)
    i = 1
    if not os.path.exists(os.path.join(dirname, appname, gran)):
        os.makedirs(os.path.join(dirname, appname, gran))
    for lst in result:
        ops = {}
        for each in lst:
            for op in each.ops:
                if not op in ops:
                    ops[op] = []
                ops[op] += [each]
        content = []
        for op in ops:
            locks = []
            for l in ops[op]:
                locks += [{'name':l.name, 'mode':l.ops[op]}]
            o = {'op':op, 'locks':locks}
            content += [o]

        outputfile = os.path.join(dirname, appname, gran, 'oplock'+str(i)+'.json')
        with open(outputfile, 'w') as f:
            json.dump(content, f)
        i += 1
    return i - 1

