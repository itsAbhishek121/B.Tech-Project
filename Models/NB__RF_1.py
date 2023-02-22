import pandas as pd

df = pd.read_csv("merged.csv", encoding='utf-8')

df["Result"] = df[df.columns[0:4]].apply(lambda x: ' '.join(x.dropna().astype(str)),axis=1)


# Vectorization

from sklearn.feature_extraction.text import TfidfVectorizer

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

# Model
from sklearn.naive_bayes import GaussianNB  
from sklearn.ensemble import RandomForestClassifier


from sklearn.model_selection import train_test_split

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(x_train, y_train, test_size=0.3, random_state=1)

# Create the Naive Bayes classifier
gnb = GaussianNB()

# Initialize the Random Forest Classifier
# rfc = RandomForestClassifier()

# train the classifier on the training data
gnb.fit(X_train, y_train)

# Fit the model to the training data
# rfc.fit(x_train, y_train)

# Evaluate the model on the testing data
y_pred = gnb.predict(X_test)

# y_pred = rfc.predict(X_test)

# evaluate the accuracy of the classifier
accuracy = (y_pred == y_test).sum() / len(y_test)
print('Accuracy: ', accuracy)