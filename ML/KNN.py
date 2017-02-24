## knn
# classification
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
X = [[0], [1], [2], [3]]
y = [0, 0, 1, 1]
neigh = KNeighborsClassifier(n_neighbors=3)
neigh.fit(X, y) 
# KNeighborsClassifier(...)
print(neigh.predict([[1.1]]))
# [0]
print(neigh.predict_proba([[0.9]]))
# [[ 0.66666667  0.33333333]]


# regression
import numpy as np
from sklearn.neighbors import KNeighborsRegressor
X = [[0], [1], [2], [3]]
y = [0, 1, 0, 2]
neigh = KNeighborsRegressor(n_neighbors=2)
neigh.fit(X,y) 
# NearestNeighbors(algorithm='auto', leaf_size=30, ...)
print(neigh.predict([[1.5]]))
# 0.5, the most nearest points with [1.5] is [1], [2] in X, so the regression result is the mean value of the corresponding y
