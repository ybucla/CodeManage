# Multiclass Support Vector Machine
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 24 13:19:52 2017

@author: ybwang
"""
import numpy as np
import svm_loss_naive

# load test data
X_dev = np.loadtxt('X_dev.txt') # X_dev.shape = (500L, 3073L)
y_dev = np.loadtxt('y_dev.txt',dtype='int32') # X_dev.shape = (500L,)
