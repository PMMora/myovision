#!/usr/bin/python

import  shutil, os, re, sys
from os.path import basename

def CheckDestFolder(destPath):
    if not os.path.exists(destPath):
        os.makedirs(destPath)

def Write(text, txtfile):
    txtfile.write(text)

def getSN(path, fileName, srcPath, destPath, txtfile):
    check_d11 = re.compile('D11\d{6}[^a-zA-Z\d]')
    check_others = re.compile('D\d{7}[^a-zA-z\d]')
    if check_d11.search(fileName) != None:
    	return serialNumber.search(fileName).group(0)
    elif check_others.search(fileName) != None:
    	return check_others.search(fileName).group(0)
    else:
    	Write(fileName+'\tUnsuccessful - Unable to find Serial Number\n', txtfile)
    	print('Did not move ' + fileName)
    	return False

def ensure_dir(file_path):
    '''If dir doesn't exist, create one'''
    directory = os.path.abspath(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(directory +" created")

def MoveFile(path, fileName, srcPath, destPath, txtfile):
    SerialNumber = getSN(path, fileName, srcPath, destPath, txtfile)
    if SerialNumber:
        ensure_dir(destPath+SerialNumber)
        print(destPath+SerialNumber+"\\"+fileName)
        if os.path.isfile(destPath+SerialNumber+"\\"+fileName):            
            Write(fileName+"\tUnsuccessful - File already exists\n", txtfile)
        else:
            shutil.move(path,destPath+SerialNumber)
            print('Moved '+fileName)
            Write(fileName + "\tSuccessful - File moved\n", txtfile)


def Walk_Through_Files(srcPath, destPath, txtfile):
    for root, dir, files in os.walk(srcPath):
        for file in files:
            if file.endswith('.pdf'):
                filePath = os.path.join(root, file)
                MoveFile(filePath, file, srcPath, destPath, txtfile)

'''def Remove_Empty_Dir(srcPath):
    for root, dir, files in os.walk(srcPath):
        os.rmdir(os.path.join(root,name))'''

def main():
    userhome = os.path.expanduser('~')
    desktop = userhome + r'\Desktop\\'
    srcPath = os.path.dirname(os.path.abspath(__name__))+'\\'
    destPath = desktop + r'\CheckIns\\'
    '''use these srcPath and destPath when calling script from C#
    srcPath = sys.argv[1]
    destPath = sys.argv[2]+"\\"
    '''

    with open('log.txt','w') as txtfile:
        CheckDestFolder(destPath)
        Walk_Through_Files(srcPath, destPath, txtfile)
if __name__ == "__main__":
    sys.exit(main())