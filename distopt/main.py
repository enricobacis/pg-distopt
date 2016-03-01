#!/usr/bin/env python2

from argparse import ArgumentParser
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

if __name__ == '__main__':
    parser = ArgumentParser(description='Optimize distributed Postgres queries',
        epilog="globs can be used like '../plans/*.xml' (single quotes!)")
    parser.add_argument('PLANS', help='query plan (or multiple using glob')
    parser.add_argument('CONFIGS', help='configuration (or multiple using glob')
    parser.add_argument('--out', default='results.out')
    args = parser.parse_args()

    #PLANS = '../plans/*.xml'
    #CONFIGS = '../configs/*.json'

    plans = [(file, Plan.parse(file)) for file in glob(args.PLANS)]
    configs = [(file, Config.parse(file)) for file in glob(args.CONFIGS)]

    with open(args.out, 'w') as outfile:
        dump(all_plans(plans, configs), outfile)
