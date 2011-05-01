#-------------------------------------------------------------------------------
# Name:        module2
# Purpose:
#
# Author:      grillermo
#
# Created:     23/04/2011
# Copyright:   (c) grillermo 2011
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python
import sys
from os import path, getcwd,system
from thread import start_new_thread
import platform
from socket import gethostbyname, gethostname
from shutil import move
from subprocess import Popen, PIPE
from functools import partial

from PyQt4.QtCore import SIGNAL, QProcess, Qt
from PyQt4.QtGui import QDialog, QApplication,QTableWidgetItem, QFileDialog,\
                        QMessageBox
from configobj import ConfigObj #allow us to treat a file as a dict, awesome!

from mainWindow import Ui_Dialog
from broadcastingReceiver import *

# ######## Load machines list ####### #
machinesFile = ConfigObj('machines.cfg')
if path.isfile('machines.cfg'):
    machinesData = {}
    for name,ip in machinesFile.items():
            machinesData[name] = ip

else:
    machinesData = {}
    machinesFile.write()

# ######################################## #

STATE, NAME, IP, TRANSFER = range(4)

class ViewController(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.ui=Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.passwordTextBox.setEchoMode(2)
        self.exeBatch = 'run.py' #read the docstring of createExecutionFile()
        self.originalFile = 'clienteOriginal.py'
        self.customForClient = 'ClientePersonalizado.py'
        self.files = set([])
        configFile = ConfigObj('configFile.cfg')

        # reimplementing drops
        self.ui.machinesTable.__class__.dragMoveEvent = self.mydragMoveEvent
        self.ui.machinesTable.__class__.dragEnterEvent = self.mydragMoveEvent
        self.ui.machinesTable.__class__.dropEvent = self.myDropEvent

        self.adaptToOS(self.customForClient)
        start_new_thread(self.startScanner,())

        self.ui.generateClientButton.clicked.connect(self.runCompilingJob)
        self.ui.uploadButton.clicked.connect(self.uploadToClients)
        self.ui.uploadAndExecuteButton.clicked.connect(self.uploadToClients)
        # don't know how to connect unbound signals with the new style
        self.connect(self,SIGNAL('dropped'),self.pruebas)

        self.ui.pruebas.clicked.connect(self.pruebas)

    def pruebas(self):
        self.warningDialog('lol osom','tu mama')
##        print str(self.files)
##        print str(self.sender().objectName())

    def startScanner(self):
        self.scanner = Scanner()
        self.connect(self.scanner, SIGNAL('updateMachines'), self.updateView)
        self.scanner.listen()

    def updateView(self,name,ip):
        if not machinesData.has_key(name):
            machinesData[name] = ip
            for name in machinesData.keys():
                _index = self.ui.machinesTable.rowCount()
                _name = QTableWidgetItem(name)
                _ip = QTableWidgetItem(machinesData[name])
                self.ui.machinesTable.insertRow(_index)
                self.ui.machinesTable.setItem(_index,NAME,_name)
                self.ui.machinesTable.setItem(_index,IP,_ip)
                machinesFile[name] = machinesData[ip]
                machinesFile.write()
        return

    def adaptToOS(self,customForClient):
        ''' the only argument is the client name as a string
            sets the following values depending on the OS

            self.exeCreator : the absolute path to the compiler(PyInstaller)
            self.toCompile : the absolute path to the script to compile
            self.exeFile : the absolute path to the compiled file

            it also sets the qradiobuttons to disabled for the other os
            '''
        cwd = getcwd()
        if platform.system() == 'Darwin' or platform.system() == 'Linux':
            self.ui.osxChoice.setEnabled(True)
            self.ui.windowsChoice.setEnabled(False)
            self.ui.linuxChoice.setEnabled(False)
            self.exeCreator = cwd+'/PyInstaller/pyinstaller.py'
            self.toCompile =cwd+'/'+customForClient
            self.exeFile = cwd+'/dist/'+customForClient[:-3]+'.app'
            if platform.system() == 'Linux':
                self.exeFile = cwd+'/dist/'+customForClient[:-3]+'.deb'
        elif platform.system() == 'Windows':
            self.ui.osxChoice.setEnabled(False)
            self.ui.windowsChoice.setEnabled(True)
            self.ui.ubuntuChoice.setEnabled(False)
            self.exeCreator = cwd+'\\PyInstaller\\pyinstaller.py'
            self.toCompile = cwd+'\\'+customForClient
            self.exeFile = cwd+'\\dist\\'+customForClient[:-3]+'.exe'

    def runCompilingJob(self):
        self.createClientFile(self.originalFile,self.customForClient)
        self.launchExeCreator(self.exeFile)
        self.moveExe(self.exeFile)

    def createClientFile(self,originalFile,customForClient):
        ''' This method will generate a client script for the .py to .exe app
         and then call that app, in this case we are using PyInstaller'''
        self.username = str(self.ui.usernameTextBox.text())
        self.password = str(self.ui.passwordTextBox.text())
        ip = self.getLocalIP()

        original = open(originalFile)
        forClient = open(customForClient,"w")
        while 1:
            line = original.readline()
            if not line: break
            line = line.replace('''USER, PASSWORD, SERVERIP ="","",""''',
                                'USER, PASSWORD, SERVERIP = "%s", "%s", "%s"'%
                                (self.username,self.password,ip))
            line = line.replace("executorFile = 'run.py'",
                                "executorFile = '%s'"%self.exeBatch)
            forClient.write(line)
        forClient.close()
        original.close()
        return
        # and now with our script ready we call the compiler

    def launchExeCreator(self,filename,flags=' --onefile --noconsole'):
        ''' Takes a string with the name of our client and calls the compiler
        with the flags hard coded here'''
        command = '%s "%s" %s'%(self.exeCreator,filename,flags)
        # remember that exeCreator and toCompile were create by customizeToOS()
        print command #debugging
        process = system(command)

        # once the file is done we save for future use the data the client used
        configFile['USERNAME'] = self.username
        configFile['PASSWORD'] = self.password
        configFile.write()
        return
        # the executable is (hopefully)done we can move it where the user wants
##        print 'debug compilation \n'+str(text)

    def saveExe(self,exeDir,exeName):
        options = QFileDialog.ShowDirsOnly
        directory = QFileDialog.getExistingDirectory(self,
                "Donde desea guardar el ejecutable", options)
        print exeDir+exeName
        print str(directory)
        move(exeDir+exeName,str(directory))
        return

    def uploadToClients(self):
        ''' will send the files to the clients '''
        senderButton = str(self.sender().objectName()) #lets see who called us
        if senderButton == uploadButton: #only do uploading
            for name in machinesData.keys():
                clientFTP = self.initFTPObject(machinesData[name])
                self.uploadFiles(clientFTP,self.files)
        else:
            batchFilePath = batchExeFile()
            self.files.add(batchFilePath)
            for name in machinesData.keys():
                clientFTP = self.initFTPObject(machinesData[name])
                self.uploadFiles(clientFTP,self.files)
            self.files.remove(batchFilePath)

    def initFTPObject(self,host):
        ''' takes a host in the form of a string ip and returns and ftplib
        object '''
        ftpObject = FTP(host)
        if configFile.has_key('USERNAME') and configFile.has_key('PASSWORD'):
            username = configFile['USERNAME']
            password = configFile['PASSWORD']
        else:
            username = str(self.ui.usernameTextBox.text())
            password = str(self.ui.passwordTextBox.text())

        ftpObject.login(username,password)
        return ftpObject

    def uploadFiles(self,ftpObject,files):
        ''' takes and ftp object and a set of files and recursively uploads
        the files'''
        if not len(files):
            for fileName in files:
                if self.uploadFile(ftpObject,filename):
                    self.files.remove(fileName)
                else:
                    print 'file sending failed at self.uploadFiles()'
                    raise
                self.uploadFiles() #recursive function ftw
        return True
##        ftp.retrlines('LIST')

    def uploadFile(self,ftpObject,fileName):
        fileHandler = open(filename,'rb')
        self.ftp.storbinary('STOR  '+filename, fileHandler)
        print 'file sending filed at self.sendFile()'
        fileHandler.close()
        return True

    def batchExeFile(self,):
        ''' hacky idea alert: this app will send a file called run.py to the
        remote pc that will detect it and execute if the file changes.
        run.py will then execute the files one by one os.system().
        If only i implemented SSH... on my ToDo list'''
        runFile = open(self.exeBatch,'wb')
        for filename in self.files:
            runFile.write(filename)
        runFile.close()
        return path.join(getcwd()+self.exeBatch)

    def warningDialog(self, message, title):
        msgBox = QMessageBox()
        msgBox.setText(message)
        msgBox.setWindowTitle(title)
        if msgBox.exec_():
            pass

    def getLocalIP(self):
        ''' yes a function is needed for this apparently there are many
        implementations, this one it is said it works with single lan boxes'''
        ip = gethostbyname(gethostname())
        if ip.startswith('127'):
            print 'linux machine or offline machine '
        return ip

    def mydragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def myDropEvent(self, event):
        ''' loads into our self.files set the dropped file names
            and emit a signal to advertise the change'''
        if event.mimeData().hasUrls:
            event.setDropAction(Qt.CopyAction)
            event.accept()
            for url in event.mimeData().urls():
                url = str(url.toLocalFile())
                if path.isfile(url):
                    self.files.add(url)
            self.emit(SIGNAL("dropped"))
        else:
            event.ignore()

def main():
    app = QApplication(sys.argv)
    window=ViewController()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()