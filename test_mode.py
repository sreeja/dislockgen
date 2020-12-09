import unittest
import os
import mode
from Lock import Lock

class TestMode(unittest.TestCase):
    def test_generate_mode(self):
        import granularity
        locklist = granularity.get_finest_locks(os.path.join(os.getcwd(), 'dislockgen', 'sample4.json'))
        mode.generate_mode(list(locklist.values()), os.path.join(os.getcwd(), 'dislockgen'), 'sample4', 'granular1')
        for i in range(1, 28):
            assert(os.path.exists(os.path.join(os.getcwd(), 'dislockgen', 'sample4', 'granular1', 'oplock'+str(i)+'.json')))

    def test_get_mode_configs(self):
        import granularity
        locklist = granularity.get_finest_locks(os.path.join(os.getcwd(), 'dislockgen', 'sample4.json'))
        assert(len(mode.get_mode_configurations(list(locklist.values()), [], os.path.join(os.getcwd(), 'dislockgen'), 'sample4')) == 27)

    def test_get_parts(self):
        for lock in ['operationa_operationb', 'operationa_operationb_operationc', 'operationa_operationb_operationc_operationd']:
            parts = mode.get_parts(lock, os.path.join(os.getcwd(), 'dislockgen'), 'sample4')
            assert(len(parts) == 2)
            ops = lock.split('_')
            assert(len(parts[0]) >= len(ops)%2)
            assert(len(parts[1]) >= len(ops)%2)
            assert(len(parts[0]) + len(parts[1]) == len(ops))

    def test_get_parts_lattice(self):
        import granularity
        granularity_lattice = granularity.generate_lattice(os.path.join(os.getcwd(), 'dislockgen', 'sample4.json'))
        for level in granularity_lattice:
            for combo in level:
                for each in combo:
                    parts = mode.get_parts(each, os.path.join(os.getcwd(), 'dislockgen'), 'sample4')
                    ops = each.split('_')
                    assert(len(parts[0]) >= len(ops)%2)
                    assert(len(parts[1]) >= len(ops)%2)
                    assert(len(parts[0]) + len(parts[1]) == len(ops))
                    for op in ops:
                        assert(op in parts[0] or op in parts[1])


if __name__ == '__main__':
    unittest.main()