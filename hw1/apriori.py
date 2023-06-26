from itertools import combinations
import sys

db_size = 0
tran_list = []
tot_item_set = set()
min_sup = int(sys.argv[1])
min_sup_freq = 0
frequent_pattern = []

def read_input():
    global db_size, tran_list, min_sup_freq, tot_item_set
    item_list = []
    
    input_file = open(sys.argv[2], 'r')
    while True:
        line = input_file.readline()
        if not line:
            break
        tran = list(map(int,line.split()))
        tran_list.append(tran)
        for item in tran:
            item_list.append(int(item))

    tot_item_set = set(item_list)
    db_size = len(tran_list)
    min_sup_freq = db_size * (min_sup / 100)
    tran_list = list_to_set(tran_list)
    input_file.close()

def list_to_set(item_list):
    result = []
    for item in item_list:
        result.append(set(item))
    return result

def get_cnt(item_set):
    cnt = 0
    for tra in tran_list:
        if item_set == item_set & tra:
            cnt += 1
    return cnt

def get_sup(item_set):
    cnt = get_cnt(item_set)
    if cnt >= min_sup_freq:
        return cnt / db_size
    else:
        return 0

def get_conf(item_set, ass_item_set):
    return get_cnt(item_set | ass_item_set) / get_cnt(item_set)

def self_join(length):
    return list_to_set(list(combinations(tot_item_set, length)))

def pruning(c_item_set):
    result = []

    for cand in c_item_set:
        cnt = 0
        for tra in tran_list:
            if cand == cand & tra:
                cnt += 1
        if cnt >= min_sup_freq:
            result.append(cand)

    return result

def apriori():
    k = 1
    cand = self_join(k)
    while True:
        l = pruning(cand)
        frequent_pattern.extend(l)
        if len(l) == 0:
            break
        k += 1
        cand = self_join(k)


def get_associative(item_set):
    global output_file
    if len(item_set) == 1:
        return

    a = []
    b = []

    for i in range(1, len(item_set)):
        a.extend(list_to_set(list((combinations(item_set, i)))))
        b.extend(list_to_set(list((combinations(item_set, i)))))
    for prev in a:
        for nxt in b:
            if len(prev & nxt) > 0 or (prev | nxt) != item_set:
                continue
            union = prev | nxt
            test = get_sup(union)
            sup = format(test * 100, ".2f")
            conf = format(get_conf(prev, nxt) * 100, ".2f")
            if test == 0:
                continue
            else:
                line = mk_brace(prev) + "\t" + mk_brace(nxt) + "\t" + str(sup) + "\t" + str(conf) + '\n'
                output_file.write(line)

def mk_brace(s):
    s = sorted(s)
    result = "{"
    for item in s:
        result += (str(item) + ",")
    return result[:-1] + "}"

output_file = open(sys.argv[3], 'w')
read_input()
apriori()

for item_set in frequent_pattern:
    get_associative(item_set)

output_file.close()