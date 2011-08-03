#-*- coding: utf-8 -*-
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
from thread import start_new_thread, exit, interrupt_main
import platform
from socket import gethostbyname_ex, gethostname
from shutil import move, copy
import ftplib
import time



from PyQt4.QtCore import SIGNAL, QProcess, Qt, QThread, QByteArray, QObject, \
                        QTextCodec, QPoint
from PyQt4.QtGui import QDialog, QApplication, QTableWidgetItem, QFileDialog, \
                        QIcon, QAbstractItemView, QBrush, QColor, QWidget, QMessageBox, \
                        QStandardItem

from configobj import ConfigObj #allow us to treat a file as a dict, awesome!
import ping

from mainWindow import Ui_Dialog
from broadcastingReceiver import Scanner


configFile = ConfigObj('configFile.cfg')
if not path.isfile('configFile.cfg'):
    configExists = False
    configFile.write()
else:
    configExists = True

CHECKED, NAME, STATUS, IP, TRANSFER = range(5)
CLIENTFILE = 'clientepersonalizado.py'


codec = QTextCodec.codecForName('iso-8859-1')
QTextCodec.setCodecForCStrings(codec) # for PyQt in a windows spanish enviroment
GREY = QBrush(QColor(169, 169, 169, 255))
GREEN = QBrush(QColor(70, 169, 0, 255))
RED = QBrush(QColor(169, 0, 0, 255))
CWD = getcwd() # It comes often

class ViewController(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.ui=Ui_Dialog()
        self.ui.setupUi(self)
        self.tableData = {}

        self.tbl = self.ui.machinesTable # i think this adds to the readability

        # the buttons
        self.ui.generateClientButton.clicked.connect(self.runCompilingJob)
        self.ui.uploadButton.clicked.connect(self.prepareShipment)
        self.ui.deleteMachinesButton.clicked.connect(self.deleteMachines)
        self.ui.multiFunctionsButton.clicked.connect(self.chooseFunction)
        self.ui.chooseFileButton.clicked.connect(self.getFilePath)

        # Ui events
        self.connect(self, SIGNAL('updateStatus'),self.updateRow)
        self.ui.fileDropTextLine.editingFinished.connect(self.checkInput)
        self.connect(self,SIGNAL('droppedFile'),self.checkInput)
        self.ui.usernameTextBox.editingFinished.connect(self.saveConfig)
        self.ui.passwordTextBox.editingFinished.connect(self.saveConfig)
        self.tbl.horizontalHeader().sectionPressed.connect(self.sortList)
        self.tbl.horizontalHeader().sectionPressed.connect(self.toggleCheck)

        # reimplementing drops
        self.ui.fileDropTextLine.__class__.dragMoveEvent = self.mydragMoveEvent
        self.ui.fileDropTextLine.__class__.dragEnterEvent =self.mydragEnterEvent
        self.ui.fileDropTextLine.__class__.dropEvent = self.myDropEvent

        self.loadingInitialData()
        self.uiTouches()
        self.adaptToOS() # because we want to support Win and *nix
        self.listenForClients()
        self.sortList()

    def saveConfig(self):
        configFile['USERNAME'] = self.ui.usernameTextBox.text()
        configFile['PASSWORD'] = self.ui.passwordTextBox.text()
        configFile.write()
        return

    def listenForClients(self):
        self.scanner = Scanner()
        self.connect(self.scanner,SIGNAL('addMachines'),self.addMachine)
        start_new_thread(self.scanner.listen,())
        return

    def adaptToOS(self):
        ''' sets the following values depending on the OS

            self.compiler : the absolute path to the compiler(PyInstaller)
            self.toCompile : the absolute path to the script to compile
            self.exeFile : the absolute path to the compiled file

            it also sets the qradiobuttons to disabled for the other os
        '''
        cwd = getcwd()
        self.localIP = self.getLocalIP()
        self.toCompile = path.join(cwd,CLIENTFILE)
        if name.lower() == 'posix':
            self.compiler = cwd+'/PyInstaller/pyinstaller.py'
            self.exeFile = cwd+'/dist/'+CLIENTFILE[:-3]+'.app'
            if platform.system() == 'Linux':
                self.exeFile = cwd+'/dist/'+CLIENTFILE[:-3]+'.deb'
        elif platform.system() == 'Windows':
            # hack to get a nice icon on the Windows
            import ctypes
            myappid = 'jefeRemoto' # arbitrary string
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
            # #####################################
            self.compiler = cwd+'\\PyInstaller\\pyinstaller.py'
            self.exeFile = CLIENTFILE[:-3]+'.exe'
            self.exeFilePath = cwd+'\\dist\\'+self.exeFile
        return

    def uiTouches(self):
        self.ui.passwordTextBox.setEchoMode(2) # how to do this on Qtdesigner?
        if len(self.machinesData) != 0: # if the user already created clients.exe
            self.ui.tabWidget.setCurrentWidget(self.ui.serverTab)
        self.tbl.verticalHeader().setVisible(False) # qtDesigner miss this
        self.tbl.horizontalHeader().setResizeMode(3) # fixed
        self.tbl.setFocusPolicy(Qt.NoFocus) # it was messing with my checkboxes
        return

    def loadingInitialData(self):
        if configExists:
            self.ui.usernameTextBox.setText(configFile['USERNAME'])
            self.ui.passwordTextBox.setText(configFile['PASSWORD'])

        self.machinesData = ConfigObj('machines.list') ## here we will save our machines list
        if not path.isfile('machines.list'):
            self.machinesData.write()
        for name,ip in self.machinesData.items():
            self.addMachine(name,ip,status='Conectada')
        self.allItemsChecked = True


    def addMachine(self,name,ip,status='Desconocido'):
        self.machinesData[name] = ip
        rowNumber = self.tbl.rowCount()
        nameItem = QTableWidgetItem(name)
        IPItem = QTableWidgetItem(self.machinesData[name])
        statusItem = QTableWidgetItem(status)
        checkboxItem = QTableWidgetItem()
        checkboxItem.setFlags(Qt.ItemIsEnabled|Qt.ItemIsUserCheckable)
        checkboxItem.setCheckState(Qt.Checked)
        transferItem = QTableWidgetItem('')
        self.allItemsChecked = True
        self.tbl.insertRow(rowNumber)
        self.tbl.setItem(rowNumber,NAME,nameItem)
        self.tbl.setItem(rowNumber,IP,IPItem)
        self.tbl.setItem(rowNumber,STATUS,statusItem)
        self.tbl.setItem(rowNumber,CHECKED,checkboxItem)
        self.tbl.setItem(rowNumber,TRANSFER,transferItem)
        self.tableData[rowNumber] = {'checkboxItem':checkboxItem,
                            'nameItem':nameItem,
                            'IPItem':IPItem,
                            'statusItem':statusItem,
                            'transferItem':transferItem}
        row = self.tableData[rowNumber]
        isAlive = None
        if status == 'conectada':
            isALive = True
        self.updateRow(row,isAlive,transferStatus=status)
        return

    def updateRow(self,row,isAlive=None,transferStatus=''):
        '''
        item(QTableWidgetItem)  : the computer in the table to modify
        isAlive(bool)           : the computer's status on by default
        transferStatus(str)     : the transfer status of the file
        '''
        statusItem = row['statusItem']
        if isAlive == True:
            statusItem.setText('conectada')
            statusItem.setForeground(GREEN)
        elif isAlive == False:
            statusItem.setText('desconectada')
            statusItem.setForeground(RED)
        else:
            statusItem.setText('desconocido')
            statusItem.setForeground(GREY)

        transferItem = row['transferItem']
        checkboxItem = row['checkboxItem']
        if transferStatus == '':
            transferItem.setText('')
        elif transferStatus == 'Transferencia fallida':
            transferItem.setText(transferStatus)
            checkboxItem.setCheckState(2)
        elif transferStatus == 'Transferencia exitosa':
            transferItem.setText(transferStatus)
            checkboxItem.setCheckState(0)
        else:
            transferItem.setText(transferStatus)
        return


    def deleteMachines(self):
        if len(self.machinesData) == 0:
            mensaje = u'La lista ya está vacia'
            QMessageBox.information(self,'Nada que borrar',mensaje)
            return
        else:
            mensaje = u'''¿Esta seguro que desea borrar la lista? Esta se \
poblará automaticaménte conforme se inicien maquinas con el cliente instalado'''
        if QMessageBox.question(self, 'Advertencia', mensaje,
                                QMessageBox.Yes | QMessageBox.No,QMessageBox.No
                                ) == QMessageBox.Yes:
            for rowNumber,row in self.tableData.items():
                self.deleteMachine(rowNumber,row)
        else:
            return
        self.ui.tabWidget.setCurrentWidget(self.ui.serverTab)
        return

    def deleteMachine(self, rowNumber,row):
        name = str(row['nameItem'].text())
        ip = str(row['ipItem'].text())
        del self.tableData[row]
        self.tbl.removeRow(rowNumber)
        del self.machinesData[name]
        self.machinesData.write()
        return

    def runCompilingJob(self):
        originalFile = 'clienteoriginal.py'
        customForClient = 'clientepersonalizado.py'
        user = str(self.ui.usernameTextBox.text())
        if user == '':
            QMessageBox.warning(self,'Error',u'Por seguridad introduzca un \
nombre de usuario')
            return
        pwd = str(self.ui.passwordTextBox.text())
        if user == '':
            QMessageBox.warning(self,'Error',u'Por seguridad introduzca una \
contraseña')
            return
        ip = self.localIP

        self.createClientFile(originalFile,customForClient,user,pwd,ip)
        self.launchCompiler(self.toCompile)
        QMessageBox.information(self,'Exito','Se ha creado exitosamente el \
cliente escoja una carpeta donde guardarlo')
        self.saveClientFile(CLIENTFILE)
        self.ui.tabWidget.setCurrentWidget(self.ui.serverTab)
        return

    def createClientFile(self,originalFile,customForClient,user,pwd,ip):
        ''' This method will generate a client script for the .py to .exe app
         and then call that app, in this case we are using PyInstaller'''
        original = open(originalFile)
        forClient = open(customForClient,"w")
        ip = '148.214.82.56'
        while 1:
            line = original.readline()
            loginData = '''USER, PASSWORD, SERVERIP = "", "", ""'''
            if not line:
                break
            line = line.replace(loginData,
                            'USER, PASSWORD, SERVERIP = "%s", "%s", "%s"'%
                            (user,pwd,ip))
            forClient.write(line)
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
        icon = path.join(CWD,'resources','client.ico')
        flags += ' --icon '+icon
        command = 'python "%s" "%s" %s'%(self.compiler,filename,flags)
        system(command) # block the script until process finishes, thats what
                        # we want
        return
        # the executable is (hopefully)done we can move it where the user wants


    def saveClientFile(self,customForClient):
        newPath = ''
        options = QFileDialog.ShowDirsOnly
        directory = QFileDialog.getExistingDirectory(self,
                "Donde desea guardar el ejecutable", getcwd(),options)
        newPath = path.join(str(directory),self.exeFile)
        try:
            move(self.exeFilePath,newPath)
        except:
            QMessageBox.warning(self,'Error','Ha habido un error intente crear \
el archivo de nuevo e intente guardarlo en otro directorio')
        return

    def prepareShipment(self):
        if self.checkInput():
            filePath = str(self.ui.fileDropTextLine.text().toLatin1())
        else:
            return
        start_new_thread(self.upload,(filePath,))
        return

    def upload(self,filename):
        folder,filename = path.split(filename)
        chdir(folder) # ftplib only works with files in the cwd
        failFlag = False
        for row in self.tableData.values():
##            print 'uploading to IP ',ip
            item = row['IPItem']
            self.tbl.scrollToItem(item,QAbstractItemView.EnsureVisible)
            ip = str(item.text())
            shouldUpload = row['checkboxItem'].checkState()
            if shouldUpload == 2:
                status = 'Enviando archivo...'
                self.updateRow(row,None,status)
                try:
                    self.initFTPObject(ip)
                    self.uploadFile(filename)
                    status = 'Transferencia exitosa'
                    self.updateRow(row,True,status)
                except:
                    status = 'Transferencia fallida'
                    failFlag = True
                    self.updateRow(row,False,status)

        if failFlag: # nice ui touch, select the bad ones to let the user retry
            for row in self.tableData.values():
                if str(row['transferItem'].text()) == 'Transferencia fallida':
                    row['checkboxItem'].setCheckState(Qt.Checked)
                else:
                    row['checkboxItem'].setCheckState(Qt.Unchecked)

        if name == 'nt':
            import winsound # because beep beep!
            sound = "C:\\c\\jefeRemoto\\master\\audio.wav"
            winsound.PlaySound('%s' % sound, winsound.SND_FILENAME)
        chdir(CWD) # where were we? oh, right...
        return

    def uploadFile(self,filename):
        fileHandler = open(filename,'rb')
        self.ftpObject.storbinary('STOR '+filename, fileHandler)
        self.ftpObject.close()
        del self.ftpObject
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
        return

    def checkInput(self):
        self.ui.fileDropTextLine.editingFinished.disconnect(self.checkInput)
        text = str(self.ui.fileDropTextLine.text().toLatin1())
        if path.isfile(text):
            self.ui.fileDropTextLine.setStyleSheet("color: black;")
            self.ui.fileDropTextLine.editingFinished.connect(self.checkInput)
            return True
        else:
            self.ui.fileDropTextLine.setStyleSheet("color: red;")
            self.ui.fileDropTextLine.setText(u'Archivo inválido o inexistente')
            self.ui.fileDropTextLine.editingFinished.connect(self.checkInput)
            return False


    def getLocalIP(self):
        ''' yes a function is needed for this, apparently there are many
        implementations, this one it is said it works with single lan boxes'''
        try:
            ip = ([ip for ip in gethostbyname_ex(
                                gethostname())[2]
                                if not ip.startswith("127.")][0])
            if ip.startswith('127'):
                self.networkProblemDialog()
        except:
            self.networkProblemDialog()
##            print 'linux machine or offline machine '
        return ip

    def networkProblemDialog(self):
        if QMessageBox.question(self, 'Problema de red', "Conectese a la red y \
abra de nuevo este programa",
                                    QMessageBox.Ok) == QMessageBox.Ok:
            sys.exit()
        return


    def mydragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
            self.ui.fileDropTextLine.clear()
        else:
            event.ignore()
        return

    def mydragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()
        return

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
        return

    def getFilePath(self):
        options = QFileDialog.List
        directory = QFileDialog.getOpenFileName(self,u'¿Que archivo desea \
enviar?', CWD)
        self.ui.fileDropTextLine.setText(directory)
        return


    def sortList(self,section=NAME):
##        print section
        if section == NAME or section == IP:
            self.tbl.sortItems(IP,Qt.AscendingOrder)
        else:
            self.tbl.sortItems(section,Qt.AscendingOrder)
        return

    def toggleCheck(self,column):
        ''' Checks all the checkboxes if most the checkboxes are unchecked
        and unchecks them if most are checked'''
        checkeds = 0
        uncheckeds = 0
        for row in self.tableData.values():
            if row['checkboxItem'].checkState() == Qt.Unchecked:
                checkeds += 1
            if row['checkboxItem'].checkState() == Qt.Checked:
                uncheckeds += 1
        if checkeds <= uncheckeds:
            for row in self.tableData.values():
                row['checkboxItem'].setCheckState(Qt.Unchecked)
        else:
            for row in self.tableData.values():
                row['checkboxItem'].setCheckState(Qt.Checked)


    def chooseFunction(self):
        if str(self.sender().text()) == 'Checar conectividad':
            start_new_thread(self.pingMachines,())
        if str(self.sender().text()) == 'Cancelar':
            self.stopThreads()
        return

    def stopThreads(self):
        try:
            exit()
            interrupt_main()
        except:
            pass


    def pingMachines(self):
        for row in self.tableData.values():
            IPItem = row['IPItem']
            ip = str(IPItem.text())
            if row['checkboxItem'].checkState() == Qt.Checked:
                self.tbl.scrollToItem(IPItem,QAbstractItemView.EnsureVisible)
                transferStatus = u'Checando conectividad a la máquina...'
                isAlive = None
                self.emit(SIGNAL('updateStatus'),row,isAlive,transferStatus)
                self.pingMachine(ip,row)
        return

    def pingMachine(self,ip,row,timeout=2):
        pings = []
        for i in range(3):
            _result = ping.do_one(ip,timeout)
            if type(_result) == float:
                pings.append(True)
                transferStatus = 'Lista para recibir archivos'
                isAlive = True
                self.emit(SIGNAL('updateStatus'),row,isAlive,transferStatus)
                return
            else:
                pings.append(False)
        if pings.count(True) < pings.count(False):
            isAlive = False
            transferStatus = ''
        self.emit(SIGNAL('updateStatus'),row,isAlive,transferStatus)
        return

    def keyPressEvent(self,ev):
        if ev.key() == Qt.Key_F5:
##            print 'F5 pressed'
            self.ui.tabWidget.setCurrentWidget(self.ui.serverTab)
            start_new_thread(self.pingMachines,())

        if ev.key() == Qt.Key_F6:
##            print 'F6 pressed'
            self.ui.tabWidget.setCurrentWidget(self.ui.serverTab)
            start_new_thread(self.sort,())




def main():
    app = QApplication(sys.argv)
    window=ViewController()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

