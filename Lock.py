class Lock:
    def __init__(self, name):
        self.name = name
        self.mode = '' #sharex, mutex
        self.ops = {} #key:opname, value:mode
        self.placement = '' # cent, clsut, dist
        self.param = ''