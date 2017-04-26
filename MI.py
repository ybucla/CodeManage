import numpy as np
import math

def getMI_discrete(x_feature, y):
    MI = 0.0
    for l in np.unique(y):
        for x in np.unique(x_feature):
            p_xy = len(np.intersect1d(np.where(x_feature == x)[0], np.where(y == l)[0])) / float(len(y))
            p_y = len(np.where(y == l)[0]) / float(len(y))
            p_x = len(np.where(x_feature == x)[0]) / float(len(y))
            p_xy += 1e-20 if p_xy == 0.0 else 0.0
            MI += p_xy * math.log(p_xy / p_x / p_y)
            print x, l, p_xy, p_y, p_x, p_xy / p_x / p_y
    return MI
   
if __name__ == '__main__':
    x = np.array([1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
    y = np.array([2, 2, 3, 2, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2])
    x = x.reshape((-1, 1))
    print getMI_discrete(x[:, 0], y)
