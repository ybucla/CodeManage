#!/usr/bin/python

# -*- coding: utf-8 -*-
"""
Created on Wed Mar 01 10:26:40 2017

@author: ybwang
"""

from collections import defaultdict
import re

_end = '_end_'

def readDatabase(database):
   head = {}
   data = defaultdict(str)
   n = 0
   with open(database,'r') as f:
       for line in f:
           line = line.rstrip()
           if line.find('>') != -1:
               n += 1
               head[n] = line[1::]
           else:
               data[n] += line
   return data,head

def readPep(cruxfile):
    pephash = {}
    with open(cruxfile,'r') as f:
        for line in f:
            ele = line.rstrip().split("\t")
            if ele[0] != 'PSMId' and float(ele[2]) < 0.05:
                pep = re.sub(re.compile("\.|\*|-"),'',ele[4])
                pephash[str.upper(pep)] = ele[3]
    return pephash

def getsubpep(data,first=['A']):
    peps = dict()
    for n in data:
        seq = data[n]
        firstindex = [i for i, ltr in enumerate(seq) if ltr in first]
        for i in firstindex:
            peps[seq[i:]] = ''
    return peps

def make_trie(words):
    root = dict()
    n = 0
    for word in words:
        n += 1
        print n
        current_dict = root
        for letter in word:
            current_dict = current_dict.setdefault(letter, {})
        current_dict[_end] = word
    return root

def in_trie(trie, word):
    current_dict = trie
    mapping = []
    for letter in word:
        print letter,current_dict.keys()
        if _end in current_dict:
            mapping.append(current_dict[_end])
        if letter in current_dict:
            current_dict = current_dict[letter]
        else:
            return mapping
    else:
        print 'key:',current_dict.keys()
        if _end in current_dict:
            mapping.append(current_dict[_end])
            return mapping
        else:
            return mapping

pepsdict = readPep('percolator.target.peptides.txt')
#data,index = readDatabase('merge_20170222014116-7431.fa')
t = make_trie(pepsdict.keys())
print pepsdict['KAKIQDKEGIPPDQQRL']
#peps = getsubpep(data)
#print len(peps)
#n = 0
#for p in peps:
#    n += 1
#    print n, in_trie(t,str.upper(p))
#print t['K']['K']['Q']['S']['K']['P']['V']['T']['T']['P']['E']['E']['I']['A']['Q']['V']['A']['T']['I']['S']['A']['N']['G']['D'].keys()
print in_trie(t,'KAKIQDKEGIPPDQQRLSDFS')
#t = make_trie(s)
#t

