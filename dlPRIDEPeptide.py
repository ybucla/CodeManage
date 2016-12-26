#! /u/home/y/ybwang/python
import urllib2,re,sys,time
from BeautifulSoup import BeautifulSoup

def dl(id):
	url = 'http://www.ebi.ac.uk/pride/archive/projects/'+id+'/psms'
	response = urllib2.urlopen(url)
	page = response.read()
	soup = BeautifulSoup(page)

	# search results
	totalnum = 0
	for t in soup.findAll('h3'):
		if t.text.find('Search results') != -1:
			totalnum = t.text.replace('Search results','')
	pagenum = (int(totalnum) + 100) / 100
	
	with open(id,'w') as fout:		
		for i in range(pagenum):
			tableurl = 'http://www.ebi.ac.uk/pride/archive/projects/'+id+'/psms?page='+str(i)+'&size=100&q=&sort='
			print tableurl
			data = parseTable(tableurl)			
			for d in data:
				fout.write('\t'.join(d))
				fout.write('\n')
			time.sleep(0.6)


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
	idlist = [('1','x_00'),('2','x_01'),('3','x_02'),('4','x_03'),('5','x_04'),('6','x_05'),('7','x_06'),('8','x_07'),('9','x_08'),('10','x_09'),('11','x_10'),('12','x_11'),('13','x_12'),('14','x_13'),('15','x_14'),('16','x_15'),('17','x_16'),('18','x_17'),('19','x_18'),('20','x_19'),('21','x_20'),('22','x_21'),('23','x_22'),('24','x_23'),('25','x_24'),('26','x_25'),('27','x_26'),('28','x_27'),('29','x_28'),('30','x_29'),('31','x_30'),('32','x_31'),('33','x_32'),('34','x_33'),('35','x_34'),('36','x_35'),('37','x_36')]
	idhash = dict(idlist)
 	infile = idhash[sys.argv[1]]
	with open(infile,'r') as f:
		for line in f:
			dl(line.rstrip())
			time.sleep(20)
