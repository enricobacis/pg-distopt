from analyzer import best
from config import Config
from plan import Plan

plan   = Plan.parse('../plans/4.xml')
plan.printtree()

for bench in xrange(5, 8):
    print '\n' + (' BENCH #%d ' % bench).center(80, '=')
    config = Config.parse('../configs/bench%d.json' % bench)
    distplan = best(plan, config, dest='CL1')
    print 'Best cost:', distplan.cost
    distplan.printtree()
