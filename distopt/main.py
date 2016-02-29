from analyzer import best
from config import Config
from plan import Plan
from glob import glob
from json import dump

def single(plan, config):
    distplan = best(plan, config)
    cost = distplan.cost(dest=config['CL1'])
    print 'Best cost:', cost
    distplan.printtree(dest=config['CL1'])
    return cost

def all_configs(plan, configs):
    results = {}
    for configfile, config in configs:
        print '\n' + (' BENCH %s ' % configfile).center(80, '-')
        results[configfile] = single(plan, config)
    return results

def all_plans(plans, configs):
    results = {}
    for planfile, plan in plans:
        print '\n' + (' PLAN %s ' % planfile).center(80, '=')
        plan.printtree()
        results[planfile] = all_configs(plan, configs)
    return results

plan_pattern = '../plans/*.xml'
config_pattern = '../configs/*.json'

plans = [(file, Plan.parse(file)) for file in glob(plan_pattern)]
configs = [(file, Config.parse(file)) for file in glob(config_pattern)]

with open('results.out', 'w') as outfile:
    dump(all_plans(plans, configs), outfile)
