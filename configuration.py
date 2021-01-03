import os
import granularity
import placement
import mode


def get_all_configurations(appname):
    dirname = os.getcwd()
    filename = os.path.join(dirname, appname+'.json')

    finest_locks = granularity.get_finest_locks(filename)
    granularity_lattice = granularity.generate_lattice(filename)
    print('result')
    print('*'*15)
    lattice_dimensions = {}
    i = 0
    j = 1
    for level in granularity_lattice:
        print('level', str(i))
        lattice_dimensions[i] = {}
        for combo in level:
            # print([(v.name, v.ops, v.param) for v in combo.values()])
            print([v.name for v in combo.values()])
            placements = placement.generate_placements([v for v in combo.values()], dirname, appname, 'granular'+str(j))
            modes = mode.generate_mode([v for v in combo.values()], dirname, appname, 'granular'+str(j))
            key = '-'.join(sorted([v.name for v in combo.values()]))
            lattice_dimensions[i][key] = (modes, placements)
            j += 1
        i += 1
    return lattice_dimensions


def get_optimal_configuration(appname, lattice_dimensions):
    pass



appname = 'sample3'
lattice_dimensions = get_all_configurations(appname)
optimal_config = get_optimal_configuration(appname, lattice_dimensions)
print('Optimal configuration')
# print('Granularity:', optimal_config[0], 'Mode:', optimal_config[1], 'Placement:', optimal_config[2])
