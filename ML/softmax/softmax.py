# Softmax Machine for Multiclass
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 24 13:19:52 2017

@author: ybwang
"""
import numpy as np
from softmax_loss_naive import softmax_loss_naive
from softmax_loss_vectorized import softmax_loss_vectorized

# load test data
X_dev = np.loadtxt('X_dev.txt') # X_dev.shape = (500L, 3073L)
y_dev = np.loadtxt('y_dev.txt',dtype='int32') # X_dev.shape = (500L,)

# random start weight matrix, Compute the loss and its gradient at W.
np.random.seed(1234)
W = np.random.randn(3073, 10,) * 0.0001 # W.shape = (3073L, 10L), 10个家族，每个家族3073个系数
loss, grad = softmax_loss_naive(W, X_dev, y_dev, 0.001)
print loss, grad[0]
# 2.42589425817 [-1.97135983  0.13098175 -0.49688204  1.34860066  1.53381781  2.48150556
#  1.61289219  1.90183472 -1.1548424  -5.38654857]

# or use vectorized format to calculate the loss and dW
loss, grad = softmax_loss_vectorized(W, X_dev, y_dev, 0.001)
print loss, grad[0]
# 2.42589425817 [-1.97135983  0.13098175 -0.49688204  1.34860066  1.53381781  2.48150556
#  1.61289219  1.90183472 -1.1548424  -5.38654857]

