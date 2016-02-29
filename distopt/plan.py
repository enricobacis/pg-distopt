from xml.etree import ElementTree as ET
from utils import get_read_cols
from lxml import objectify
from memo import classkeymemo
import re

class Plan:
    def __init__(self, plan):
        self.plan = plan
        self.children = map(Plan, self.plan.findall('./Plans/Plan'))
        self.totaltime = self['Actual-Total-Time']

    def __getitem__(self, key):
        return self.plan[key]

    def __len__(self):
        return 1 + sum(len(child) for child in self.children)

    @property
    def time(self):
        return self.totaltime - sum(child.totaltime for child in self.children)

    @classmethod
    def parse(cls, filename):
        with open(filename, 'r') as fp:
            xml = re.sub(' xmlns="[^"]+"', '', fp.read(), count=1)
        return cls(objectify.fromstring(xml).find('./Query/Plan'))

    def printtree(self, level=0):
        if not level: print ' TREE '.center(80, '-')
        print '%s%s [Time: %g]' % (' '*(level*4), self['Node-Type'], self.time)
        for child in self.children:
            child.printtree(level=level + 1)

class DistPlan:
    def __init__(self, plan, server, nodecost):
        self.plan, self.server, self.nodecost = plan, server, nodecost
        self.children = []

    @classkeymemo(lambda self, dest: dest['name'] if dest else None)
    def transfer_cost(self, dest=None):
        if not dest or dest == self.server: return 0.0
        through = float(self.server['links'][dest['name']]['throughput'])
        return ( (self.size() *                      # transfer time
                   (self.server['costs']['out'] + dest['costs']['in']))
               + (self.size() / through *            # cpu during transfer
                   (self.server['costs']['cpu'] + dest['costs']['cpu'])) )

    @classkeymemo(lambda self, dest: dest['name'] if dest else None)
    def encryption_cost(self, dest=None):
        if not dest or dest == self.server: return 0.0
        output = set(get_read_cols(self.plan))
        encrypted = output & set(dest['encrypted'])
        try: return ( (self.size() * float(len(encrypted)) / len(output))
                    / dest['performance']['aes'] * self.server['costs']['cpu'] )
        except ZeroDivisionError: return 0.0

    def size(self):
        return int(self.plan['Plan-Rows']) * int(self.plan['Plan-Width']) / 10e6

    def cost(self, dest=None):
        return ( self.nodecost
               + self.transfer_cost(dest)
               + self.encryption_cost(dest)
               + sum(child.cost(dest=self.server)
                     for child in self.children))

    def printtree(self, level=0, dest=None):
        if level == 0: print ' DISTPLAN '.center(80, '-')
        print ('%s%s [Server: %s, Cost: %g, Size: %g MB, Transfer: %g, '
                'Encryption: %g]') % (' ' * (level*4), self.plan['Node-Type'],
                self.server['name'], self.nodecost, self.size(),
                self.transfer_cost(dest), self.encryption_cost(dest))
        for child in self.children:
            child.printtree(level=level+1, dest=self.server)
