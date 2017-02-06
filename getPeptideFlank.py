def getPeptideFlank(seq,position,left,right):
	newseq = ('*' * left) + seq + ("*" * right)
	start = left+position - left
	end = right + left + 1 - 1 + start
	return newseq[start-1:end]

if __name__ == '__main__':
  print getPeptideFlank('MSQVQVQVQNPSAALSGSQILNKNQSLLSQPLMSIPSTTSSLPSENAGRPIQNSALPSAS',58,7,7)
