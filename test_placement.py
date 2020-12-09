import unittest
import os
import placement
from Lock import Lock

class TestPlacement(unittest.TestCase):
    def test_get_placement_configs(self):
        lst = []
        for i in range(3):
            l = Lock('op'+str(i))
            lst += [l]
        assert(len(placement.get_placement_configs(lst, [])) == 27)

    def test_generate_placements(self):
        dirname = os.getcwd() + 'dislockgen'
        appname = 'test'
        gran = 'granularity1'
        lst = []
        for i in range(3):
            l = Lock('op'+str(i))
            lst += [l]
        placement.generate_placements(lst, dirname, appname, gran)
        for i in range(1, 28):
            print(i)
            assert(os.path.exists(os.path.join(dirname, appname, gran, 'locktype'+str(i)+'.json')))

if __name__ == '__main__':
    unittest.main()