#!/bin/python

import optparse
import zipfile
import os
import json
import shutil
import re

COMPANY_CODE="es.jaumesingla"

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
        #print "zip", completePathFile, file;

def package(origin, output):
    fileConfig=os.path.join(origin, "LovePackager.conf")
    if not os.path.exists(fileConfig):
        print "Origin folder should contain LovePackager.conf file"
        exit()

    jsonData=open(fileConfig).read()
    print jsonData
    config=json.loads(jsonData)
    config['files'].append('main.lua')
    if os.path.exists(os.path.join(origin, 'conf.lua')):
        config['files'].append('conf.lua')


    zipFileName=config['name']+'.love'

    zipFile=zipfile.ZipFile(os.path.join(output, zipFileName), mode='w')

    for file in config['files']:
        chargeFile(zipFile, origin, file)

    return os.path.join(output, zipFileName)

def getName(loveFile):
    return os.path.splitext(os.path.basename(loveFile))[0]

def generateWindowsExecutable(loveFile, loveData, output):
    name=getName(loveFile)
    folderName=os.path.join(output,name+"-win")
    if not os.path.exists(folderName):
        os.mkdir(folderName)
    assert(os.path.isdir(loveData))

    for file in os.listdir(loveData):
        if os.path.splitext(file)[1]=='.dll' or file=='license.txt':
            shutil.copyfile(os.path.join(loveData,file), os.path.join(folderName, file))
    writer=open(os.path.join(folderName,name+".exe"), 'wb')
    writer.write(open(os.path.join(loveData,"love.exe"), 'rb').read())
    writer.write(open(loveFile,'rb').read())


def generateMacExecutable(loveFile, loveData, output):
    name=getName(loveFile)
    folderName=os.path.join(output,name+"-mac")
    if not os.path.exists(folderName):
        os.mkdir(folderName)
    path=os.path.join(folderName, name+'.app')

    shutil.copytree(loveData, path)

    shutil.copyfile(loveFile, os.path.join(path, "Contents", "Resources", name+".love"))

    infoFile=os.path.join(path, "Contents", "Info.plist")
    infoContents=open(infoFile).read()

    m=re.search('<key>CFBundleIdentifier</key>.*\n.*<string>(.*)</string>', infoContents)
    infoContents=infoContents.replace(m.group(1), COMPANY_CODE+'.'+name)

    m=re.search('<key>CFBundleName</key>.*\n.*<string>(.*)</string>', infoContents)
    infoContents=infoContents.replace(m.group(1), name)

    m=re.search('<key>UTExportedTypeDeclarations</key>.*<array>.*</array>', infoContents, re.DOTALL)
    infoContents=infoContents.replace(m.group(0), '')    

    open(infoFile, 'w').write(infoContents)


if __name__=="__main__":
    usage="Usage: %prog [ -p origin | -l file.love [ -w baseData ] [ -m  baseData ] ] output"
    parser = optparse.OptionParser(usage, version="%prog 0.2")

    parser.add_option("-p", "--package", action="store", dest="package", default=None, 
        help="Package origin as .love file in output", metavar="origin")
    parser.add_option('-l', "--love", action="store", dest="loveFile", default=None, 
        help="Set love file to generate builds")
    parser.add_option('-w', '--windows', action="store", dest="windows", default=None,
        help="Set windows file source to made package")
    parser.add_option('-m', '--mac', action="store", dest="mac", default=None,
        help="Set mac os X file source to made package")

    (options, args)= parser.parse_args()
    if not len(args)==1:
        parser.error("the output folder is requested")
    output=args[0]

    if options.package is None and options.loveFile is None:
        parser.error("option -p or -l is required")

    if options.package is not None and options.loveFile is not None:
        parser.error("options -p and -l are mutually exclusive")

    if options.loveFile is not None:
        if options.windows is None and options.mac is None:
            parser.error("with option -l you should use -w or -m option")

    if options.package is not None:
        loveFile=package(options.package, output)
    else:
        loveFile=options.loveFile

    if options.windows is not None:
        generateWindowsExecutable(loveFile, options.windows, output)

    if options.mac is not None:
        generateMacExecutable(loveFile, options.mac, output)

