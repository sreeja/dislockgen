import os
import granularity


dirname = os.path.join('/', 'Users', 'snair', 'works',
                      'dislock-experiments', 'dislockgen')

filename = os.path.join(dirname, 'sample4.json')

granularity_lattice = granularity.generate_lattice(filename)
i = 0
print('result')
print('*'*15)
for level in granularity_lattice:
    print('level', str(i))
    i += 1
    for combo in level:
        # print([(v.name, v.ops, v.param) for v in combo.values()])
        print([v.name for v in combo.values()])

# for each in granularity_lattice:
#     generate_modes(each, dirname)
#     generate_placements(each, dirname)


