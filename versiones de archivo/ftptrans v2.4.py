
import sys
import subprocess
from Queue import Queue
import ipaddr
from functools import partial
import threading

_fromUtf8 = QString.fromUtf8
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import ping

from mainWindow import Ui_Dialog
import reporterdialog

from ftpclient import FTPClient
import ftpserver

# for translation purposes, all the text strings here, remeber to respect the
# added spaces
initialIPStr = _fromUtf8('IPv4 inicial')
endingIPStr = _fromUtf8('IPv4 final')
initialIPEgStr = _fromUtf8('148.214.82.20')
endingIPEgStr = _fromUtf8('148.214.82.60')
actionButtonStr = _fromUtf8('Correr')
closeButtonStr = _fromUtf8('Cerrar')
settingIPAddressErrorStr = _fromUtf8('No se pudo establecer esa dirección IP')
notAnIPStr = _fromUtf8('IP inv??lida')
outOfRangeIPStr = _fromUtf8('IP fuera de rango')
modeUEStr = _fromUtf8('Subir y Ejecutar archivos')
modeUStr = _fromUtf8('Solo subir archivos')
modeTStr = _fromUtf8('Solo probar conexión')
workingStr = _fromUtf8('Ejecutando...')
fileChoosingButtonStr = _fromUtf8('Escoger &archivo')
interruptButtonName = _fromUtf8('Interrumpir')
chosenFileStr = _fromUtf8('El archivo es ')
successfulConnection = _fromUtf8(' conectó exitosamente')
failedConnection = _fromUtf8(' no respondio')

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
        initialTxt = self.ui.initialIPTextBox.text()
        endingTxt = self.ui.endingIPTextBox.text()

        try:
            ipaddr.IPAddress(initialTxt)
        except:
            self.ui.initialIPTextBox.setText(notAnIPStr)
            self.ui.initialIPTextBox.selectAll()

        try:
            ipaddr.IPAddress(endingTxt)
        except:
            self.ui.endingIPTextBox.setText(notAnIPStr)
            self.ui.endingIPTextBox.selectAll()

        initial = ipaddr.IPAddress(initialTxt)
        ending = ipaddr.IPAddress(endingTxt)

        if initial > ending: #the ipaddr module allows us to do this
            self.ui.endingIPTextBox.setText(outOfRangeIPStr)
            self.ui.endingIPTextBox.selectAll()

        self.initialIP = initial
        self.endingIP = ending

    def guessHostmask(self):
        ''' we want to guess 255.255.255.0 if the user types 192.168.1.2
        and 192.168.1.3 and guess 255.255.0.0 if the user types 192.168.2.3
        192.168.3.4'''
        initial = str(self.ui.initialIPTextBox.text()).split('.')

        ending = str(self.ui.endingIPTextBox.text()).split('.')
        hostmask = ['255','255','255','255']

        for i in range(4):
            if initial[i] != ending[i]:
                hostmask[i] = '0'

        hostmask = '.'.join(hostmask)
        self.ui.subnetmaskTextBox.setText(hostmask)

    def createList(self):
        ''' returns a list with IP's in the range defined by the user
        and creates a file with that each IP on a different line'''
        listfile = open('list.txt', 'w')

        mask = self.ui.subnetmaskTextBox.text()
        ip = self.ui.initialIPTextBox.text()

        network = ipaddr.IPNetwork(ip+'/'+mask)

        machines = []
        for machine in network.iterhosts():
            if machine >= self.initialIP and machine <= self.endingIP:
                machines.append(str(machine)) #object ipaddr.IPAddress() to str
                listfile.write(str(machine)+'\n')
        self.machines = machines
        listfile.close()

    def setMode(self,mode):
        self.mode = mode

    def setUse(self,use):
        self.use = use

    def CLIwrapper(self,*args):
        self.disconnect( self, SIGNAL('update'),self.updateReporter)
        self.connect( self, SIGNAL('update'),self.updateReporter)

        _qprocess = QProcess()
        _qprocess.start(*args)
        _qprocess.waitForFinished()
        text = _qprocess.readAllStandardOutput()
        alive = True
        text = str(text)
        self.emit( SIGNAL('update'),(text,alive))

    def pingMachine(self,machine,timeout=1):
        _result = ping.do_one(machine,timeout)
        if type(_result) == float:
            alive = True
        else:
            alive = False
        self.emit( SIGNAL('update'),(machine,alive))

    def pingMachines(self,machines,timeout=1):
        self.threadPool = []
        for machine in machines:
            __thread = GenericThread(self.pingMachine,machine)
            __thread.TimeCriticalPriority
            self.threadPool.append(__thread)

        for i in range(len(self.threadPool)):
            self.threadPool[i].start()
            if len(self.threadPool) == 8:
                self.threadPool[i].wait()

    def multiThreadIt(self,*args):
        self.disconnect(self, SIGNAL('update'),self.updateReporter)
        self.connect(self, SIGNAL('update'),self.updateReporter)
        _thread = GenericThread(*args)
        _thread.start()

    def runJob(self):
        username = self.ui.usernameTextBox.text()
        password = self.ui.passwordTextBox.text()
        fileName = self.ui.fileTextBox.text()

        self.validateField()
        self.createList()
        self.dialog = reporterClass()
        self.dialog.show()
        if self.mode == 'UE':
            if self.use == 'FTP':
                pass
            elif self.use == 'SSH':
                pass
        elif self.mode == 'U':
            if self.use == 'FTP':
                pass
            elif self.use == 'SSH':
                pass
        elif self.mode == 'T':
            self.updateReporter('Probando conexion...')
            self.multiThreadIt(self.pingMachines,self.machines)

    def getFileName(self):
        self.openFilesPath = ''
        fileName = QFileDialog.getOpenFileName(self,
                "Escoge un archivo", 'C:\\',
                "Todos los archivos(*.*)")
        if fileName:
            self.ui.fileTextBox.setText(fileName)

    def uploadAndExecute(self,file,machines):
        pass

    def processFTP():
        pass

    def cleanForm(self):
        self.ui.initialIPTextBox.setText('')
        self.ui.endingIPTextBox.setText('')
        self.ui.subnetmaskTextBox.setText('')
        self.ui.usernameTextBox.setText('')
        self.ui.passwordTextBox.setText('')
        self.ui.fileTextBox.setText('')

    def updateReporter(self,values):
        value = values[1]
        string = values[0]
##        aliveTry = (value,string)

## checando el numero de veces que ha conectado esa máquina
        if string == 'P': #fix strange bug, where does P come from?
            pass
        else:
            if value == True:
                self.dialog.reporter.append(string+' '+ successfulConnection)
            else:
                self.dialog.reporter.append(string+' '+ failedConnection)

 # Create a class for our main window
class Main(QDialog,Controller):
    def __init__(self):
        QDialog.__init__(self)
        Controller.__init__(self)

        # This is always the same
        self.ui=Ui_Dialog()
        self.ui.setupUi(self)

        self.connect(self.ui.initialIPTextBox,
            SIGNAL('editingFinished()'), self.validateField)
        self.connect(self.ui.endingIPTextBox,
            SIGNAL('editingFinished()'), self.validateField)

        self.connect(self.ui.initialIPTextBox,
            SIGNAL('editingFinished()'), self.guessHostmask)
        self.connect(self.ui.endingIPTextBox,
            SIGNAL('editingFinished()'), self.guessHostmask)


        # mode selection
        self.connect(self.ui.testingOnly,
            SIGNAL('clicked()'), partial(self.setMode,'T'))
        self.connect(self.ui.uploadOnly,
            SIGNAL('clicked()'), partial(self.setMode,'U'))
        self.connect(self.ui.uploadAndExecute,
            SIGNAL('clicked()'), partial(self.setMode,'UE'))

        self.connect(self.ui.useFTP,
            SIGNAL('clicked()'), partial(self.setUse,'FTP'))
        self.connect(self.ui.useSMB,
            SIGNAL('clicked()'), partial(self.setUse,'SMB'))
        self.connect(self.ui.useSSH,
            SIGNAL('clicked()'), partial(self.setUse,'SSH'))


        self.connect(self.ui.fileChoosingButton,
            SIGNAL('clicked()'), self.getFileName)

        self.connect(self.ui.actionButton,SIGNAL('clicked()'),self.runJob)
        self.connect(self.ui.closeButton,SIGNAL('clicked()'),self.close)
        self.connect(self.ui.cleanButton,SIGNAL('clicked()'),self.cleanForm)

class reporterClass(QDialog, reporterdialog.Ui_reporterDialog):
    def __init__(self,parent=None):
        super(reporterClass, self).__init__(parent)
        self.setupUi(self)

    @pyqtSignature("")
    def on_interruptButton_clicked(self):
        print 'clickeado'



# Again, this is boilerplate, it's going to be the same on
# almost every app you write
app = QApplication(sys.argv)
window=Main()
window.show()
# It's exec_ because exec is a reserved word in Python
sys.exit(app.exec_())
