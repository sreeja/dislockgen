OPS = 'ops'
MODE = 'mode'
PLACEMENT = 'place'
EXCLUSIVE = 'exclusive'
SHARED = 'shared'
CENT = 'cent'
CLUST = 'clust'
DIST = 'dist'

replicas = ['paris', 'tokyo', 'singapore', 'capetown', 'newyork']
ops = ['a', 'b']
Cost = {CENT:{'paris':127.484,'tokyo':866.836,'singapore':897.060,'capetown':595.722,'newyork':363.777},
        CLUST:{'paris':433.156,'tokyo':1516.557,'singapore':1202.702,'capetown':716.398,'newyork':276.888},
        DIST:{'paris':701.746,'tokyo':956.047,'singapore':1051.981,'capetown':975.570,'newyork':539.720}
        }
Exec = {'a':0.5, 'b':1.2}
workload = {'workloadeqeq':{'a':[100,100,100,100,100],'b':[100,100,100,100,100]},
            'workloadeqhot':{'a':[500,0,0,0,0],'b':[500,0,0,0,0]},
            'workloadeqclust':{'a':[167,167,166,0,0],'b':[500,0,0,0,0]},
            'workloadhoteq':{'a':[200,200,200,200,200],'b':[0,0,0,0,0]},
            'workloadhothot':{'a':[1000,0,0,0,0],'b':[0,0,0,0,0]},
            'workloadhotclust':{'a':[334,333,333,0,0],'b':[0,0,0,0,0]}
            }
locks = {'labp11':{OPS:{'a':{MODE:EXCLUSIVE},'b':{MODE:SHARED}}, PLACEMENT:CENT},
        'labp12':{OPS:{'a':{MODE:EXCLUSIVE},'b':{MODE:SHARED}}, PLACEMENT:CLUST},
        'labp13':{OPS:{'a':{MODE:EXCLUSIVE},'b':{MODE:SHARED}}, PLACEMENT:DIST},
        'labp21':{OPS:{'a':{MODE:SHARED},'b':{MODE:EXCLUSIVE}}, PLACEMENT:CENT},
        'labp22':{OPS:{'a':{MODE:SHARED},'b':{MODE:EXCLUSIVE}}, PLACEMENT:CLUST},
        'labp23':{OPS:{'a':{MODE:SHARED},'b':{MODE:EXCLUSIVE}}, PLACEMENT:DIST}
}


def LHT(op, place, r):
    return Exec[op] + Cost[place][r]


def operation_serialization(l,r, wl):
    res = 0
    for op in locks[l][OPS]:
        if locks[l][OPS][op][MODE] == EXCLUSIVE:
            for i, rep in enumerate(replicas):
                if rep != r:
                    # print(LHT(op, locks[l][PLACEMENT], r))
                    # print(workload[wl][op][i])
                    res += LHT(op, locks[l][PLACEMENT], r) * workload[wl][op][i]
    return res


def replica_serialization(l,r,wl):
    res = 0
    for o in locks[l][OPS]:
        # if o != op:
        # print(LHT(o, locks[l][PLACEMENT], r))
        # print(workload[wl][op][replicas.index(r)])
        res += LHT(o, locks[l][PLACEMENT], r) * workload[wl][o][replicas.index(r)]
    return res


def operation_parallelism(l,r,wl):
    maxres = 0
    for rep in replicas:
        res = 0
        if rep != r:
            for op in locks[l][OPS]:
                if locks[l][OPS][op][MODE] == SHARED:
                    # print(LHT(op, locks[l][PLACEMENT], rep))
                    # print(workload[wl][op][replicas.index(rep)])
                    res += LHT(op, locks[l][PLACEMENT], rep) * workload[wl][op][replicas.index(rep)]
        if res > maxres:
            maxres = res
    return maxres


def nonparallelism(l,wl):
    maxres = 0
    for r in replicas:
        res = operation_serialization(l,r,wl) + replica_serialization(l,r,wl) - operation_parallelism(l,r,wl)
        if maxres < res:
            maxres = res
    return maxres




# print(LHT('a', CENT, 'paris')) 
# print(operation_serialization('labp11','workloadhoteq')) 
# print(replica_serialization('labp11','paris','a','workloadhoteq')) 
# print(operation_parallelism('labp11','paris','workloadhoteq')) 
# print(operation_serialization('labp21','workloadhoteq')) 
# print(replica_serialization('labp21','paris','a','workloadhoteq')) 
# print(operation_parallelism('labp21','paris','workloadhoteq')) 
# print(nonparallelism('labp21','workloadhoteq')) 
# print(nonparallelism('labp11','workloadhoteq')) 

for wl in workload:
    print(wl)
    print('-'*20)
    for l in locks:
        print(l, ':', nonparallelism(l,wl))