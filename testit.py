#!/usr/bin/python2
from __future__ import print_function
from subprocess import Popen, PIPE

import re
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('init_temp', type=float, help='initial temperature')
args = parser.parse_args()

i=0

REPEAT = 2
missed = 0

graph_sizes = [1000, 5000]
probabs = [0.1, 0.005]
OUTER_LOOP = 100
INNER_LOOP = 1000

for graph_size in graph_sizes:
    for probab in probabs:
        i = 0
        missed = 0
        
        jumps_avg = 0
        cost_avg = 0
        for i in range(REPEAT):
            
            process = Popen(["python3", "./graph_generator.py", str(graph_size), str(probab)], stdout=PIPE)
            (output, err) = process.communicate()
            exit_code = process.wait()

            process = Popen(["python3", "./colann.py", str(args.init_temp), str(OUTER_LOOP), str(INNER_LOOP)], stdin=PIPE, stdout=PIPE)
            (output2, err) = process.communicate(input=output)
            exit_code = process.wait()
            if (exit_code != 0):
                missed += 1
                print("Illegal solution, n =", graph_size, ", p =", probab, ", init temp =", args.init_temp, file=sys.stderr)
                continue

            p = re.compile('LPPL: (.*)\n')
            jumps = p.search(output2)
            jumps = jumps.group(1)
            jumps = float(jumps)
            jumps_avg += jumps

            ppa = re.compile('Cost of solution: (.*)\n')
            cost = ppa.search(output2)
            cost = cost.group(1)
            cost = int(cost)
            cost_avg += cost

        jumps_avg /= REPEAT
        cost_avg /= REPEAT

        
        print("n =", graph_size, ", p =", probab, ", init temp =", args.init_temp, ", jumps =", jumps, "%, cost =", cost, ", missed = ", missed)

