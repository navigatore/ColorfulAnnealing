#!/usr/bin/python
from subprocess import Popen, PIPE
import re
import sys

i=0
j=0

REPEAT = 1
while i < REPEAT:
    process = Popen(["python3", "./graph_generator.py", "10", "0.5"], stdout=PIPE)
    (output, err) = process.communicate()
    exit_code = process.wait()

    process = Popen(["python3", "./colann.py"], stdin=PIPE, stdout=PIPE)
    (output2, err) = process.communicate(input=output)
    exit_code = process.wait()
    i += 1

    p = re.compile('LPPL: (.*)\n')
    changes = p.match(output2)
    changes = changes.group(1)
    changes = int(changes)
    print("Changes: " + str(changes))
    #print(str(i) + ": " + str(exit_code))
