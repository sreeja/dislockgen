import os
import granularity
import placement
import mode

dirname = os.getcwd()
appname = 'sample3'
filename = os.path.join(dirname, appname+'.json')

finest_locks = granularity.get_finest_locks(filename)
granularity_lattice = granularity.generate_lattice(filename)
i = 0
print('result')
print('*'*15)
j = 1
for level in granularity_lattice:
    print('level', str(i))
    i += 1
    for combo in level:
        # print([(v.name, v.ops, v.param) for v in combo.values()])
        print([v.name for v in combo.values()])
        placement.generate_placements([v for v in combo.values()], dirname, appname, 'granular'+str(j))
        mode.generate_mode([v for v in combo.values()], dirname, appname, 'granular'+str(j))
        j += 1

# for each in granularity_lattice:
#     generate_modes(each, dirname)
#     generate_placements(each, dirname)
