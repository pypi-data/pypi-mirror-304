from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import accuracy_score
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

data_load = load_iris()
x = data_load['data']
y = data_load['target']

x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.2, random_state=32)
model = DecisionTreeClassifier()
model.fit(x_train, y_train)
prediction = model.predict(x_test)
accuracy = accuracy_score(y_test, prediction)
print(accuracy)

plt.figure(figsize=(20, 10))
plot_tree(model, filled=True, feature_names=x,
            class_names=data_load.target_names)
plt.show()
