#! /u/home/y/ybwang/python
from BeautifulSoup import BeautifulSoup
from ftplib import FTP 

def getftpconnect():
	ftp_server = 'ftp.pride.ebi.ac.uk'
	username = ''
	password = ''
	ftp=FTP()
	ftp.set_debuglevel(2)
	ftp.connect(ftp_server,21)
	ftp.login(username,password)
	return ftp    

def mzfiles(ftp, remotepath):
	result = []
	ftp.cwd(remotepath)
	files = ftp.nlst()
	for f in files:
		newpath = remotepath + '/'+f
		ftp.cwd(newpath)
		for fname in ftp.nlst():
			result.append(i+"\t"+newpath+'/'+fname)
	for r in result:
		print r
if __name__ == '__main__':
	ftp = getftpconnect()
	mzfiles(ftp, '/pride/data/archive/2016')

