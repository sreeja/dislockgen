import unittest
import os
import granularity

class TestGranularity(unittest.TestCase):
    def test_generate_lattice_sample(self):
        dirname = os.getcwd()
        filename = os.path.join(dirname, 'dislockgen', 'sample2.json')
        granularity_lattice = granularity.generate_lattice(filename)
        i = 0
        for level in granularity_lattice:
            for combo in level:
                i += 1
        assert(i == 1)
        filename = os.path.join(dirname, 'dislockgen', 'sample3.json')
        granularity_lattice = granularity.generate_lattice(filename)
        i = 0
        for level in granularity_lattice:
            for combo in level:
                i += 1
        assert(i == 2)
        filename = os.path.join(dirname, 'dislockgen', 'sample4.json')
        granularity_lattice = granularity.generate_lattice(filename)
        i = 0
        for level in granularity_lattice:
            for combo in level:
                i += 1
        assert(i == 4)

    def test_generate_lattice_auction(self):
        dirname = os.getcwd()
        filename = os.path.join(dirname, 'dislockgen', 'auction3.json')
        granularity_lattice = granularity.generate_lattice(filename)
        i = 0
        for level in granularity_lattice:
            for combo in level:
                i += 1
        assert(i == 8)
        filename = os.path.join(dirname, 'dislockgen', 'auction2.json')
        granularity_lattice = granularity.generate_lattice(filename)
        i = 0
        for level in granularity_lattice:
            for combo in level:
                i += 1
        assert(i == 2)
        filename = os.path.join(dirname, 'dislockgen', 'auction1.json')
        granularity_lattice = granularity.generate_lattice(filename)
        i = 0
        for level in granularity_lattice:
            for combo in level:
                i += 1
        assert(i == 2)

    def test_get_finest_locks_auction(self):
        dirname = os.getcwd()
        locks = granularity.get_finest_locks(os.path.join(dirname, 'dislockgen', 'auction3.json'))
        assert(len(locks) == 5)
        locks = granularity.get_finest_locks(os.path.join(dirname, 'dislockgen', 'auction2.json'))
        assert(len(locks) == 3)
        locks = granularity.get_finest_locks(os.path.join(dirname, 'dislockgen', 'auction1.json'))
        assert(len(locks) == 2)
    
    def test_get_finest_locks_sample(self):
        dirname = os.getcwd()
        locks = granularity.get_finest_locks(os.path.join(dirname, 'dislockgen', 'sample2.json'))
        assert(len(locks) == 1)
        locks = granularity.get_finest_locks(os.path.join(dirname, 'dislockgen', 'sample3.json'))
        assert(len(locks) == 2)
        locks = granularity.get_finest_locks(os.path.join(dirname, 'dislockgen', 'sample4.json'))
        assert(len(locks) == 3)


if __name__ == '__main__':
    unittest.main()