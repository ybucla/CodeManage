import numpy as np
import math

def viterbi(obs,A,B,pi):
	state_len = len(pi)
	obs_len = len(obs)
	wmatrix = np.zeros((state_len,obs_len))
	wmatrix[:,0] = pi * B[:,obs[0]]
	pmatrix = np.zeros((state_len,obs_len))
	for i in range(1,obs_len):
		w_list = []
		tag_list = []
		for s in range(state_len):
			l = wmatrix[:,i-1] * A[:,s] * B[s,obs[i]]
			w_list.append(l.max())
			tag_list.append(int(np.where(l == l.max())[0]))
		wmatrix[:,i] = np.array(w_list)
		pmatrix[:,i] = np.array(tag_list)
	# backwards to path
	path = [-1] * obs_len
	path[-1] = int(np.where(wmatrix[:,-1] == wmatrix[:,-1].max())[0])
	for i in range(obs_len-1,0,-1):
		path[i-1] = int(pmatrix[path[i],i])
	print wmatrix
	print pmatrix
	print path

obs = [0,1,1,0,0,0,0,0,0,1]
A = np.array([[0.5,0.2,0.3],[0.3,0.5,0.2],[0.2,0.3,0.5]])
B = np.array([[0.5,0.5],[0.4,0.6],[0.7,0.3]])
pi = np.array([0.2,0.4,0.4])

viterbi(obs,A,B,pi)
