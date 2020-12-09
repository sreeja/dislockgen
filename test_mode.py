import unittest
import os
import mode
from Lock import Lock

class TestMode(unittest.TestCase):
    def test_generate_mode(self):
        pass

    def test_get_parts(self):
        for lock in ['operationa_operationb', 'operationa_operationb_operationc', 'operationa_operationb_operationc_operationd']:
            parts = mode.get_parts(lock, os.getcwd(), 'sample4')
            assert(len(parts) == 2)
            ops = lock.split('_')
            assert(len(parts[0]) >= len(ops)%2)
            assert(len(parts[1]) >= len(ops)%2)
            assert(len(parts[0]) + len(parts[1]) == len(ops))

    def test_get_parts_lattice(self):
        import granularity
        granularity_lattice = granularity.generate_lattice(os.path.join(os.getcwd(), 'sample4.json'))
        for level in granularity_lattice:
            for combo in level:
                for each in combo:
                    print(each)
                    parts = mode.get_parts(each, os.getcwd(), 'sample4')
                    ops = each.split('_')
                    assert(len(parts[0]) >= len(ops)%2)
                    assert(len(parts[1]) >= len(ops)%2)
                    assert(len(parts[0]) + len(parts[1]) == len(ops))
                    for op in ops:
                        assert(op in parts[0] or op in parts[1])


if __name__ == '__main__':
    unittest.main()