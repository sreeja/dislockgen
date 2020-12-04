import os
import json
from Lock import Lock


configurations = ['cent', 'clust', 'dist']

def generate_placements(locklist, dirname, appname, gran):
    result = get_placement_configs(locklist, [])
    i = 1
    if not os.path.exists(os.path.join(dirname, appname, gran)):
        os.makedirs(os.path.join(dirname, appname, gran))
    for lst in result:
        content = []
        # print('lst', lst)
        for each in lst:
            # print('each', each)
            l = {'name':each.name, 'param':each.param, 'placement':each.placement}
            content += [l]
        outputfile = os.path.join(dirname, appname, gran, 'locktype'+str(i)+'.json')
        with open(outputfile, 'w') as f:
            json.dump(content, f)
        i += 1
    # return result


def get_placement_configs(locklist, prev):
    if not locklist:
        return prev
    # print('inside get_placement_configs', locklist[0].name)

    locks = []
    for each in configurations:
        # print('inside loop', each)
        newlock = Lock(locklist[0].name)
        newlock.mode = locklist[0].mode
        newlock.ops = locklist[0].ops
        newlock.placement = each
        newlock.param = locklist[0].param
        locks += [newlock]
    
    # print('configed', len(locks))

    if prev:
        result = []
        for new in locks:
            for each in prev:
                # print('combining', len(each), new.name, new.placement)
                result += [each + [new]]
    else:
        result = [[l] for l in locks]

    # print('combined', len(result))

    return get_placement_configs(locklist[1:], result)

