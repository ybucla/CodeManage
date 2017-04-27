# -*- coding: utf-8 -*-
"""

Created on 2017/4/27

@author: ybwang
"""
import numpy as np
from sklearn.naive_bayes import GaussianNB
from sklearn.datasets import load_digits
from sklearn.model_selection import learning_curve
from sklearn.model_selection import ShuffleSplit

digits = load_digits()
X, y = digits.data, digits.target

estimator = GaussianNB()

cv = ShuffleSplit(n_splits=1, test_size=0.2, random_state=0)

for train_index, test_index in cv.split(X):
    print("TRAIN:", train_index.shape, "TEST:", test_index.shape)
    X_train, y_train = X[train_index, :], y[train_index]
    X_test, y_test = X[test_index, :], y[test_index]

    estimator.fit(X_train, y_train)

    y_pre_train = estimator.predict(X_train)
    y_pre_test = estimator.predict(X_test)

    print 'X_train accuracy:', np.sum(y_pre_train == y_train) / float(len(y_train))
    print 'X_train estimator.score:', estimator.score(X_train, y_train)
    print 'X_test accuracy:', np.sum(y_pre_test == y_test) / float(len(y_test))
    print 'X_test estimator.score:', estimator.score(X_test, y_test)

train_sizes, train_scores, test_scores = learning_curve(
    estimator, X, y, cv=cv, train_sizes=[1.0])

print 'learning curve score:', train_sizes, train_scores, test_scores


'''
estimator.score(X, y)：返回给定数据的预测准确性，accuracy，为什么不用AUC，可能是因为当存在多类的时候，无法计算AUC
cv = ShuffleSplit(n_splits=1, test_size=0.2, random_state=0)：表示选择test_size=0.2的数据作为测试数据，其他数据作为训练数据，并且随机打乱n_splits=1次，注意n_splits次并不是互补的
train_sizes, train_scores, test_scores = learning_curve(
    estimator, X, y, cv=cv, train_sizes=[1.0])：表示用给定的estimator，X，y，以及随机分好的训练集和测试集cv，我们在训练集中再次选择一定比例数据做训练，然后计算该小部分训练性能以及cv确定的测试集的score，即accuracy
'''