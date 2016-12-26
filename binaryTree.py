import sys

class Node(object):
	def __init__(self,data=-1,lchild=None,rchild=None):
		self.data = data
		self.lchild = lchild
		self.rchild = rchild

class BinaryTree(object):
	def __init__(self):
		self.root = Node()

	def add(self, data):
		node = Node(data)
		if self.isEmpty():
			self.root = node
		else:
			tree_node = self.root
			queue = []
			queue.append(self.root)
			while queue:
				tree_node = queue.pop(0)
				if tree_node.lchild == None:
					tree_node.lchild = node
					return
				elif tree_node.rchild == None:
					tree_node.rchild = node
					return
				else:
					queue.append(tree_node.lchild)
					queue.append(tree_node.rchild)

	def printTreeNR(self):	# non-recursively print tree
		queue = [self.root]
		level = [0]
		while queue:
			node = queue.pop()
			l = level.pop()
			print (l * '-') + str(node.data)
			if node.rchild:
				queue.append(node.rchild)
				level.append(l+1)
			if node.lchild:
				queue.append(node.lchild)
				level.append(l+1)

	def retriveNR(self, obj):	# non-recursively retrieve a data
		queue = [self.root]
		level = [0]
		objLevel = -1
		while queue:
			node = queue.pop()
			l = level.pop()
			if obj == node.data:
				print (l * '-') + str(node.data) + "*"
				objLevel = l
				break
			else:
				print (l * '-') + str(node.data)
			if node.rchild:
				queue.append(node.rchild)
				level.append(l+1)
			if node.lchild:
				queue.append(node.lchild)
				level.append(l+1)
		return objLevel

	def pre_order_print(self, node, num=0):	# recursively print tree
		print (num * '-') + str(node.data)
		if node.lchild:
			self.pre_order_print(node.lchild, num + 1)
		if node.rchild:
			self.pre_order_print(node.rchild, num + 1)
		return

	def pre_order_retrive(self, node, obj, tag = False, num=0):	# recursively retrieve a data
		if obj == node.data:
			print (num * '-') + str(node.data) + "*"
			return True
		else:
			print (num * '-') + str(node.data)
		if node.lchild and tag == False:
			tag = self.pre_order_retrive(node.lchild, obj, tag, num+1)
		if node.rchild and tag == False:
			tag = self.pre_order_retrive(node.rchild, obj, tag, num+1)
		return tag

	def in_order_print(self, node):	# recursively
		if node.lchild:
			self.in_order_print(node.lchild)
		print node.data
		if node.rchild:
			self.in_order_print(node.rchild)
		# if node == None:
			# return
		# self.in_order_print(node.lchild)
		# print node.data
		# self.in_order_print(node.rchild)

	def post_order_print(self,node):	# recursively
		if node.lchild:
			self.post_order_print(node.lchild)
		if node.rchild:
			self.post_order_print(node.rchild)
		print node.data

	def isEmpty(self):
		return True if self.root.data == -1 else False


if __name__ == '__main__':
	tree = BinaryTree()
	for i in range(7):
		tree.add(i)

	tree.post_order_print(tree.root)
