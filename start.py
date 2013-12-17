#!/bin/python

import optparse
import zipfile
import os
import json

def chargeFile(zipFile, path, file):
	"""
	@type zip zipfile.ZipFile
	"""
	completePathFile=os.path.join(path,file)
	if os.path.isdir(completePathFile):
		for subfile in os.listdir(completePathFile):
			chargeFile(zipFile, path, os.path.join(file, subfile))
	else:
		zipFile.write(completePathFile, file)
		print "zip", completePathFile, file;


if __name__=="__main__":
	usage="Usage: %prog folder output"
	parser = optparse.OptionParser(usage)

	(options, args)= parser.parse_args()

	assert(len(args)==2)

	#(origin, output)=os.path.split(args[0])
	origin=args[0]
	output=args[1]

	fileConfig=os.path.join(origin, "LovePackager.conf")
	if not os.path.exists(fileConfig):
		print "Origin folder should contain LovePackager.conf file"
		exit()

	jsonData=open(fileConfig).read()
	print jsonData
	config=json.loads(jsonData)

	zipFileName=config['name']+'.love'

	zipFile=zipfile.ZipFile(os.path.join(output, zipFileName), mode='w')

	for file in config['files']:
		chargeFile(zipFile, origin, file)

	#chargeFile(None, path, file)
