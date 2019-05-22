import numpy as np
import rpy2.robjects.numpy2ri
from rpy2.robjects.packages import importr
rpy2.robjects.numpy2ri.activate()
import pickle
import pandas as pd

DEFAULT_DATA_DIR = "/Users/laurent/Documents/HeadPoseClustering-master/data/"

# preprocess bicycle file
bicycle = 'bicycles_script&gestures11082018v4.txt'
text_file = open(DEFAULT_DATA_DIR + bicycle, "r")
lines = text_file.readlines()
newlines = []
for line in lines:
    s = line.split()
    s.pop(2)
    s.pop(3)
    # for ss in s:
    #     ss = ss.replace('"', '')
    # print(s[3])
    newline = " ".join(map(str, s))
    newline = newline.replace('"', '')
    newlines.append(newline)

outF = open(DEFAULT_DATA_DIR + "bicycles.txt", "w")
for line in newlines:
  # write line to output file
  outF.write(line)
  outF.write("\n")
outF.close()




files = ['bicycles.txt', 'perspectives_script&gestures11082018v4.txt', 'tarmac_script&gestures11082018v4.txt']
gesture = ['beats', 'deictic', 'iconic', 'metaphoric']
data = {}


for file in files:
    text_file = open(DEFAULT_DATA_DIR + file, "r")
    lines = text_file.readlines()
    g_start = []
    g_end = []
    gestures = []
    s_start = []
    s_end = []
    scripts = []
    for line in lines:
        if "gesture_major" in line:
            g = line.split()
            g_start.append(g[1])
            g_end.append(g[2])
            # print(g)
            gestures.append(g[4])
        elif "script" in line:
            s = line.split()
            s_start.append(s[1])
            s_end.append(s[2])
            scripts.append(s[4: ])

    if "bicycles" in file:
        data["bicycles"] = [g_start, g_end, gestures, s_start, s_end, scripts]
    elif "perspectives" in file:
        data["perspectives"] = [g_start, g_end, gestures, s_start, s_end, scripts]
    elif "tarmac" in file:
        data["tarmac"] = [g_start, g_end, gestures, s_start, s_end, scripts]

# print(data["bicycles"])
# find words that correspond with each gesture
results = {}
for key, value in data.items():
    [g_start, g_end, gestures, s_start, s_end, scripts] = value
    pair = []
    for i in range(0, len(g_start)):
        gestureStart = int(g_start[i])
        a = 0
        b = 0
        for j in range(0, len(s_start)):
            scriptStart = int(s_start[j])
            if gestureStart < scriptStart:
                a = j - 1
                break
        if a < 0:
            a = 0
        gestureEnd = int(g_end[i])
        for j in range(a, len(s_end)):
            scriptEnd = int(s_end[j])
            if gestureEnd > scriptEnd:
                b = j - 1
                break
        if b < a:
            b = a
        # print(a)
        # print(b)
        # print(gestures[i])
        flat_scripts = [item for sublist in scripts[a: b + 1] for item in sublist]
        # print(flat_scripts)
        pair.append(gestures[i] + " ^ " + ' '.join(flat_scripts))
    results[key] = pair
# print(results["bicycles"][0])
# print(results["bicycles"][1])
# print(results["perspectives"][0])
# print(results["tarmac"][0])

files = ['bicycles_gesture_words_pair.txt', 'perspectives_gesture_words_pair.txt', 'tarmac_gesture_words_pair.txt']

for file in files:
    outF = open(DEFAULT_DATA_DIR + file, "w")
    for line in results[file.split("_")[0]]:
        # write line to output file
        outF.write(line)
        outF.write("\n")
    outF.close()


# poll together all words related to a specific gesture
outFile = open(DEFAULT_DATA_DIR + "aggregate.txt", "w")
for key, value in results.items():
    outFile.write("*********Aggregate Gesture-Word Table for Video " + key + "*********")
    outFile.write("\n\n")
    aggregate = {}
    for g in gesture:
        words = []
        aggregate[g] = words
    for line in value:
        l = line.split(" ^ ")
        aggregate[l[0]].append(l[1])
    for k, v in aggregate.items():
        outFile.write(k + ": ")
        outFile.write(' '.join(v))
        outFile.write("\n\n")
    outFile.write("\n\n\n\n")
outFile.close()


# using new timecodes
# parse the new timecode file to produce s_start, s_end, word
files = ["bicycles_timecoded.txt", "perspectives_timecoded.txt", "tarmac_timecoded.txt"]
timecodeddata = {}

for file in files:
    text_file = open(DEFAULT_DATA_DIR + file, "r")
    lines = text_file.readlines()
    s_start = []
    s_end = []
    word = []
    for line in lines:
        if "Word: " in line:
            codes = line.split(",")
            for code in codes:
                if "Word: " in code:
                    word.append(code.split(":")[1].strip())
                elif "start_time" in code:
                    s_start.append(code.split(":")[1].strip())
                elif "end_time" in code:
                    s_end.append(code.split(":")[1].strip())

    if "bicycles" in file:
        [g_start, g_end, gestures, d1, d2, d3] = data["bicycles"]
        timecodeddata["bicycles"] = [g_start, g_end, gestures, s_start, s_end, word]
        print(timecodeddata["bicycles"])
    elif "perspectives" in file:
        [g_start, g_end, gestures, d1, d2, d3] = data["perspectives"]
        timecodeddata["perspectives"] = [g_start, g_end, gestures, s_start, s_end, word]
        print(timecodeddata["perspectives"])
    elif "tarmac" in file:
        [g_start, g_end, gestures, d1, d2, d3] = data["tarmac"]
        timecodeddata["tarmac"] = [g_start, g_end, gestures, s_start, s_end, word]
        print(timecodeddata["tarmac"])

# using new timecodes
# find words that correspond with each gesture
results = {}
result_dicts = {}
for key, value in timecodeddata.items():
    [g_start, g_end, gestures, s_start, s_end, word] = value
    pair = []
    dicts = []
    for i in range(0, len(g_start)):
        gestureStart = int(g_start[i])
        a = 0
        b = 0
        # print("gesture start: %d" % gestureStart)
        for j in range(0, len(s_start)):
            scriptStart = float(s_start[j]) * 1000
            # print("script start: %d" % scriptStart)
            if gestureStart < scriptStart:
                a = j - 1
                break
            else:
                a = j
        if a < 0:
            a = 0
        gestureEnd = int(g_end[i])
        # print("gesture end: %d" % gestureEnd)
        for j in range(a, len(s_end)):
            scriptEnd = float(s_end[j]) * 1000
            # print("script end: %d" % scriptEnd)
            b = j
            if gestureEnd <= scriptEnd and gestureEnd > float(s_start[j]) * 1000:
                break
            if gestureEnd >= scriptEnd and j + 1 < len(s_end) and gestureEnd < float(s_start[j + 1]) * 1000:
                break
            elif gestureEnd >= scriptEnd and j + 1 >= len(s_end):
                break
        # print("gesture: " + gestures[i])
        if b < a:
            b = a
        # print(a)
        # print(b)
        # print(gestures[i])
        # print("a: %d, b: %d" % (a, b))
        flat_scripts = word[a: b + 1]
        # print(' '.join(flat_scripts))
        # print(flat_scripts)
        pair.append(gestures[i] + " ^ " + ' '.join(flat_scripts))
        pairdict = {}
        pairdict['gesture'] = gestures[i]
        pairdict['words'] = ' '.join(flat_scripts)
        pairdict['annotation'] = ''
        dicts.append(pairdict)
    results[key] = pair
    result_dicts[key] = dicts

files = ['bicycles_gesture_words_pair_timecoded.txt', 'perspectives_gesture_words_pair_timecoded.txt', 'tarmac_gesture_words_pair_timecoded.txt']

print(result_dicts)

for file in files:
    outF = open(DEFAULT_DATA_DIR + file, "w")
    for line in results[file.split("_")[0]]:
        # write line to output file
        outF.write(line)
        outF.write("\n")
    outF.close()


for video, annotationList in result_dicts.items():
    print('*****************' + video)
    df = pd.DataFrame.from_records(annotationList)
    columnsTitles = ['gesture', 'words', 'annotation']
    df = df.reindex(columns=columnsTitles)
    df.to_csv(video + '.csv')
    print(df)

# poll together all words related to a specific gesture
aggregate_bicycles = {}
aggregate_perspectives = {}
aggregate_tarmac = {}
agg = [aggregate_bicycles, aggregate_perspectives, aggregate_tarmac]
index = 0
outFile = open(DEFAULT_DATA_DIR + "aggregate_timecoded.txt", "w")
for key, value in results.items():
    outFile.write("*********Aggregate Gesture-Word Table for Video " + key + "*********")
    outFile.write("\n\n")
    aggregate = {}
    for g in gesture:
        words = []
        aggregate[g] = words
    for line in value:
        l = line.split(" ^ ")
        aggregate[l[0]].append(l[1])
    for k, v in aggregate.items():
        outFile.write(k + ": ")
        outFile.write(' '.join(v))
        outFile.write("\n\n")
    outFile.write("\n\n\n\n")
    agg[index] = aggregate
    index += 1
outFile.close()

pickle.dump(agg, open("aggregate.p", "wb"))
            # sequence.append(gesture.index(g))
    # transition = list(zip([gestures[i] for i in range(0, len(gestures) - 1)],
    #                        [gestures[i] for i in range(1, len(gestures))]))
    # transitions.append(transition)
    # sequences.append(sequence)
#     unique, counts = np.unique(gestures, return_counts=True)
#     for gesture in unique:
#         if gesture in gestures:
#             data[np.where(unique == gesture), files.index(file)] = counts[np.where(unique == gesture)]
#     print(unique)
#     print(counts)
#     print(counts.shape)
# print(data)