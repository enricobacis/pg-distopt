from json import load

class Config:
    def __init__(self, nodes):
        self.nodes = nodes

    @classmethod
    def parse(cls, filename):
        with open(filename, 'r') as fp:
            return cls(load(fp)['nodes'])
