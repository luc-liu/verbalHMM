import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report

file = 'perspectives_annotated.csv'

candidate_gestures = ['deictic', 'iconic', 'metaphoric']

df = pd.read_csv(file)
df = df[df['gesture'].isin(candidate_gestures)]
print(df.iloc[0, :])

gestures = sorted(df.gesture.unique().tolist())
print(gestures)
for gesture in gestures:
    print('the vocabulary for %s is: ' % gesture)
    gesture_df = df.loc[df['gesture'] == gesture]
    vocab = sorted(gesture_df.annotation.unique().tolist())
    print(vocab)
    print('There counts are: ')
    counts = gesture_df.groupby('annotation').count()
    # plt.bar(range(len(counts.index.values)), counts['gesture'].values / counts['gesture'].values.sum(), tick_label=counts.index.values)
    # plt.title("Vocabulary probability for %s gestures in %s video" % (gesture, file.split('_')[0]))
    # plt.xlabel('Vocabulary')
    # plt.ylabel('Probability')
    # plt.show()
vocabulary = sorted(df.annotation.unique().tolist())
print(vocabulary)

# gestureMap = {k: v for v, k in enumerate(gestures)}
# vocabularyMap = {k: v for v, k in enumerate(vocabulary)}
# df['gesture'] = df['gesture'].map(gestureMap)
# df['annotation'] = df['annotation'].map(vocabularyMap)
# print(df.iloc[0, :])

print(df.shape[0])
nTrains = int(df.shape[0] * 0.6)
nTest = df.shape[0] - nTrains

train = df.head(nTrains)
test = df.tail(nTest)

transitionProb = pd.crosstab(pd.Series(list(train.gesture)[:-1], name='from'),
                             pd.Series(list(train.gesture)[1:], name='to'), normalize=0)
print("transition prob")
print(transitionProb)

emissionProb = pd.crosstab(pd.Series(list(train.gesture), name='gesture'),
            pd.Series(list(train.annotation), name='annotation'), normalize=0)
print("emission prob")
for index, row in emissionProb.iterrows():
    print(row)
missingColumns = list(set(vocabulary) - set(emissionProb.columns.values))
print(missingColumns)

for missingColumn in missingColumns:
    emissionProb[missingColumn] = pd.DataFrame(np.zeros(shape=(len(emissionProb), 1)))

prev = train.loc[train.index[-1], 'gesture']
predictions = []
for index, row in test.iterrows():
    scores = []
    observation = row['annotation']
    for gesture in gestures:
        score = transitionProb.loc[prev, gesture] * emissionProb.loc[gesture, observation]
        scores.append(score)
    print(scores)
    prediction = gestures[scores.index(max(scores))]
    predictions.append(prediction)
    prev = row['gesture']

print(predictions)
print(test.gesture)
accuracy = len([prediction for prediction, truth in zip(predictions, list(test.gesture)) if prediction == truth]) \
           / test.shape[0]
print(accuracy)
report = classification_report(predictions, list(test.gesture))
print(report)