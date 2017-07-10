import numpy as np
from collections import defaultdict

dataset_filename = "affinity_dataset.txt"
X = np.loadtxt(dataset_filename)
num_apple_purchases = 0
for sample in X:
    if sample[3] == 1:
        num_apple_purchases += 1
print("{0} people bought apples".format(num_apple_purchases))

valid_rules = defaultdict(int)
invalid_rules = defaultdict(int)
num_occurances = defaultdict(int)
for sample in X:
    for premise in range(5):
        if sample[premise] == 0:
            continue
