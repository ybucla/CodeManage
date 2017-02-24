# Multiclass Support Vector Machine
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 24 13:19:52 2017

@author: ybwang
"""
import numpy as np
import svm_loss_naive
import svm_loss_vectorized

# load test data
X_dev = np.loadtxt('X_dev.txt') # X_dev.shape = (500L, 3073L)
y_dev = np.loadtxt('y_dev.txt',dtype='int32') # X_dev.shape = (500L,)

# random start weight matrix, Compute the loss and its gradient at W.
np.random.seed(1234)
W = np.random.randn(3073, 10,) * 0.0001 # W.shape = (3073L, 10L), 10个家族，每个家族3073个系数
loss, grad = svm_loss_naive(W, X_dev, y_dev, 0.001)
print loss,grad[0]
# 9.67730025105 [-14.36639208  13.41560776  -8.99955402   8.36593372  18.26639205
#  12.79171719  20.89630984   7.72187818 -12.88302775 -45.20886504]

# or use vectorized format to calculate the loss and dW
loss, grad = svm_loss_naive(W, X_dev, y_dev, 0.001)
print loss,grad[0]
# 9.67730025105 [-14.36639208  13.41560776  -8.99955402   8.36593372  18.26639205
#  12.79171719  20.89630984   7.72187818 -12.88302775 -45.20886504]

