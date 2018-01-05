#!/usr/bin/python
from subprocess import Popen, PIPE
import re
import sys

i=0

REPEAT = 20
missed = 0

graph_sizes = [10, 15]
probabs = [0.5, 0.6]
INIT_TEMP = 10
OUTER_LOOP = 10
INNER_LOOP = 100

for graph_size in graph_sizes:
    for probab in probabs:
        i = 0
        missed = 0
        print("GRAPH SIZE: " + str(graph_size) + " probability: " + str(probab))
        while i < REPEAT:
            process = Popen(["python3", "./graph_generator.py", str(graph_size), str(probab)], stdout=PIPE)
            (output, err) = process.communicate()
            exit_code = process.wait()

            process = Popen(["python3", "./colann.py", str(INIT_TEMP), str(OUTER_LOOP), str(INNER_LOOP)], stdin=PIPE, stdout=PIPE)
            (output2, err) = process.communicate(input=output)
            exit_code = process.wait()
            if (exit_code != 0):
                missed += 1
                continue
            else:
                i += 1

            p = re.compile('LPPL: (.*)\n')
            changes = p.search(output2)
            changes = changes.group(1)
            changes = float(changes)

            ppa = re.compile('Cost of solution: (.*)\n')
            cost = ppa.search(output2)
            cost = cost.group(1)
            cost = int(cost)

            print("Jumps " + str(changes) + "% cost: " + str(cost))
        print("Missed: " + str(missed))
