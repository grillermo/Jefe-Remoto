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
import platform
from socket import gethostbyname, gethostname
from shutil import move, copy
import time

if name == 'nt':
    import winsound

from PyQt4.QtCore import SIGNAL, QProcess, Qt, QThread, QByteArray, QObject
from PyQt4.QtGui import QDialog, QApplication, QTableWidgetItem, QFileDialog, \
                        QIcon, QMovie, QAbstractItemView, QBrush, QColor

import ping

from mainWindow import Ui_Dialog


from server import localdata
from server import uploading
from server import clientmaking
from server import communication

NAME, STATUS, IP, TRANSFER = range(4)
VIRGINCLIENT = 'client.py'
DISTRIBUTABLEFILE = 'customclient.py'

class MainWindow(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.ui=Ui_Dialog()
        self.ui.setupUi(self)

        self.configFile, self.machinesData,configExists = localdata.loadData()
        self.UIfixes()
        self.fillTable()
        self.adaptToOS(self.customForClient)

        communication.listen(self)  # we pass self to emmit a signal each time a
                                    # machine is found

        self.machinesItems = {} # for Bookeeping our table items
        self.table = self.ui.machinesTable #because too long name

        # buttons
        self.ui.generateClientButton.clicked.connect(self.runCompilingJob)
        self.ui.uploadButton.clicked.connect(self.prepareShipment)

        # Ui events
        self.connect(self,SIGNAL('droppedFile'),self.checkInput)
        self.connect(self,SIGNAL('updateStatus'),self.updateMachinesTable)
        self.connect(self,SIGNAL('toggleAnimation'),self.toggleWaiting)
        self.connect(self,SIGNAL('addMachines'),self.addDetectedMachine)
        self.ui.fileDropTextLine.editingFinished.connect(self.checkInput)
        self.table.cellDoubleClicked.connect(self.deleteMachine)
        self.ui.usernameTextBox.editingFinished.connect(self.saveConfig)
        self.ui.passwordTextBox.editingFinished.connect(self.saveConfig)


        machinesAlive(self.machinesItems)

    def getMachineItem(self,ip):
        return self.machinesItems[ip]

    def toggleWaiting(self):
        if self.movie.state() == 0:
            self.ui.fileDropTextLine.setFixedHeight(0)
            self.ui.movie_screen.setFixedHeight(26)
            self.movie.start()
        else:
            self.movie.stop()
            self.ui.fileDropTextLine.setFixedHeight(26)
            self.ui.movie_screen.setFixedHeight(0)

    def UIfixes(self):
        ''' Stuff you can't do on QtDesigner '''
        # reimplementing drops
        self.ui.fileDropTextLine.__class__.dragMoveEvent = self.mydragMoveEvent
        self.ui.fileDropTextLine.__class__.dragEnterEvent =self.mydragEnterEvent
        self.ui.fileDropTextLine.__class__.dropEvent = self.myDropEvent

        # Waiting animation
        self.ui.movie_screen.setFixedHeight(0)
        self.movie = QMovie("loader.gif", QByteArray(), self)
        self.movie.setCacheMode(QMovie.CacheAll)
        self.movie.setSpeed(100)
        self.ui.movie_screen.setMovie(self.movie)

        if len(self.machinesData) != 0: # if the user already created clients.exe
            self.ui.tabWidget.setCurrentWidget(self.ui.serverTab)
        self.table.verticalHeader().setVisible(False) # QtDesigner miss this
        self.ui.passwordTextBox.setEchoMode(2) # how to do this on Qtdesigner?
        # darn it QtDesign get your stuff together
        if configExists:
            self.ui.usernameTextBox.setText(configFile['USERNAME'])
            self.ui.passwordTextBox.setText(configFile['PASSWORD'])

    def fillTable(self):
        for name,ip in self.machinesData.items():
            rowCount = self.table.rowCount()
            nameItem = QTableWidgetItem(name)
            ipItem = QTableWidgetItem(self.machinesData[name])
            statusItem = QTableWidgetItem('desconocido')
            self.table.insertRow(rowCount)
            self.table.setItem(rowCount,NAME,nameItem)
            self.table.setItem(rowCount,IP,ipItem)
            self.table.setItem(rowCount,STATUS,statusItem)

            self.machinesItems[ip] = ipItem #save QTableWidgetItem for later use
        self.sortTable()

    def addDetectedMachine(self,name,ip):
        if not self.machinesData.has_key(name):
            self.machinesData[name] = ip
            rowCount = self.table.rowCount()
            nameItem = QTableWidgetItem(name)
            ipItem = QTableWidgetItem(self.machinesData[name])
            statusItem = QTableWidgetItem('conectada')
            self.table.insertRow(rowCount)
            self.table.setItem(rowCount,NAME,nameItem)
            self.table.setItem(rowCount,IP,ipItem)
            self.table.setItem(rowCount,STATUS,statusItem)

            self.machinesData.write() #and save our detected data to our machines dic

            self.machinesItems[ip] = ipItem #save QTableWidgetItem for later use

    def updateMachinesTable(self,item,isAlive=True,transferStatus=None):
        '''
        item(QTableWidgetItem)  : the computer in the table to modify
        isAlive(bool)           : the computer's status on by default
        transferStatus(str)     : the transfer status of the file
        '''
        row = item.row()
        if isAlive == True:
            statusItem = QTableWidgetItem('conectada')
        else:
            statusItem = QTableWidgetItem('desconectada')
            return
        self.table.setItem(row,STATUS,statusItem)

        if transferStatus:
            transfer = QTableWidgetItem(transferStatus)
        else:
            transfer = QTableWidgetItem('Lista para recibir archivos')
        self.table.setItem(row,TRANSFER,transfer)

    def deleteMachine(self, row, column):
        self.table.selectRow(row)
        name = str(self.table.item(row,0).text())
        ip = str(self.table.item(row,2).text())
        del self.machinesItems[ip]
        self.table.removeRow(row)
        del self.machinesData[name]
        self.machinesData.write()


    def prepareShipment(self):
        if self.checkInput():
            filename = str(self.ui.fileDropTextLine.text())
        else:
            return
        start_new_thread(self.upload,(filename,))

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
            communication.pingThem(self,self.machinesItems)

        if ev.key() == Qt.Key_F6:
            print 'F6 pressed'
            self.ui.tabWidget.setCurrentWidget(self.ui.serverTab)
            start_new_thread(self.sort,())


    def sortTable(self):
        self.table.sortItems(IP,Qt.AscendingOrder)



def main():
    app = QApplication(sys.argv)
    window=ViewController()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()