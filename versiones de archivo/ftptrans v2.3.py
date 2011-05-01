#-------------------------------------------------------------------------------
# Name:        Ftp Admin Sender
# Purpose:     this script allows you to send file script to several different
#              clients that run an ftp server.
#              I wrote this to help me distribute software and updates remotely
# Author:      Guillermo Siliceo Trueba
#
# Created:     05/03/2011
# Copyright:   (c) Guillermo Siliceo Trueba 2011
# Licence:     GPL v2.0
# version:     2.0
# Notes:       In this version i used OO programming and the following extra
#              libraries:
#              EasyGui      v0.96             http://easygui.sourceforge.net/
#              ipaddr-py    v2.1.5-py3k       http://code.google.com/p/ipaddr-py
#-------------------------------------------------------------------------------

import sys
from ftplib import FTP
from PyQt4.QtCore import *
from PyQt4.QtGui import *
##import PyQt4.QtCore
import time
import subprocess
from Queue import Queue
import ipaddr
from functools import partial
import threading
_fromUtf8 = QString.fromUtf8
import ping, socket

# for translation purposes, all the text strings here, remeber to respect the
# added spaces

initialIPStr = _fromUtf8('IPv4 inicial')
endingIPStr = _fromUtf8('IPv4 final')
initialIPEgStr = _fromUtf8('148.214.82.20')
endingIPEgStr = _fromUtf8('148.214.82.60')
actionButtonStr = _fromUtf8('Correr')
closeButtonStr = _fromUtf8('Cerrar')
settingIPAddressErrorStr = _fromUtf8('No se pudo establecer esa dirección IP')
notAnIPStr = _fromUtf8('IP inválida')
outOfRangeIPStr = _fromUtf8('IP fuera de rango')
modeUEStr = _fromUtf8('Subir y Ejecutar archivos')
modeUStr = _fromUtf8('Solo subir archivos')
modeTStr = _fromUtf8('Solo probar conexión')
workingStr = _fromUtf8('Ejecutando...')
pingCmdFailedStr =_fromUtf8('Host de destino inaccesible')
fileChoosingButtonStr = _fromUtf8('Escoger &archivo')
interruptButtonName = _fromUtf8('Interrumpir')
chosenFileStr = _fromUtf8('El archivo es ')
successfulConnection = _fromUtf8(' conectó exitosamente')
failedConnection = _fromUtf8(' no respondió')

class GenericThread(QThread):
    def __init__(self, function='', *args, **kwargs):
        QThread.__init__(self)
        self.function = function
        self.args = args
        self.kwargs = kwargs

    def __del__(self):
        self.wait()

    def run(self):
        self.function(*self.args,**self.kwargs)
        return

class Controller(GenericThread):
    '''
        implements the functionality of our application connecting the dada
        from the model to the view
            attributes:
                    address - the 4 octects that form an IP in a string
            methods:
                    isValidIP.('string')
                    set_address

    '''
    def __init__(self):
        GenericThread.__init__(self)
        self.mode = 'T'

    def validateField(self):
        ''' checks that we are using a valid IPv4 using the ipaddr module
        and also checks that the IP class C range is valid'''
        initialTxt = self.initialIPTextBox.text()
        endingTxt = self.endingIPTextBox.text()

        try:
            ipaddr.IPAddress(initialTxt)
        except:
            self.initialIPTextBox.setText(notAnIPStr)
            self.initialIPTextBox.selectAll()

        try:
            ipaddr.IPAddress(endingTxt)
        except:
            self.endingIPTextBox.setText(notAnIPStr)
            self.endingIPTextBox.selectAll()

        initial = ipaddr.IPAddress(initialTxt)
        ending = ipaddr.IPAddress(endingTxt)

        if initial > ending: #the ipaddr module allows us to do this
            self.endingIPTextBox.setText(outOfRangeIPStr)
            self.endingIPTextBox.selectAll()

        self.initialIP = initial
        self.endingIP = ending

    def guessHostmask(self):
        ''' we want to guess 255.255.255.0 if the user types 192.168.1.2
        and 192.168.1.3 and guess 255.255.0.0 if the user types 192.168.2.3
        192.168.3.4'''
        initial = str(self.initialIPTextBox.text()).split('.')

        ending = str(self.endingIPTextBox.text()).split('.')
        hostmask = ['255','255','255','255']

        for i in range(4):
            if initial[i] != ending[i]:
                hostmask[i] = '0'

        hostmask = '.'.join(hostmask)
        return hostmask

    def createList(self):
        ''' returns a list with IP's in the range defined by the user '''
        mask = self.guessHostmask()
        ip = self.initialIPTextBox.text()

        network = ipaddr.IPNetwork(ip+'/'+mask)

        machines = []
        for machine in network.iterhosts():
            if machine >= self.initialIP and machine <= self.endingIP:
                machines.append(str(machine)) #object ipaddr.IPAddress() to str
        self.machines = machines

    def updateReporter(self,string):
        self.reporter.append(string)

    def setMode(self,mode):
        ''' changes the connection mode to upload and execute '''
        self.mode = mode

    def threadOutput(self):
        text = self.qprocess.readAllStandardOutput()
        self.reporter.append(str(text))

    def wrapper(self,program,*args):
        ''' program(string), *arguments(strings), ...
        Executes a program in the os cli(not the python interpreter)
         after it finished calls threadOutput to print its output.
         Remember to add the spaces as necessary before or after the program
         and arguments to form a valid string for the os to execute'''

        _qprocess = QProcess()
        _qprocess.connect(self.qprocess, SIGNAL( 'readyReadStandardOutput()' ),
                      self.threadOutput )
        _qprocess.connect(self.qprocess, SIGNAL( 'readyReadStandardError()' ),
                      self.threadOutput  )
        _qprocess.start(program,args)
        _qprocess.waitForFinished()

    def pingMachines(self,machine,timeout=2):
        _result = ping.do_one(machine,timeout)
        if type(_result) == float:
            _result = ' conecto'
        else:
            _result = ' fallo'
        self.emit( SIGNAL('update'), 'la ip '+machine+' '+_result)

    def multithreading(self,function, machines,*args):
        self.threadPool = []
        self.disconnect( self, SIGNAL('update'),self.updateReporter)
        self.connect( self, SIGNAL('update'),self.updateReporter)
        for machine in machines:
            self.threadPool.append(GenericThread(function,machine))
        for i in range(len(self.threadPool)):
            self.threadPool[i].start()

    def runJob(self):
        self.createList()
        self.validateField()

        if self.mode == 'UE':
            self.multithreading(self.uploadAndExecute,*args)
        elif self.mode == 'U':
            self.multithreading(self.uploadOnly,*args)
            self.multithreading(self.wrapper,(psexec,'-u UsuarioRemoto -p 2010'))
        elif self.mode == 'T':
            self.reporter.setText('Probando conexion...')
            self.multithreading(self.pingMachines,(self.machines))

    def openFileName(self):
        fileName = QFileDialog.getOpenFileName()
        if fileName:
            self.reporter.setText(chosenFileStr+fileName)

    def uploadAndExecute(self,file,machines):
        pass

class View(QDialog,Controller):
    '''' Implements the GUI'''
    def __init__(self, parent=None):
        QDialog.__init__(self)
        Controller.__init__(self)

        # initializing the GUI widgets
        self.initialIPLbl = QLabel(initialIPStr)

        self.initialIPTextBox = QLineEdit()
        self.initialIPTextBox.setText(initialIPEgStr)
        self.initialIPTextBox.selectAll()
        self.initialIPTextBox.setMaximumWidth(93)

        self.endingIPLbl = QLabel(endingIPStr)

        self.endingIPTextBox = QLineEdit()
        self.endingIPTextBox.setText(endingIPEgStr)
        self.endingIPTextBox.selectAll()
        self.endingIPTextBox.setMaximumWidth(93)

        self.testingOnly = QRadioButton()
        self.testingOnly.setText(modeTStr)

        self.uploadAndExecute = QRadioButton()
        self.uploadAndExecute.setText(modeUEStr)
        self.uploadAndExecute.setChecked(True)

        self.uploadOnly = QRadioButton()
        self.uploadOnly.setText(modeUStr)


        self.fileChoosingButton = QPushButton(fileChoosingButtonStr)

        self.interruptButton = QPushButton(interruptButtonName)
        self.interruptButton.setMaximumWidth(100)
        self.interruptButton.setDisabled(True)

        self.actionButton = QPushButton(actionButtonStr)
        self.actionButton.setMaximumWidth(100)

        self.reporter = QTextBrowser()

        self.closeButton = QPushButton()
        self.closeButton.setMaximumWidth(100)
        self.closeButton.setText(closeButtonStr)

        #actually using the widgets
        layout = QGridLayout()
        self.buttonGroup = QButtonGroup(parent=layout)

        layout.addWidget(self.initialIPLbl,1,0)
        layout.addWidget(self.initialIPTextBox,2,0)
        layout.addWidget(self.endingIPLbl,3,0)
        layout.addWidget(self.endingIPTextBox,4,0)
        layout.addWidget(self.uploadAndExecute,7,0)
        layout.addWidget(self.testingOnly,8,0)
        layout.addWidget(self.uploadOnly,9,0)
        layout.addWidget(self.fileChoosingButton, 11, 0)
        layout.addWidget(self.actionButton,12,0)
        layout.addWidget(self.interruptButton,13,0)
        layout.addWidget(self.reporter,14,0)
        layout.addWidget(self.closeButton,15,0)

        self.setLayout(layout)

        # controller calls

        # text box validator
        self.connect(self.initialIPTextBox,
                SIGNAL('editingFinished()'), self.validateField)
        self.connect(self.endingIPTextBox,
                SIGNAL('editingFinished()'), self.validateField)

        # mode selection
        self.connect(self.uploadAndExecute,
                SIGNAL('clicked()'), partial(self.setMode,'UE'))
        self.connect(self.uploadOnly,
                SIGNAL('clicked()'), partial(self.setMode,'U'))
        self.connect(self.testingOnly,
                SIGNAL('clicked()'), partial(self.setMode,'T'))

        self.connect(self.fileChoosingButton,
                SIGNAL('clicked()'), self.openFileName)

        self.connect(self.actionButton,SIGNAL('clicked()'),self.runJob)


app = QApplication(sys.argv)
view = View()
view.show()
app.exec_()


