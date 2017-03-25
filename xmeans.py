# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 16:27:39 2017

@author: ybwang
"""

import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
import re
from collections import defaultdict
from pyclustering.cluster.xmeans import xmeans

def readSite(infile):
    data = []
    with open(infile, 'r') as f:
        for line in f:
            line = line.rstrip()
            data.append(line)
    return data

def readMatrix(matrixfile):
    codes = ['A', 'R', 'N', 'D', 'C', 'Q', 'E', 'G', 'H', 'I', 'L', 'K', 'M', 'F', 'P', 'S', 'T', 'W', 'Y', 'V', 'B', 'Z', 'X', '*']
    matrix = np.zeros((len(codes),len(codes)))
    with open(matrixfile, 'r') as f:
        for line in f:
            if line[0] not in codes: continue
            ele = re.split(r'\s+',line.rstrip())
            index = codes.index(ele[0])
            matrix[index] = [int(x) for x in ele[1::]]
    return matrix, codes

def encodePepByDist(peps, matrix, codes):
    '''
    each peptide is represented by 1*len(peps[0]), the value in each dim represented
    the similarity with all peptides using BLOSUM62 matrix
    '''
    distmatrix = np.zeros((len(peps),len(peps[0])),dtype=float)
    for i,pi in enumerate(peps):
        print i
        for l in range(len(pi)):
            scores = [matrix[codes.index(pi[l]),codes.index(pj[l])]  for j,pj in enumerate(peps)]
            distmatrix[i,l] = np.sum(scores) / float(len(peps))
    print distmatrix
    np.savetxt('distmatrix.txt',distmatrix)

def dist(p1,p2,matrix,codes):
    score = 0.0
    for i in range(len(p1)):
        aa1,aa2 = p1[i],p2[i]
        score += matrix[codes.index(aa1),codes.index(aa2)]
    return score

if __name__ == '__main__':
    data = readSite('PositivePeptide')
    matrix, codes = readMatrix('BLOSUM62R.matrix')
    encodePepByDist(data,matrix,codes)

    d = np.loadtxt('distmatrix.txt')
    dlist = d.tolist()
    xmeans_instance = xmeans(dlist, [ dlist[1] ], ccore = True)
    xmeans_instance.process()
    clusters = xmeans_instance.get_clusters()
    centers = xmeans_instance.get_centers()
    ssewithin = 0.0
    for i, cluster in enumerate(clusters):
        s = np.sum((d[cluster,:] - centers[i]) * (d[cluster,:] - centers[i]))
        ssewithin += s
    meantotal = np.mean(d,0)
    ssetotal = np.sum((d - meantotal) * (d - meantotal))
    print ssewithin, ssetotal, ssewithin / ssetotal