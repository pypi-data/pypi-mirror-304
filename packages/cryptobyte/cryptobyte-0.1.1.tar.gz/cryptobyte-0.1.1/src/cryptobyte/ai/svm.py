from sklearn.datasets import load_iris
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from collections import Counter

dataset = load_iris()
X = dataset['data']
y = dataset['target']

X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2,random_state=50)

model = SVC()
model.fit(X_train,y_train)
prediction = model.predict(X_test)
print(Counter(list(map(lambda x: dataset['target_names'][x],prediction))))

accuracy = accuracy_score(y_test,prediction)
print(accuracy)