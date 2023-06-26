import sys, math
import numpy as np

data = []
label = dict()
filename = ''
n = 0
eps = 0
minpts = 0

def calc_dist(a, b):
    x = (float(a[1]) - float(b[1])) ** 2
    y = (float(a[2]) - float(b[2])) ** 2
    return math.sqrt(x + y)

def find_neighbor(a):
    neighbor = []
    for b in data:
        if a[0] == b[0]:
            continue
        if calc_dist(a, b) <= eps:
            neighbor.append(b)
    return neighbor

def DB_scan():
    cnt = 0
    for p in data:
        if p[0] in label:
            continue
        neighbor = find_neighbor(p)
        if len(neighbor)+1 < minpts:
            label[p[0]] = 'noise'
            continue
        label[p[0]] = cnt

        while True:
            new_neighbor = neighbor
            for q in neighbor:
                if q[0] in label:
                    if label[q[0]] == 'noise':
                        label[q[0]] = cnt
                    else:
                        continue
                neigh_q = find_neighbor(q)
                label[q[0]] = cnt
                if len(neigh_q)+1 < minpts:
                    continue
                
                new_neighbor = np.concatenate((new_neighbor, neigh_q))
                
            if len(neighbor) == len(new_neighbor):
                break
            else:
                neighbor = new_neighbor
                    
        cnt += 1

    cluster = []
    for i in range(n):
        tmp = []
        for p in data:
            if label[p[0]] == i:
                tmp.append(p[0])
        cluster.append(tmp)

    cnt = 0
    for c in cluster:
        output_filename = filename + '_cluster_' + str(cnt) + '.txt'
        write_output(output_filename, c)
        cnt += 1

def read_input():
    file = open(sys.argv[1], 'r')
    while True:
        line = file.readline()
        if not line:
            break
        point = np.array(line.split())
        data.append(point)
    file.close()

def write_output(output_filename, cluster):
    output_file = open(output_filename, 'w')
    for c in cluster:
        output_file.write(str(c) + '\n')
    output_file.close()

def main():
    global filename, n, eps, minpts
    filename = sys.argv[1][:-4]
    n, eps, minpts = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
    read_input()
    DB_scan()

if __name__ == '__main__':
    main()
