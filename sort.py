# 1,3,5,7,2,8
def mpsort(x):
	while(1):
		tag = 0
		for i in range(len(x)-1):
			if x[i] > x[i + 1]:
				x[i],x[i+1] = x[i+1],x[i]
				tag = tag + 1
		if tag == 0:
			break	
	print x
	
def quicksort(x):
	# print x
	if len(x) <= 1:
		return x
	pivot = x[-1]	
	left = [i for i in x[0:-1] if i < pivot]
	right = [i for i in x[0:-1] if i >= pivot]
	return quicksort(left) + [pivot] + quicksort(right)
	
		
print quicksort([1,7,8,5,9,4,3,5])
