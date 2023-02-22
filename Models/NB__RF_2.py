import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

# Models
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier

# Training

df = pd.read_csv("merged.csv", encoding='utf-8')

df["Result"] = df[df.columns[0:4]].apply(lambda x: ' '.join(x.dropna().astype(str)),axis=1)


# Vectroize

v = TfidfVectorizer()
x_train = v.fit_transform(df["Result"])
x_train = x_train.toarray()

n_feat = x_train.shape[1]
y_train = []

dict = {}
i = 1
for item in df["Tag"]:
    if item not in dict:
        dict[item] = i
        i+=1

for j in range(len(df["Tag"])):
     y_train.append(dict[df["Tag"][j]])


# create the Naive Bayes classifier
gnb = GaussianNB()

# Initialize the Random Forest Classifier
# rfc = RandomForestClassifier()

# train the classifier on the training data
gnb.fit(x_train, y_train)


# Testing

df = pd.read_csv("data6.csv", encoding='utf-8', on_bad_lines='skip')

df["Result"] = df[df.columns[0:4]].apply(lambda x: ' '.join(x.dropna().astype(str)),axis=1)

# Vectroize
v = TfidfVectorizer()
x_test = v.fit_transform(df["Result"])
x_test = x_test.toarray()
n_feat1 = x_test.shape[1]
y_test = []
x_test_final = []
if (n_feat1 < n_feat):
    l = np.zeros(n_feat - n_feat1)
    for i in range(x_test.shape[0]):
        arr = np.concatenate((x_test[i], l))
        x_test_final.append(arr)

elif (n_feat1 > n_feat):
    z = n_feat1 - n_feat
    for i in range(x_test.shape[0]):
        arr = x_test[i][0:z]
        x_test_final.append(arr)
else:
    x_test_final = x_test


dicty = {}
i = 1
for item in df["Tag"]:
    dicty[item] = dict[item]

for j in range(len(df["Tag"])):
    y_test.append(dicty[df["Tag"][j]])


# make predictions on the test data
y_pred = gnb.predict(x_test_final)

# y_pred = rfc.predict(x_test_final)

# evaluate the accuracy of the classifier
accuracy = (y_pred == y_test).sum() / len(y_test)
print('Accuracy: ', accuracy)





