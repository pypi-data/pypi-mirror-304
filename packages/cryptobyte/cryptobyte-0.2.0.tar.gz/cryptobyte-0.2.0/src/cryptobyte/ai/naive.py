from sklearn.datasets import load_iris
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from collections import Counter

dataset = load_iris()
x = dataset['data']
y = dataset['target']

x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.2,random_state=40)
model = GaussianNB()
model.fit(x_train,y_train)
prediction = model.predict(x_test)
print(Counter(list(map(lambda x: dataset['target_names'][x], prediction))))
accuracy = accuracy_score(y_test,prediction)
print(accuracy)