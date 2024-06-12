import random 
import time
import sys
import os

random.seed(time.time)

try:
    os.makedirs("batches")
except OSError as exception:
    pass

num_batches = int(sys.argv[1])
batch_size = int(sys.argv[2])

with open("params", 'r') as f:
    lines = f.readlines()
    for i in range(num_batches):
        rand_lines = random.sample(lines, batch_size*1000)
        with open("batches/params_" + str(batch_size)+"K" + "_" + str(i), "w") as out:
            out.write("".join(line for line in rand_lines))
    
