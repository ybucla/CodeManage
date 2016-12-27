#! /u/home/y/ybwang/python
import urllib2,re,sys,time
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
	ftp.cwd(remotepath)
	files = ftp.nlst()
	print files

if __name__ == '__main__':
	ftp = getftpconnect()
	mzfiles(ftp, '/pride/data/archive/2015/06/PXD002046')

