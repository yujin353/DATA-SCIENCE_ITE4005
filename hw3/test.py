import numpy as np
import math

label = dict()

label[3] = 'noise'
label[5] = 0
label[6] = 0
label[1] = 0
label[15] = 1
label[16] = 1
label[11] = 1

label[5] = 'noise'

print(label)

for i in label:
    if label[i] == 'noise': #1:
        print(i)

a = [1,2,3,4]
b = [3,4,5,6]

print(list(set(a+b)))

a = np.concatenate((a,b))
print(a)

for i in a:
    print(i)

def calc_dist(a, b):
    x = (float(a[1]) - float(b[1])) ** 2
    y = (float(a[2]) - float(b[2])) ** 2
    return math.sqrt(x + y)

p = [0, 3,4]
q = [1, 0,0]

if calc_dist(p,q) >= 5:
    print('yes')

print('p~q', calc_dist(p,q))
