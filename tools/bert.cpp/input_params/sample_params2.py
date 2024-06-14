import pandas as pd
import random 
import time
import sys
import os

random.seed(time.time())

try:
    os.makedirs("batches")
except OSError as exception:
    pass

num_batches = int(sys.argv[1])
batch_size = int(sys.argv[2])

'''
with open("params", 'r') as f:
    lines = f.readlines()

    for i in range(num_batches):
        start = random.randint(0, num_params-batch_size*1000)
        rand_lines = lines[start:start+batch_size*1000]
        with open("batches/params_" + str(batch_size)+"K" + "_" + str(i), "w") as out:
            out.write("".join(line for line in rand_lines))
'''
lines = []
with open("params", 'r') as f:
    lines = f.readlines()
#rand_lines = random.choices(lines, k=batch_size*1000)
#rand_lines = pd.DataFrame(lines).sample(n=batch_size*1000)
#print(rand_lines[0])
#rand_lines.to_csv("batches/params_10K_0")

#idx = random.sample(range(0, 10000), 10000)
#rand_lines = [lines[i] for i in idx]

for i in range(num_batches):
    start = random.randint(0, 321776)
    #print(start)
    #print(type(start))
    rand_lines = lines[start:start+batch_size*1000]
    #rand_lines = lines[85923: 85923+batch_size*1000]
    with open("batches/params_" + str(batch_size)+"K" + "_" + str(i), "w") as out:
        #out.write("".join(line for line in lines[345:10345]))
        out.write("".join(line for line in rand_lines))

'''
for i in range(num_batches):
    
    with open("batches/params_" + str(batch_size)+"K" + "_" + str(i), "w") as out:
        out.write("".join(line for line in rand_lines))
'''