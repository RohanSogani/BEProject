#!/usr/bin/python

import sys
import os
import zipfile

BASE_DJANGO_DIR = '/home/nishad/BE_Project/bitbucket/xcalibur/Backend/mysite/'

def checkFileName(checkFile):
	if checkFile.endswith('.apk') != 1:
		#print 'Error: wrong file type, type should be .apk only'
		return 0
	try:
		zf = zipfile.ZipFile(checkFile)
	except zipfile.BadZipfile:
		#print 'Error: wrong file type, type should be .apk only'
		return 0
	else:
		try:
			info = zf.getinfo('AndroidManifest.xml')
		except KeyError:
			#print 'Error: file is .zip/.apk but does not contain AndroidManifest.xml file'
			return 0
		
	#print 'Is an apk'
	return 1


def runAW(filename):
	filename = BASE_DJANGO_DIR + 'media/apks/' + filename
	absApkPath = os.path.abspath(filename)
	print 'Absolute Path is ' + absApkPath

	if checkFileName(absApkPath) != 1:
		print 'Error: wrong file type, type should be .apk only'
		sys.exit(0)
	
	print 'Is an apk'
	print 'Beginning static analysis. . . .'

	androwarnDirPath = BASE_DJANGO_DIR + 'appWindow/androwarn/androwarn.py'
	print 'Androwarn path is ' + androwarnDirPath

	command = 'python ' + str(androwarnDirPath) + ' -i ' + str(absApkPath) + ' -v 1 -r txt'
	os.system(command)
