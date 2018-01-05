#!/usr/bin/python
from subprocess import Popen, PIPE
import re
import sys

i=0
j=0

REPEAT = 20
missed = 0
while i < REPEAT:
    process = Popen(["python3", "./graph_generator.py", "10", "0.5"], stdout=PIPE)
    (output, err) = process.communicate()
    exit_code = process.wait()

    process = Popen(["python3", "./colann.py", "0.95", "10", "100"], stdin=PIPE, stdout=PIPE)
    (output2, err) = process.communicate(input=output)
    exit_code = process.wait()
    if (exit_code != 0):
        missed += 1
        continue
    else:
        i += 1
    p = re.compile('LPPL: (.*)\n')
    changes = p.match(output2)
    changes = changes.group(1)
    changes = int(changes)

    ppa = re.compile('Cost of solution: (.*)\n')
    cost = ppa.search(output2)
    cost = cost.group(1)
    cost = int(cost)

    print("Changes: " + str(changes) + " cost: " + str(cost))
    #print(output2)
print("Missed: " + str(missed))
