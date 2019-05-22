import numpy as np
import rpy2.robjects.numpy2ri
from rpy2.robjects.packages import importr
rpy2.robjects.numpy2ri.activate()

DEFAULT_DATA_DIR = "/Users/laurent/Documents/HeadPoseClustering-master/data/"


files = ['bicycles_script&gestures11082018v4.txt', 'perspectives_script&gestures11082018v4.txt', 'tarmac_script&gestures11082018v4.txt']
data = np.zeros((4, 3))
gesture = ['beats', 'deictic', 'iconic', 'metaphoric']
sequences = []

for file in files:
    text_file = open(DEFAULT_DATA_DIR + file, "r")
    lines = text_file.readlines()
    gestures = []
    sequence = []
    for line in lines:
        if "gesture_major" in line:
            g = line.split()[-1]
            # print(g)
            gestures.append(g)
            # sequence.append(gesture.index(g))
    # transition = list(zip([gestures[i] for i in range(0, len(gestures) - 1)],
    #                        [gestures[i] for i in range(1, len(gestures))]))
    # transitions.append(transition)
    # sequences.append(sequence)
    unique, counts = np.unique(gestures, return_counts=True)
    for gesture in unique:
        if gesture in gestures:
            data[np.where(unique == gesture), files.index(file)] = counts[np.where(unique == gesture)]
    print(unique)
    print(counts)
    print(counts.shape)
print(data)


stats = importr('stats')
res = stats.fisher_test(data, simulate_p_value = True)
print('p-value: {}'.format(res[0][0]))
print(res)
# print(gestures)




# data = np.genfromtxt('/Users/laurent/Documents/HeadPoseClustering-master/data/bicycles_script&gestures11082018v4.txt', dtype=np.str)
#
# gesture = ['beats', 'deictic', 'iconic', 'metaphoric']
#
# data = data.tolist()
#
# data = [d for d in data if d in gesture]
# unique, counts = np.unique(data, return_counts=True)