import numpy as np

# A simple one dimensional fast sweeping method implementation used to 
# understand the sweeping process

size = 13
h = 1

line = np.full(size, 100)
line[3] = line[8] = 0

for i in range(1, size-1):
    line[i] = min(min(line[i-1], line[i+1]) + h, line[i])

print(line)

for i in range(size-2, -1, -1):
    line[i] = min(min(line[i-1], line[i+1]) + h, line[i])

print(line)
