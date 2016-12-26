import random,math

def km(d,k,e=1e-5):
	center = [random.randint(0,len(d)-1) for i in range(k)]
	label = [0] * len(d)
	for iter in range(2):
		center_new = [0] * k
		count = [0] * k
		for i in range(len(d)):
			dis = [abs(d[i] - x) for x in center]			
			min_index = dis.index(min(dis))
			label[i] = min_index
			count[min_index] += 1
			center_new[min_index] += dis[min_index]	
		count = [x + 1 for x in count]
		center_new = [center_new[x] / float(count[x]) for x in range(k)]
		a = sum([abs(x) for x in center])
		b = sum([abs(x) for x in center_new])
		if abs(a-b) < e: break
		center = center_new[:]
	return label
	
d = [0,1,1,22,3,2,4,20,21,27,25]

print km(d,3)