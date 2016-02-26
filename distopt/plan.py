import xml.etree.ElementTree as ET
from lxml import objectify
import re

class Plan:
    def __init__(self, plan):
        self.plan = plan
        self.children = map(Plan, self.plan.findall('./Plans/Plan'))
        self.totaltime = self['Actual-Total-Time']

    def __getitem__(self, key):
        return self.plan[key]

    def __len__(self):
        if self.children:
            return 1 + sum(len(child) for child in self.children)
        return 1

    @property
    def time(self):
        return self.totaltime - sum(child.totaltime for child in self.children)

    @classmethod
    def parse(cls, filename):
        with open(filename, 'r') as fp:
            xml = re.sub(' xmlns="[^"]+"', '', fp.read(), count=1)
        return cls(objectify.fromstring(xml).find('./Query/Plan'))

    def printtree(self, level=0):
        if not level: print ' TREE '.center(80, '=')
        print ' ' * (level * 4) + self['Node-Type'], self.time, self.totaltime
        for child in self.children:
            child.printtree(level=level + 1)
