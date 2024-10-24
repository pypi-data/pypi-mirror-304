import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsClassifier

model = KNeighborsClassifier(n_neighbors=2)

x = [2, 4, 6, 8]
y = [1, 3, 5, 7]
target = [0, 1, 0, 1]

cord = list(zip(x, y))
plt.scatter(x, y, c=target)
plt.show()

model.fit(cord, target)
new_cord_x = 4.5
new_cord_y = 1.2
cord_list = [(new_cord_x, new_cord_y)]
prediction = model.predict(cord_list)

plt.scatter(x+[new_cord_x], y+[new_cord_y], c=target+[prediction[0]])
plt.show()
