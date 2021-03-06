#!/usr/bin/python

import  shutil, os, re, sys
from os.path import basename

def CheckDestFolder(destPath):
    if not os.path.exists(destPath):
        os.makedirs(destPath)

def Write(text, txtfile):
    txtfile.write(text)

def getSN(path, fileName, srcPath, destPath, txtfile):
    lstSerialNumber = []  
    SNinFileName = basename(path[-16:-4]).strip("( )")

    #I think this is good, we may need to go further in the future.
    #Get SN from file name and check it's length and contents.

    if len(SNinFileName[SNinFileName.index("D"):len(SNinFileName)]) > 9:
        Write(fileName+"\tUnsuccessful - Naming error - SN too long\n", txtfile)
        return False
    elif re.search('[a-zA-Z]', SNinFileName[SNinFileName.index("D")+1:len(SNinFileName)]):
        Write(fileName+"\tUnsuccessful - Naming error - SN has letters\n", txtfile)
        return False
    else:
        lstSerialNumber.append(SNinFileName[SNinFileName.index("D")])
        for char in range(SNinFileName.index("D")+1,len(SNinFileName)):
            if (SNinFileName[char]).isdigit():
                lstSerialNumber.append(SNinFileName[char])
        SerialNumber = ''.join(lstSerialNumber)
        SerialLen = len(SerialNumber[SerialNumber.index("D"):len(SerialNumber)])
        if SerialLen == 7 or SerialLen == 8:
            return SerialNumber
        else:
            Write(fileName+"\tUnsuccessful - Problem with SN in file name\n", txtfile)
            return False

def ensure_dir(file_path):
    '''If dir doesn't exist, create one'''
    directory = os.path.abspath(file_path)
    #print(directory)
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
            Write(fileName + "\tSuccessful - File moved\n", txtfile)


def Walk_Through_Files(srcPath, destPath, txtfile):
    print("made it here")
    for root, dir, files in os.walk(srcPath):
        for file in files:
            print(file)
            if file.endswith('.pdf'):
                filePath = os.path.join(root, file)
                MoveFile(filePath, file, srcPath, destPath, txtfile)
                print("Moved " +file)

'''def Remove_Empty_Dir():
    for root, dir, files in os.walk(srcPath):
        os.rmdir(os.path.join(root,name))'''

def main():
    userhome = os.path.expanduser('~')
    desktop = userhome + r'\Desktop\\'
    srcPath = os.path.dirname(os.path.abspath(__name__))+'\\'
    destPath = desktop + r'\CheckIns\\'
    print(srcPath)

    #srcPath = sys.argv[1]
    #destPath = sys.argv[2]+"\\"
    with open('log.txt','w') as txtfile:
        CheckDestFolder(destPath)
        Walk_Through_Files(srcPath, destPath, txtfile)
        
if __name__ == "__main__":
    main()
