# -*- coding: utf-8 -*-
"""

Created on 2017/4/14

@author: ybwang
"""
import numpy as np
from scipy.optimize import minimize
from sklearn.metrics import roc_curve, roc_auc_score
import matplotlib.pyplot as plt


def rosen(x):
    return sum(100.0 * (x[1:] - x[:-1] ** 2.0) ** 2.0 + (1 - x[:-1]) ** 2.0)


def loss(w, data):
    x = data[:, :-1]
    y = data[:, -1]
    w = np.array([w])
    p = (1.0 / (1.0 + np.exp(-x.dot(w.T)))).flatten()
    mle = -np.sum(y * np.log(p + 1e-9) + (1 - y) * np.log(1 - p + 1e-9))
    return mle


def readTSV(tsvfile, skipcolumn=True, skiprow=True):
    data = []
    n = 0
    with open(tsvfile, 'r') as f:
        for line in f:
            if n == 0 and skiprow == True:
                n += 1
                continue
            ele = line.rstrip().split('\t')
            if skipcolumn == True: ele = ele[1::]
            data.append(ele)
    return np.float64(np.array(data))


data = readTSV('E:/Pycharm/code/hp/dataPLS.txt')

# loss(np.array([np.repeat(1, 62)]), np.hstack((np.ones((data.shape[0], 1)), data)))

x0 = np.repeat(0, 62).tolist()
d = np.hstack((np.ones((data.shape[0], 1)), data))
# print loss(x0, d)
res = minimize(loss, x0, args=(d,), method='BFGS')

w = np.array([res.x] ).reshape((-1,1))
p = 1 / (1 + np.exp(-d[:,:-1].dot(w)))
auc = roc_auc_score(d[:,-1].flatten(), p.flatten())
fpr, tpr, threshold = roc_curve(d[:,-1].flatten(), p.flatten(),pos_label=1)
plt.plot(fpr,tpr,'r-')
plt.legend(['AUC = ' +str(auc)], loc=4)
plt.show()
