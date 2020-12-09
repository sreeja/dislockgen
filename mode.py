import os
import json

modes = [['exclusive', 'exclusive'], ['exclusive', 'shared'], ['shared', 'exclusive']]

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
    # print(conflict_graph)
    return conflict_graph

def get_parts(lock, dirname, appname):
    conflict_graph = get_conflict_graph(dirname, appname, lock)
    # with this conflict graph, identify the minimal vertex cover
    cover = {}
    cover[0] = set()
    cover[1] = set()
    # visited = set()
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


# for each lock, generate possible modes. for 2 op locks = ee, es, se. for more than that, minimum vertex coverage problem
# then generate all possible permutations, again 3 ** n
def generate_mode(locklist, dirname, appname):
    # divide graph into two to acquire each mode
    partdict = {}
    for lock in locklist:
        parts = get_parts(lock)
        partdict[lock.name] = parts
    # iterate through modes and assign ops into the pairs according to part membership

