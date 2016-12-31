#! /u/home/y/ybwang/python
import urllib2,re,sys,time
from BeautifulSoup import BeautifulSoup

def dl(id,assay):
	url = 'http://www.ebi.ac.uk/pride/archive/projects/'+id+'/assays/'+assay+'/psms'
	response = urllib2.urlopen(url)
	page = response.read()
	soup = BeautifulSoup(page)

	# search results
	totalnum = 0
	for t in soup.findAll('h3'):
		if t.text.find('Search results') != -1:
			totalnum = t.text.replace('Search results','')
	pagenum = (int(totalnum) + 500) / 500
	print id+"\t"+assay+"\t"+totalnum

	with open(id,'w') as fout:		
		for i in range(pagenum):
			tableurl = 'http://www.ebi.ac.uk/pride/archive/projects/'+id+'/assays/'+assay+'/psms?page='+str(i)+'&size=500&q=&sort='
			print tableurl
			data = parseTable(tableurl)			
			for d in data:
				fout.write('\t'.join(d))
				fout.write('\n')
			time.sleep(5)


def parseTable(url):
	data = []
	response = urllib2.urlopen(url)
	page = response.read()
	soup = BeautifulSoup(page)
	tbody = soup.tbody
	rows = tbody.findAll('tr')
	for row in rows:
		cols = row.findAll('td')
		cols = [ele.text.strip() for ele in cols]
		data.append([ele for ele in cols if ele])
	return data

if __name__ == '__main__':
 	# parseTable('http://www.ebi.ac.uk/pride/archive/projects/PXD004626/psms?page=0&size=100&q=&sort=')
	idlist = ['47453']
	for i in idlist:
		dl('PXD001933',i)
	# idhash = dict(idlist)
 # 	infile = idhash[sys.argv[1]]
	# with open(infile,'r') as f:
	# 	for line in f:
	# 		dl(line.rstrip())
	# 		time.sleep(20)
