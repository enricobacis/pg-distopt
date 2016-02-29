from analyzer import best
from config import Config
from plan import Plan

plan = Plan.parse('../plans/2.xml')
plan.printtree()

for bench in xrange(5, 8):
    print '\n' + (' BENCH #%d ' % bench).center(80, '=')
    config = Config.parse('../configs/bench%d.json' % bench)
    distplan = best(plan, config)
    print 'Best cost:', distplan.cost(dest=config['CL1'])
    distplan.printtree(dest=config['CL1'])
