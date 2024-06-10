import random 
import time
import sys
import os

random.seed(time.time())

try:
    os.makedirs("batches")
except OSError as exception:
    pass

with open("params", 'r') as f:
    lines = f.readlines()
    for i in range(int(sys.argv[1])):
        rand_lines = random.sample(lines, int(sys.argv[2]))
        with open("batches/params_" + str(int(sys.argv[2])%10)+"K" + "_" + str(i), "w") as out:
            out.write("".join(line for line in rand_lines))
    
