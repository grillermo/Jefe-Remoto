# ftptest.py - An example application using Python's ftplib module.
# Author: Matt Croydon <matt@ooiio.com>, referencing many sources, including:
#   Pydoc for ftplib: http://web.pydoc.org/2.2/ftplib.html
#   ftplib module docs: http://www.python.org/doc/current/lib/module-ftplib.html
#   Python Tutorial: http://www.python.org/doc/current/tut/tut.html
# License: GNU GPL.  The software is free, don't sue me.
# This was written under Python 2.2, though it should work with Python 2.x
# and greater.

# Import the FTP object from ftplib
from ftplib import FTP
from os import path,getcwd

# This will handle the data being downloaded
# It will be explained shortly
class FTPClient():
    def __init__(self, host,username,password):
        self.ftp = FTP(host,4,4,3)
        self.username = username
        self.password = password

    def login(self):
        print 'Logging in.'
        self.ftp.login(self.username,self.password)
        self.ftp.retrlines('LIST')

    def handleDownload(self,block):
        self.file.write(block)
        return '.'

    def getFile(self,remoteFilename):
        # Open the file for writing in binary mode
        print 'Opening local file ' + remoteFilename

        self.file = open(remoteFilename, 'wb')


        # retrbinary as the docs say, defaults to a chunk size and pass it to
        # the callback
        print 'Getting ' + remoteFilename
        self.ftp.storbinary('STOR '+remoteFilename,open(remoteFilename, "rb"))
        self.file.close()
        return True

    def closeConnection(self):
        # Clean up time

        print 'Closing FTP connection'
        print self.ftp.close()

    def printDir(self):
        print self.ftp.retrlines('LIST')

def main():
    # test function
    servidor = FTPClient('localhost','labsia','labsia')
    servidor.login()
    servidor.printDir()
    servidor.getFile('paramiko-1.7.4.zip')
    servidor.closeConnection()

if __name__ == '__main__':
    pass



