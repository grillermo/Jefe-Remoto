#-------------------------------------------------------------------------------
# Application Name:         JefeRemoto
# Module Name:              ServerMain
# Purpose:                  View+Controller+Data of the main server for admins
# Author:                   Guillermo Siliceo Trueba
#
# Created:                  23/04/2011
# Licence:
'''
   Copyright 2011 Guillermo Siliceo Trueba

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
'''
#
#-------------------------------------------------------------------------------
import sys
from os import path, getcwd, system
from thread import start_new_thread
import platform
from socket import gethostbyname, gethostname
from shutil import move, copy
import ftplib
import time

from PyQt4.QtCore import SIGNAL, QProcess, Qt, QThread, QByteArray, QObject
from PyQt4.QtGui import QDialog, QApplication, QTableWidgetItem, QFileDialog, \
                        QIcon, QMovie
from configobj import ConfigObj #allow us to treat a file as a dict, awesome!

from mainWindow import Ui_Dialog
from broadcastingReceiver import Scanner
import ping

# hack to get a nice icon on the Windows
import ctypes
myappid = 'jefeRemoto' # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
# #####################################

machinesData = ConfigObj('machines.list') ## here we will save our machines list
if not path.isfile('machines.list'):
    machinesData.write()
NAME, STATUS, IP, TRANSFER = range(4)

class ViewController(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.ui=Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.passwordTextBox.setEchoMode(2) # how to do this on Qtdesigner?

        self.originalFile = 'clienteoriginal.py'
        self.customForClient = 'clientepersonalizado.py'

        self.machinesItems = {}
        self.configFile = ConfigObj('configFile.cfg')
        self.tbl = self.ui.machinesTable

        self.ui.movie_screen.setFixedHeight(0)
        self.movie = QMovie("loader.gif", QByteArray(), self)
        self.movie.setCacheMode(QMovie.CacheAll)
        self.movie.setSpeed(100)
        self.ui.movie_screen.setMovie(self.movie)


        if len(machinesData) != 0: # if the user already created clients.exe
            self.ui.tabWidget.setCurrentWidget(self.ui.serverTab)
        self.tbl.verticalHeader().setVisible(False) # qtDesigner miss this

        # reimplementing drops
        self.ui.fileDropTextLine.__class__.dragMoveEvent = self.mydragMoveEvent
        self.ui.fileDropTextLine.__class__.dragEnterEvent =self.mydragEnterEvent
        self.ui.fileDropTextLine.__class__.dropEvent = self.myDropEvent

        self.initialLoading()
        self.adaptToOS(self.customForClient)
        start_new_thread(self.startScanner,())

        # buttons
        self.ui.generateClientButton.clicked.connect(self.runCompilingJob)
        self.ui.uploadButton.clicked.connect(self.distributeSending)
        self.ui.uploadAndExecuteButton.clicked.connect(self.distributeSending)

        # Ui events
        self.connect(self, SIGNAL('updateStatus'),self.updateMachinesTable)
        self.ui.fileDropTextLine.editingFinished.connect(self.checkInput)
        self.connect(self,SIGNAL('droppedFile'),self.checkInput)
        self.tbl.cellDoubleClicked.connect(self.deleteMachine)
        self.connect(self, SIGNAL('toggleAnimation'),self.toggleWaiting)


    def toggleWaiting(self):
        print 'cambiando estado'
        if self.movie.state() == 0:
            self.ui.fileDropTextLine.setFixedHeight(0)
            self.ui.movie_screen.setFixedHeight(26)
            self.movie.start()
        else:
            self.movie.stop()
            self.ui.fileDropTextLine.setFixedHeight(26)
            self.ui.movie_screen.setFixedHeight(0)

    def startScanner(self):
        self.scanner = Scanner()
        self.connect(self.scanner,SIGNAL('addMachines'),self.addDetectedMachine)
        self.scanner.listen()

    def adaptToOS(self,customForClient):
        ''' the only argument is the client name as a string
            sets the following values depending on the OS

            self.compiler : the absolute path to the compiler(PyInstaller)
            self.toCompile : the absolute path to the script to compile
            self.exeFile : the absolute path to the compiled file

            it also sets the qradiobuttons to disabled for the other os
        '''
        cwd = getcwd()
        if platform.system() == 'Darwin' or platform.system() == 'Linux':
            self.ui.osxChoice.setEnabled(True)
            self.ui.windowsChoice.setEnabled(False)
            self.ui.ubuntuChoice.setEnabled(False)
            self.compiler = cwd+'/PyInstaller/pyinstaller.py'
            self.toCompile =cwd+'/'+customForClient
            self.exeFile = cwd+'/dist/'+customForClient[:-3]+'.app'
            if platform.system() == 'Linux':
                self.exeFile = cwd+'/dist/'+customForClient[:-3]+'.deb'
        elif platform.system() == 'Windows':
            self.ui.osxChoice.setEnabled(False)
            self.ui.windowsChoice.setEnabled(True)
            self.ui.ubuntuChoice.setEnabled(False)
            self.compiler = cwd+'\\PyInstaller\\pyinstaller.py'
            self.toCompile = cwd+'\\'+customForClient
            self.exeFile = cwd+'\\dist\\'+customForClient[:-3]+'.exe'

    def initialLoading(self):
        for name,ip in machinesData.items():
            rowCount = self.tbl.rowCount()
            nameItem = QTableWidgetItem(name)
            ipItem = QTableWidgetItem(machinesData[name])
            statusItem = QTableWidgetItem('desconocido')
            self.tbl.insertRow(rowCount)
            self.tbl.setItem(rowCount,NAME,nameItem)
            self.tbl.setItem(rowCount,IP,ipItem)
            self.tbl.setItem(rowCount,STATUS,statusItem)

            self.machinesItems[ip] = ipItem #save QTableWidgetItem for later use

    def addDetectedMachine(self,name,ip):
        start_new_thread(self.pingMachine,(ip,))
        if not machinesData.has_key(name):
            machinesData[name] = ip
            rowCount = self.tbl.rowCount()
            nameItem = QTableWidgetItem(name)
            ipItem = QTableWidgetItem(machinesData[name])
            statusItem = QTableWidgetItem('conectada')
            self.tbl.insertRow(rowCount)
            self.tbl.setItem(rowCount,NAME,nameItem)
            self.tbl.setItem(rowCount,IP,ipItem)
            self.tbl.setItem(rowCount,STATUS,statusItem)

            machinesData.write() #and save our detected data to our machines dic

            self.machinesItems[ip] = ipItem #save QTableWidgetItem for later use

    def updateMachinesTable(self,item,isAlive):
        row = item.row()
        if isAlive == True:
            statusItem = QTableWidgetItem('conectada')
        else:
            statusItem = QTableWidgetItem('desconectada')
        self.tbl.setItem(row,STATUS,statusItem)

    def deleteMachine(self, row, column):
        self.tbl.selectRow(row)
        name = str(self.tbl.item(row,0).text())
        ip = str(self.tbl.item(row,2).text())
        del self.machinesItems[ip]
        self.tbl.removeRow(row)
        del machinesData[name]
        machinesData.write()


    def runCompilingJob(self):
        self.createClientFile(self.originalFile,self.customForClient)
##        self.launchCompiler(self.toCompile)
        self.saveClientFile(self.customForClient)
        self.ui.tabWidget.setCurrentWidget(self.ui.serverTab)

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
            forClient.write(line)
        forClient.close()
        original.close()
        return
        # and now with our script ready we call the compiler

##    def launchCompiler(self,filename,flags=' --onefile'):
##        ''' Takes a string with the name of our client and calls the compiler
##        with the flags hard coded here'''
##        command = '%s "%s" %s'%(self.compiler,filename,flags)
##        # remember that compiler and toCompile were create by customizeToOS()
##        print command #debugging
##        system(command)
##        # once the file is done we save for future use the data the client used
##        self.configFile['USERNAME'] = self.username
##        self.configFile['PASSWORD'] = self.password
##        self.configFile.write()
##        return
##        # the executable is (hopefully)done we can move it where the user wants
##        print 'debug compilation \n'+str(text)

    def saveClientFile(self,customForClient):
        options = QFileDialog.ShowDirsOnly
        directory = QFileDialog.getExistingDirectory(self,
                "Donde desea guardar el ejecutable", getcwd(),options)
##        print exeFile
##        print str(directory)
        timeString = ' %s%s%s%s%s.exe'%time.localtime()[:5]
        newPath = directory+'\\'+customForClient
        move(customForClient,newPath)
        copy('ftpserver.py',newPath)
        copy('configobj.py',newPath)

        return
    def distributeSending(self):
##        self.disconnect(self, SIGNAL('clicked'),self.uploadToClients)
        if self.checkInput():
            tail, filename = path.split(str(self.ui.fileDropTextLine.text()))
        else:
            return
        senderButton = str(self.sender().objectName()) # lets see who called us
        print senderButton
        if senderButton == 'uploadButton': # only do uploading
            start_new_thread(self.uploadOnly,(filename,))
        else:
            start_new_thread(self.uploadAndExecute,(filename,))

    def uploadOnly(self,filename):
        self.emit(SIGNAL('toggleAnimation'))
        for ip in machinesData.values():
            print 'uploading to IP ',ip
            self.initFTPObject(ip)
            self.uploadFile(filename)
        self.emit(SIGNAL('toggleAnimation'))


    def uploadAndExecute(self,filename):
        self.emit(SIGNAL('toggleAnimation'))
        tail, head = path.split(filename)
        head = 'RUNME'+head
        newFilename = path.join(tail,head)
        move(filename,newFilename)
        for ip in machinesData.values():
            print 'uploading to ',ip
            self.initFTPObject(ip)
            self.uploadFile(newFilename)
        self.emit(SIGNAL('toggleAnimation'))
        move(newFilename,filename)


    def uploadFile(self,filename):
        fileHandler = open(filename,'rb')
        self.ftpObject.storbinary('STOR '+filename, fileHandler)
        fileHandler.close()
        print 'file %s succesfully sent'%filename
        return True

    def initFTPObject(self,host):
        ''' takes a host in the form of a string ip and returns and ftplib
        object '''
        self.ftpObject = ftplib.FTP(host)
        if self.configFile.has_key('USERNAME') and\
                                            self.configFile.has_key('PASSWORD'):
            username = self.configFile['USERNAME']
            password = self.configFile['PASSWORD']
        else:
            username = str(self.ui.usernameTextBox.text())
            password = str(self.ui.passwordTextBox.text())
        self.ftpObject.login(username,password)

    def checkInput(self):
        text = self.ui.fileDropTextLine.text()
        if path.isfile(text):
            self.ui.fileDropTextLine.setStyleSheet("color: black;")
            return True
        else:
            self.ui.fileDropTextLine.setStyleSheet("color: red;")
            self.ui.fileDropTextLine.setText('Archivo invalido o inexistente')
            return False

    def getLocalIP(self):
        ''' yes a function is needed for this apparently there are many
        implementations, this one it is said it works with single lan boxes'''
        ip = gethostbyname(gethostname())
        if ip.startswith('127'):
            print 'linux machine or offline machine '
        return ip

    def mydragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
            self.ui.fileDropTextLine.clear()
        else:
            event.ignore()

    def mydragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def myDropEvent(self, event):
        ''' loads into our self.files set the dropped fil5e names
            and emit a signal to advertise the change'''
        if event.mimeData().hasUrls:
            event.setDropAction(Qt.CopyAction)
            event.accept()
            if len(event.mimeData().urls()) > 1:
                self.ui.fileDropTextLine.setText('Arraste un solo archivo')
            else:
                for url in event.mimeData().urls():
                    url = str(url.toLocalFile())
                    self.ui.fileDropTextLine.setText(url)
                    self.emit(SIGNAL('droppedFile'))
        else:
            event.ignore()

    def keyPressEvent(self,ev):
        if ev.key() == Qt.Key_F5:
            print 'F5 pressed'
            self.ui.tabWidget.setCurrentWidget(self.ui.serverTab)
            start_new_thread(self.pingMachines,())

    def pingMachines(self,timeout=2):
        for ip in self.machinesItems.keys():
            self.pingMachine(ip)

    def pingMachine(self,ip,timeout=2):
        _result = ping.do_one(ip,timeout)
        if type(_result) == float:
            isAlive = True
            print 'ip %s alive'%ip
        else:
            isAlive = False
            print 'ip %s dead'%ip
        self.emit(SIGNAL('updateStatus'),self.machinesItems[ip],isAlive)



def main():
    app = QApplication(sys.argv)
    window=ViewController()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
