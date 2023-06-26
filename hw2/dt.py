import sys
import numpy as np

attributes = []
class_labels = []
training_set = []

class DT:
    def __init__(self, mask):
        self.child = {}
        self.attr_idx = None
        self.mask = set()
        self.mask.update(mask)
        self.class_label = None

    def info(self, data_set):
        entropy = 0
        lavel_values = data_set.T[-1]

        for label in class_labels:
            p_i = np.sum(lavel_values == label)/lavel_values.size
            if p_i != 0:
                entropy += p_i * np.log2(p_i)

        return -entropy

    def info_a(self, data_set, attr_idx):
        entropy = 0
        attr_values = np.unique(data_set.T[attr_idx])

        for attr in attr_values:
            data_subset = data_set[data_set.T[attr_idx] == attr]
            d_i = data_subset.shape[0]/data_set.shape[0]
            entropy += d_i * self.info(data_subset)

        return entropy
    
    def majority_voting(self, data_set):
        major_label = None
        max_cnt = 0
        lavel_values = data_set.T[-1]
        
        for label in class_labels:
            cnt = np.sum(lavel_values == label)
            if cnt > max_cnt:
                max_cnt = cnt
                major_label = label

        return major_label

    def construct(self, data_set):
        if self.info(data_set) == 0:
            self.class_label = data_set[0][-1]
            return
        
        self.class_label = self.majority_voting(data_set)
        if len(self.mask) == attributes.size - 1:
            return

        test_attr_idx = None
        max_info_gain = 0

        for attr_idx in range(attributes.size - 1):
            if attr_idx in self.mask:
                continue
            
            info_gain = self.info(data_set) - self.info_a(data_set, attr_idx)
            if info_gain > max_info_gain:
                max_info_gain = info_gain
                test_attr_idx = attr_idx
        
        new_mask = set()
        new_mask.update(self.mask)
        new_mask.add(test_attr_idx)

        self.attr_idx = test_attr_idx
        attr_values = np.unique(data_set.T[test_attr_idx])
        
        for attr in attr_values:
            data_subset = data_set[data_set.T[test_attr_idx] == attr]
            new_leaf = DT(new_mask)

            new_leaf.construct(data_subset)
            self.child[attr] = new_leaf

    def classify(self, data):
        if self.attr_idx == None:
            return self.class_label
        
        attr = data[self.attr_idx]
        if not (attr in self.child):
            return self.class_label

        return self.child[attr].classify(data)

def read_input():
    global attributes, class_labels, training_set

    file = open(sys.argv[1], 'r')
    attributes = np.array(file.readline().split())
    while True:
        line = file.readline()
        if not line:
            break
        data = np.array(line.split())
        class_labels.append(data[-1])
        training_set.append(data)
    
    training_set = np.array(training_set)
    class_labels = list(set(class_labels))

    file.close()

def build_decision_tree():
    decision_tree = DT(set())
    decision_tree.construct(training_set)
    return decision_tree

def make_string(arr):
    line = ''
    for a in arr:
        line += a + '\t'
    line = line[:-1] + '\n'
    return line

def write_output(decision_tree): 
    test_file = open(sys.argv[2], 'r')
    output_file = open(sys.argv[3], 'w')

    test_file.readline()
    output_file.write(make_string(attributes))

    while True:
        line = test_file.readline()
        if not line:
            break
        data = np.array(line.split())

        class_label = decision_tree.classify(data)
        data = np.append(data, class_label)
        output_file.write(make_string(data))
    
    test_file.close()
    output_file.close()

def main():
    read_input()
    write_output(build_decision_tree())

if __name__ == '__main__':
    main()