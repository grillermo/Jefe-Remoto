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
from os import path, getcwd, system, name, chdir
from thread import start_new_thread
import platform
from socket import gethostbyname, gethostname
from shutil import move, copy
import ftplib
import time

if name == 'nt':
    import winsound

from PyQt4.QtCore import SIGNAL, QProcess, Qt, QThread, QByteArray, QObject, QTextCodec
from PyQt4.QtGui import QDialog, QApplication, QTableWidgetItem, QFileDialog, \
                        QIcon, QAbstractItemView, QBrush, QColor, QWidget, QMessageBox, \
                        QStandardItem

from configobj import ConfigObj #allow us to treat a file as a dict, awesome!
import ping

from mainWindow import Ui_Dialog
from broadcastingReceiver import Scanner


# hack to get a nice icon on the Windows
import ctypes
myappid = 'jefeRemoto' # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
# #####################################

configFile = ConfigObj('configFile.cfg')
if not path.isfile('configFile.cfg'):
    configExists = False
    configFile.write()
else:
    configExists = True

CHECKED, NAME, OS, STATUS, IP, TRANSFER = range(6)

codec = QTextCodec.codecForName('iso-8859-1')
QTextCodec.setCodecForCStrings(codec)
GRIS = QBrush(QColor(169, 169, 169, 255))
VERDE = QBrush(QColor(70, 169, 0, 255))
ROJO = QBrush(QColor(169, 0, 0, 255))

class ViewController(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.ui=Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.passwordTextBox.setEchoMode(2) # how to do this on Qtdesigner?
        self.cwd = getcwd()

        self.machinesItems = {}

        self.tbl = self.ui.machinesTable
        if configExists:
            self.ui.usernameTextBox.setText(configFile['USERNAME'])
            self.ui.passwordTextBox.setText(configFile['PASSWORD'])

        # reimplementing drops
        self.ui.fileDropTextLine.__class__.dragMoveEvent = self.mydragMoveEvent
        self.ui.fileDropTextLine.__class__.dragEnterEvent =self.mydragEnterEvent
        self.ui.fileDropTextLine.__class__.dropEvent = self.myDropEvent


        # buttons
        self.ui.generateClientButton.clicked.connect(self.runCompilingJob)
        self.ui.uploadButton.clicked.connect(self.prepareShipment)
        self.ui.deleteMachinesButton.clicked.connect(self.deleteMachines)

        # Ui events
        self.connect(self, SIGNAL('updateStatus'),self.updateMachinesTable)
        self.ui.fileDropTextLine.editingFinished.connect(self.checkInput)
        self.connect(self,SIGNAL('droppedFile'),self.checkInput)
        self.ui.usernameTextBox.editingFinished.connect(self.saveConfig)
        self.ui.passwordTextBox.editingFinished.connect(self.saveConfig)
        self.ui.pingMachinesButton.clicked.connect(self.preparePinging)
        self.ui.chooseFileButton.clicked.connect(self.getFilePath)
        self.tbl.horizontalHeader().sectionPressed.connect(self.sort)
        self.tbl.horizontalHeader().sectionPressed.connect(self.checkUncheck)
        self.tbl.itemClicked.connect(self.checkboxesHandler)

        self.initialLoading()
        self.adaptToOS()
        start_new_thread(self.startScanner,())
        self.lista = []

    def saveConfig(self):
        configFile['USERNAME'] = self.ui.usernameTextBox.text()
        configFile['PASSWORD'] = self.ui.passwordTextBox.text()
        configFile.write()

    def startScanner(self):
        self.scanner = Scanner()
        self.connect(self.scanner,SIGNAL('addMachines'),self.addDetectedMachine)
        self.scanner.listen()

    def adaptToOS(self):
        ''' the only argument is the client name as a string
            sets the following values depending on the OS

            self.compiler : the absolute path to the compiler(PyInstaller)
            self.toCompile : the absolute path to the script to compile
            self.exeFile : the absolute path to the compiled file

            it also sets the qradiobuttons to disabled for the other os
        '''
        cwd = getcwd()
        self.customForClient = 'clientepersonalizado.py'
        self.localIP = self.getLocalIP()
        if platform.system() == 'Darwin' or platform.system() == 'Linux':
            self.ui.osxChoice.setEnabled(True)
            self.ui.windowsChoice.setEnabled(False)
            self.ui.ubuntuChoice.setEnabled(False)
            self.compiler = cwd+'/PyInstaller/pyinstaller.py'
            self.toCompile =cwd+'/'+self.customForClient
            self.exeFile = cwd+'/dist/'+self.customForClient[:-3]+'.app'
            if platform.system() == 'Linux':
                self.exeFile = cwd+'/dist/'+self.customForClient[:-3]+'.deb'
        elif platform.system() == 'Windows':
            self.compiler = cwd+'\\PyInstaller\\pyinstaller.py'
            self.toCompile = cwd+'\\'+self.customForClient
            self.exeFile = self.customForClient[:-3]+'.exe'
            self.exeFilePath = cwd+'\\dist\\'+self.exeFile

    def initialLoading(self):
        self.machinesData = ConfigObj('machines.list') ## here we will save our machines list
        if not path.isfile('machines.list'):
            self.machinesData.write()

        if len(self.machinesData) != 0: # if the user already created clients.exe
            self.ui.tabWidget.setCurrentWidget(self.ui.serverTab)
        self.tbl.verticalHeader().setVisible(False) # qtDesigner miss this
        self.tbl.horizontalHeader().setResizeMode(3) #fixed


        for name,ip in self.machinesData.items():
            rowCount = self.tbl.rowCount()
            nameItem = QTableWidgetItem(name)
            ipItem = QTableWidgetItem(self.machinesData[name])
            statusItem = QTableWidgetItem('desconocido')
            statusItem.setForeground(GRIS)
            checkboxItem = QTableWidgetItem()
            checkboxItem.setFlags(Qt.ItemIsEnabled|Qt.ItemIsUserCheckable)
            checkboxItem.setCheckState(Qt.Checked)
            self.allItemsChecked = True
            self.tbl.insertRow(rowCount)
            self.tbl.setItem(rowCount,NAME,nameItem)
            self.tbl.setItem(rowCount,IP,ipItem)
            self.tbl.setItem(rowCount,STATUS,statusItem)
            self.tbl.setItem(rowCount,CHECKED,checkboxItem)
            isChecked = 2
            self.machinesItems[ip] = [ipItem,isChecked] #save QTableWidgetItem for later use

    def addDetectedMachine(self,name,ip):
        if not self.machinesData.has_key(name):
            self.machinesData[name] = ip
            rowCount = self.tbl.rowCount()
            nameItem = QTableWidgetItem(name)
            ipItem = QTableWidgetItem(self.machinesData[name])
            statusItem = QTableWidgetItem('conectada')
            statusItem.setForeground(VERDE)
            self.tbl.insertRow(rowCount)
            self.tbl.setItem(rowCount,NAME,nameItem)
            self.tbl.setItem(rowCount,IP,ipItem)
            self.tbl.setItem(rowCount,STATUS,statusItem)

            self.machinesData.write() #and save our detected data to our machines dic

            self.machinesItems[ip] = [ipItem,isChecked] #save QTableWidgetItem for later use

    def updateMachinesTable(self,item,isAlive=True,transferStatus=''):
        '''
        item(QTableWidgetItem)  : the computer in the table to modify
        isAlive(bool)           : the computer's status on by default
        transferStatus(str)     : the transfer statos of the file
        '''
        row = item.row()
        if isAlive == True:
            statusItem = QTableWidgetItem('conectada')
            statusItem.setForeground(VERDE)
        else:
            statusItem = QTableWidgetItem('desconectada')
            statusItem.setForeground(ROJO)
        self.tbl.setItem(row,STATUS,statusItem)

        if transferStatus == '':
            transfer = QTableWidgetItem('Lista para recibir archivos')
        elif transferStatus == 'Transferencia fallida':
            transfer = QTableWidgetItem(transferStatus)
            unchecked = QTableWidgetItem()
            unchecked.setFlags(Qt.ItemIsEnabled|Qt.ItemIsUserCheckable)
            unchecked.setCheckState(Qt.Unchecked)
            self.tbl.setItem(row,CHECKED,unchecked)
        self.tbl.setItem(row,TRANSFER,transfer)


    def deleteMachines(self):
        mensaje = "¿Esta seguro que desea borrar la lista? Esta se volverá a\
poblar automaticaménte conforme se inicien maquinas con el cliente instalado"
        mensaje = mensaje.decode('utf-8')
        if QMessageBox.question(self, 'Advertencia', mensaje,
        QMessageBox.Yes | QMessageBox.No,QMessageBox.No ) == QMessageBox.Yes:
            for machine in self.machinesItems.values():
                self.deleteMachine(machine[0].row())
        else:
            return

    def deleteMachine(self, row):
        self.tbl.selectRow(row)
        name = str(self.tbl.item(row,NAME).text())
        ip = str(self.tbl.item(row,IP).text())
        del self.machinesItems[ip]
        self.tbl.removeRow(row)
        del self.machinesData[name]
        self.machinesData.write()


    def runCompilingJob(self):
        originalFile = 'clienteoriginal.py'
        customForClient = 'clientepersonalizado.py'
        user = str(self.ui.usernameTextBox.text())
        if user == '':
            QMessageBox.warning(self,'Error','Por seguridad introduzca un nombre de usuario')
        pwd = str(self.ui.passwordTextBox.text())
        if user == '':
            QMessageBox.warning(self,'Error','Por seguridad introduzca una contraseña')
        ip = self.localIP

        self.createClientFile(originalFile,customForClient,user,pwd,ip)
        self.launchCompiler(self.toCompile)
        self.saveClientFile(self.customForClient)
        self.ui.tabWidget.setCurrentWidget(self.ui.serverTab)

    def createClientFile(self,originalFile,customForClient,user,pwd,ip):
        ''' This method will generate a client script for the .py to .exe app
         and then call that app, in this case we are using PyInstaller'''
        original = open(originalFile)
        forClient = open(customForClient,"w")
        while 1:
            line = original.readline()
            loginData = '''USER, PASSWORD, SERVERIP ="","",""'''
            if not line:
                break
            if line == loginData:
                line = line.replace(loginData,
                                'USER, PASSWORD, SERVERIP = "%s", "%s", "%s"'%
                                (user,pwd,ip))
                forClient.write(line)
                break
        forClient.close()
        original.close()
        # once the file is done we save the data for future use the user typed
        configFile['USERNAME'] = user
        configFile['PASSWORD'] = pwd
        configFile.write()
        return
        # and now with our script ready we call the compiler

    def launchCompiler(self,filename,flags=' --onefile'):
        ''' Takes a string with the name of our client and calls the compiler
        with the flags hard coded here'''
        icon = path.join(self.cwd,'resources','client.ico')
        flags += ' --icon '+icon
        command = 'python "%s" "%s" %s'%(self.compiler,filename,flags)
        # remember that compiler and toCompile were create by customizeToOS()
##        print command #debugging
        system(command) # block the script until process finishes, thats what
                        # we want
        return
        # the executable is (hopefully)done we can move it where the user wants
##        print 'debug compilation \n'+str(text)

    def saveClientFile(self,customForClient):
        newPath = ''
        options = QFileDialog.ShowDirsOnly
        directory = QFileDialog.getExistingDirectory(self,
                "Donde desea guardar el ejecutable", getcwd(),options)
        newPath = path.join(str(directory),self.exeFile)
        try:
            move(self.exeFilePath,newPath)
        except:
            QMessageBox.warning(self,'Error','Ha habido un error intente crear el archivo de nuevo, intente guardarlo en otro directorio')
        return

    def prepareShipment(self):
        if self.checkInput():
            filePath = str(self.ui.fileDropTextLine.text().toLatin1())
        else:
            return
        start_new_thread(self.upload,(filePath,))

    def upload(self,filename):
        folder,filename = path.split(filename)
        chdir(folder) # ftplib only works with files in the cwd
        for ip in self.machinesData.values():
##            print 'uploading to IP ',ip
            item = self.machinesItems[ip][0]
            self.tbl.scrollToItem(item,QAbstractItemView.EnsureVisible)
            shouldUpload = self.machinesItems[ip][1]
            if shouldUpload == 2:
                try:
                    status = 'Enviando archivo...'
                    self.updateMachinesTable(item,False,status)
                    self.initFTPObject(ip)
                    self.uploadFile(filename)
                    status = 'Transferencia exitosa'
                    self.updateMachinesTable(item,transferStatus=status)
                except:
                    status = 'Transferencia fallida'
                    self.updateMachinesTable(item,False,status)
            else:
                pass


        if name == 'nt':
            sound = "C:\\c\\jefeRemoto\\master\\audio.wav"
            winsound.PlaySound('%s' % sound, winsound.SND_FILENAME)
        chdir(self.cwd)

    def uploadFile(self,filename):
        fileHandler = open(filename,'rb')
        self.ftpObject.storbinary('STOR '+filename, fileHandler)
        fileHandler.close()
##        print 'file %s succesfully sent'%filename
        return True

    def initFTPObject(self,host):
        ''' takes a host in the form of a string ip and returns and ftplib
        object '''
        self.ftpObject = ftplib.FTP(host,timeout=3)
        if configFile.has_key('USERNAME') and configFile.has_key('PASSWORD'):
            username = configFile['USERNAME']
            password = configFile['PASSWORD']
        else:
            username = str(self.ui.usernameTextBox.text())
            password = str(self.ui.passwordTextBox.text())
        self.ftpObject.login(username,password)

    def checkInput(self):
        text = str(self.ui.fileDropTextLine.text().toLatin1())
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
            self.networkProblemDialog()
##            print 'linux machine or offline machine '
        return ip

    def networkProblemDialog(self):
        if QMessageBox.question(self, 'Problema de red', "Conectese a la red y abra de nuevo este programa",
                                    QMessageBox.Ok) == QMessageBox.Ok:
                sys.exit()


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
            if len(event.mimeData().urls()) > 1: # we can only handle 1 file
                self.ui.fileDropTextLine.setText('Arraste un solo archivo')
            else:
                for url in event.mimeData().urls():
                    url = str(url.toLocalFile().toLatin1())
##                    print url
                    self.ui.fileDropTextLine.setText(url)
                    self.emit(SIGNAL('droppedFile'))
        else:
            event.ignore()

    def getFilePath(self):
        options = QFileDialog.List
        directory = QFileDialog.getOpenFileName(self,
                "¿Que archivo desea enviar?", self.cwd)
        self.ui.fileDropTextLine.setText(directory)

    def keyPressEvent(self,ev):
        if ev.key() == Qt.Key_F5:
##            print 'F5 pressed'
            self.ui.tabWidget.setCurrentWidget(self.ui.serverTab)
            start_new_thread(self.pingMachines,())

        if ev.key() == Qt.Key_F6:
##            print 'F6 pressed'
            self.ui.tabWidget.setCurrentWidget(self.ui.serverTab)
            start_new_thread(self.sort,())

        if ev.key() == Qt.Key_F7:
            self.getFile()

        if ev.key() == Qt.Key_F8:
            self.dialog()
##            print self.lista

    def sort(self,section=NAME):
##        print section
        if section == NAME or section == IP:
            self.tbl.sortItems(IP,Qt.AscendingOrder)
        else:
            self.tbl.sortItems(section,Qt.AscendingOrder)

    def checkboxesHandler(self,item):
        row = item.row()
        state = item.checkState()
        ip = str(self.tbl.item(row,IP).text())
        self.machinesItems[ip][1] = state

    def checkUncheck(self,column):
        if column == CHECKED:
            if self.allItemsChecked:
                i = 0
                for name,ip in self.machinesData.items():
                    checkboxItem = QTableWidgetItem()
                    checkboxItem.setFlags(Qt.ItemIsEnabled|Qt.ItemIsUserCheckable)
                    checkboxItem.setCheckState(0)
                    self.tbl.setItem(i,CHECKED,checkboxItem)
                    i += 1
                for ip in self.machinesItems:
                    self.machinesItems[ip][1] = 0
            else:
                i = 0
                for name,ip in self.machinesData.items():
                    checkboxItem = QTableWidgetItem()
                    checkboxItem.setFlags(Qt.ItemIsEnabled|Qt.ItemIsUserCheckable)
                    checkboxItem.setCheckState(2)
                    self.tbl.setItem(i,CHECKED,checkboxItem)
                    i += 1
                for ip in self.machinesItems:
                    self.machinesItems[ip][1] = 2
            self.allItemsChecked = not self.allItemsChecked

    def preparePinging(self):
        start_new_thread(self.pingMachines,())

    def pingMachines(self):
        for ip in self.machinesItems.keys():
            self.pingMachine(ip)

    def pingMachine(self,ip,timeout=2):
        _result = ping.do_one(ip,timeout)
##        print _result
        if type(_result) == float:
            isAlive = True
##            print 'ip %s alive'%ip
        else:
            isAlive = False
##            print 'ip %s dead'%ip
        self.emit(SIGNAL('updateStatus'),self.machinesItems[ip][0],isAlive)



def main():
    app = QApplication(sys.argv)
    window=ViewController()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()