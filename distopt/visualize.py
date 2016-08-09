#!/usr/bin/env python2

import matplotlib.pyplot as plt
from argparse import ArgumentParser
from operator import itemgetter
from numpy import arange
from json import load

def generate(outfile):
    results = []
    for planfile, data in sorted(list(load(outfile).items()), key=itemgetter(0)):
        results.append([max(0, data[k]) for k in sorted(data.keys())])
    bench = list(zip(*results))

    N = min(len(b) for b in bench)     # number of plans in benchmarks
    plt.xlim(.5, N + 1.5)              # set the graph x limits
    cm = plt.get_cmap('YlGnBu')        # get colormap
    xs = arange(1, N + 1)              # xs to use for the bar plot
    width = .8 / len(bench)            # width of a single bar

    for i, ys in enumerate(bench):
        plt.bar(xs + i * width, ys, width=width,
               color=cm(.2 + (.8 * i / len(bench))))

if __name__ == '__main__':
    parser = ArgumentParser(description='Visualize the output of main.py')
    parser.add_argument('FILE', type=file, help='the main.py output file')
    args = parser.parse_args()
    generate(args.FILE)
    plt.show()
