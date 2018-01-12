#!/usr/bin/python2
from __future__ import print_function
from subprocess import Popen, PIPE

import re
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('init_temp', type=float, help='initial temperature')
parser.add_argument('outer_loop', type=int, help='initial temperature')
parser.add_argument('inner_loop', type=int, help='initial temperature')
parser.add_argument('graph_size', type=int, help='graph size')
args = parser.parse_args()

REPEAT = 50

OUTER_LOOP = args.outer_loop
INNER_LOOP = args.inner_loop

missed = 0

jumps_begin_avg = jumps_end_avg = cost_avg = 0.0
i = 0
while i < REPEAT:

    process = Popen(["python3", "./cycle_generator.py", str(args.graph_size)], stdout=PIPE)
    output, _ = process.communicate()

    process = Popen(["./colann", str(args.init_temp), str(OUTER_LOOP), str(INNER_LOOP)], stdin=PIPE, stdout=PIPE)
    output2, _ = process.communicate(input=output)
    exit_code = process.wait()
    if exit_code != 0:
        missed += 1
        print("Illegal solution, n =", args.graph_size, "init temp =", args.init_temp, file=sys.stderr)
        continue

    p = re.compile('Accepted upwards jumps \(highest temp\): (.*)\n')
    jumps_begin = p.search(output2)
    jumps_begin = jumps_begin.group(1)
    jumps_begin = 100.0 * float(jumps_begin)
    jumps_begin_avg += jumps_begin

    p = re.compile('Accepted upwards jumps \(lowest temp\): (.*)\n')
    jumps_end = p.search(output2)
    jumps_end = jumps_end.group(1)
    jumps_end = 100.0 * float(jumps_end)
    jumps_end_avg += jumps_end

    ppa = re.compile('Cost of solution: (.*)\n')
    cost = ppa.search(output2)
    cost = cost.group(1)
    cost = int(cost)
    cost_avg += cost

    i += 1
    # print(i, "/", REPEAT, file=sys.stderr)

jumps_begin_avg /= REPEAT
jumps_end_avg /= REPEAT
cost_avg /= REPEAT


print("n =", args.graph_size, ", init temp =", args.init_temp, ", jumps (highest temp) =", jumps_begin_avg, "%, jumps (lowest temp) =", jumps_end_avg, "%, cost =", cost_avg, ", missed = ", missed)
