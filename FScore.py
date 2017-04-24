# -*- coding: utf-8 -*-
"""

Created on 2017/4/21

@author: ybwang
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import roc_auc_score
from sklearn.linear_model import LogisticRegression


class FScore(object):
    def __init__(self):
        self.x = []
        self.y = []

    def cal(self, feature, label, pos_label=1):
        feature = feature.flatten()
        pindex = np.where(label == pos_label)[0]
        nindex = np.where(label != pos_label)[0]
        mu_all = np.mean(feature)
        mu_pos = np.mean(feature[pindex])
        mu_neg = np.mean(feature[nindex])
        n_pos, n_neg = pindex.size, nindex.size
        numerator = np.sum((mu_pos - mu_all) ** 2) + np.sum((mu_neg - mu_all) ** 2)
        denominator = 1.0 / (n_pos - 1) * np.sum((feature[pindex] - mu_pos) ** 2) + 1.0 / (n_neg - 1) * np.sum(
            (feature[nindex] - mu_neg) ** 2)
        f = 0.0 if numerator == 0 else (numerator + 1e-5) / (denominator + 1e-5)
        return f

    def fselect(self, predictor, x, y, nfold=5, measure='auc'):
        '''
        The predictor should implement fit and predict function of Classifier
        :param predictor: (Classifier) predictor
        :param x: (numpy) x
        :param y: (numpy) y
        :param measure: (str) 'auc'
        :return: (list) feature index
        '''
        ini_fscore = []
        for i in range(x.shape[1]):
            ini_fscore.append(self.cal(x[:, i], y))
        best_threshold, feature, best_auc = ini_fscore[0], [], 0
        for threshold in sorted(ini_fscore)[::-1]:
            if threshold == 0.0: continue
            feature_index = np.where(np.array(ini_fscore) >= threshold)[0]
            performance = []
            for iter in range(20):
                p_fold, n_fold = nfoldsplit(x, y, nfold)
                for i in range(1, nfold + 1):
                    p_test_index, p_train_index = np.where(p_fold[:, 1] == i)[0], np.where(p_fold[:, 1] != i)[0]
                    n_test_index, n_train_index = np.where(n_fold[:, 1] == i)[0], np.where(n_fold[:, 1] != i)[0]
                    p_train, n_train = p_fold[p_train_index, 0], n_fold[n_train_index, 0]
                    p_test, n_test = p_fold[p_test_index, 0], n_fold[n_test_index, 0]
                    train, test = np.concatenate((p_train, n_train)), np.concatenate((p_test, n_test))
                    # print '#', threshold, i, train.shape, test.shape
                    x_train, y_train = x[np.ix_(train, feature_index)], y[train]
                    x_test, y_test = x[np.ix_(test, feature_index)], y[test]
                    predictor.fit(x_train, y_train)
                    scores = predictor.predict(x_test)
                    performance.append(roc_auc_score(y_test, scores))
            average = sum(performance) / len(performance)
            if average > best_auc:
                best_auc = average
                feature = feature_index[:]
            print threshold, average, len(feature_index)
        return feature, best_auc


class classicifier(object):
    def __init__(self):
        pass

    def fit(self, x, y):
        return None

    def predict(self, x):
        return None


def nfoldsplit(x, y, nfold=5, pos_label=1):
    pindex = np.where(y == pos_label)[0]
    np.random.shuffle(pindex)
    nindex = np.where(y != pos_label)[0]
    np.random.shuffle(nindex)
    each = (len(pindex) - len(pindex) % nfold) / nfold
    p_fold_num = np.repeat(1, each + len(pindex) % nfold)
    for i in range(2, nfold + 1):
        p_fold_num = np.concatenate((p_fold_num, np.repeat(i, each)))
    each = (len(nindex) - len(nindex) % nfold) / nfold
    n_fold_num = np.repeat(1, each + len(nindex) % nfold)
    for i in range(2, nfold + 1):
        n_fold_num = np.concatenate((n_fold_num, np.repeat(i, each)))
    return np.hstack((pindex.reshape((-1, 1)), p_fold_num.reshape((-1, 1)))), np.hstack(
        (nindex.reshape((-1, 1)), n_fold_num.reshape((-1, 1))))


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


if __name__ == '__main__':
    f = FScore()
    d = readTSV('Other_PLK_PLK1/dataMM.txt')
    x, y = d[:, :-1], d[:, -1]

    lr = LogisticRegression(C=1e5)
    feature, auc = f.fselect(lr, x, y)
    print feature
    print auc

    # fold_p, fold_n = nfoldsplit(x, y)
    # print fold_p
    # print fold_n
    # index, fscore = [], []
    # for i in range(x.shape[1]):
    #     # print i, f.cal(x[:, i], y)
    #     index.append(i)
    #     fscore.append(f.cal(x[:, i], y))
    # print fscore
    # plt.bar(index, fscore)
    # plt.show()
