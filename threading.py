import time,threading

index = 0
mutex = threading.Lock()
def main():
	thread_list = []
	for i in xrange(5):
		sthread = threading.Thread(target = run, args = str(i))
		sthread.setDaemon(True)
		sthread.start()
		thread_list.append(sthread)
	for i in xrange(5):
		thread_list[i].join()
	print "Main thread"

def run(threadIndex):
	global index
	num = 0
	while 1:
		if mutex.acquire(1):
			if index == 3:
				print "Thread-%s acquired, current num: %d, finish!" % (threadIndex,index)
				mutex.release()
				break
			print "Thread-%s: acquired %s" % (threadIndex,index)
			num = index
			index += 1
			mutex.release()
		# start do something with 'num'
		time.sleep(1)
		# end
		

if __name__ == '__main__':
	main()
