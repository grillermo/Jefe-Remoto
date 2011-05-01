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




# for translation purposes, all the text strings here

initialIPStr = _fromUtf8('IPv4 inicial')
endingIPStr = _fromUtf8('IPv4 final')
initialIPEgStr = _fromUtf8('192.168.1.1')
endingIPEgStr = _fromUtf8('192.168.1.254')
actionButtonStr = _fromUtf8('Correr')
closeButtonStr = _fromUtf8('Cerrar')
settingIPAddressErrorStr = _fromUtf8('No se pudo establecer esa dirección IP')
validatingIPErrorStr = _fromUtf8('IP inválida')
modeUEStr = _fromUtf8('Subir y Ejecutar archivos')
modeUStr = _fromUtf8('Solo subir archivos')
modeTStr = _fromUtf8('Solo probar conexión')
workingStr = _fromUtf8('Ejecutando...')
pingCmdFailedStr =_fromUtf8('Host de destino inaccesible')
fileChoosingButtonStr = _fromUtf8('Escoger &archivo')
interruptButtonName = _fromUtf8('Interrumpir')
chosenFileStr = _fromUtf8('El archivo es ')

machines = ['192.168.1.102','192.168.1.103']
file = ''

class Controller():
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
        self.initialIP = '1.1.1.1'
        self.endingIP = '1.1.1.1'
        self.inBetweenIPsLst = []
        self.mode = 'T'
        self.reporterTxt = ''
        self.connectionMode = ''
        self.num_threads = 2
        self.report = []

    def validateIP(self):
        ''' 'string'
        checks that we are using a valid IPv4 using the ipaddr module
        changes'''
        who = self.sender()
        ip = who.text()
        try:
            ipaddr.IPAddress(ip)
        except:
            who.setText(validatingIPErrorStr)
            who.selectAll()

    def setAddress(self):
        ''' 'string'
        Changes object.address to that of userIP if it's a valid IPv4
            otherwise returns a message error and quits
        sets the current instance.address'''

    def setMode(self,mode):
        ''' changes the connection mode to upload and execute '''
        self.reporter.setText(mode)
        self.mode = mode

    def pinger(self):
        machine = '192.168.1.102'
        currentPing = subprocess.Popen('ping '+machine,
                                stdout=subprocess.PIPE,
                                shell=True)
        returnStr = currentPing.communicate()
##        returnStr = currentPing.stdout.read()
        self.report.append(returnStr)
##        if pingCmdFailedStr not in str(returnStr):
##            self.report.append((machine+' is alive'))

    def multithreading(self,function):
        worker = threading.Thread(target=function)
        worker.start()
        self.reporter.setText(workingStr)
        worker.join()
        self.reporter.setText(str(self.report))


    def runJob(self):
        if self.mode == 'UE':
            self.multithreading(self.uploadAndExecute,machines,file)
        elif self.mode == 'U':
            self.multithreading(self.uploadOnly,machines,file)
        elif self.mode == 'T':
            self.multithreading(self.pinger)

    def createList(self):
        self.initialIP

    def openFileName(self):
        fileName = QFileDialog.getOpenFileName()
        if fileName:
            self.reporter.setText(chosenFileStr+fileName)

    def uploadAndExecute(self,file,machines):
        pass


class View(QDialog,Controller):
    '''' Implements the GUI'''
    def __init__(self, parent=None):
        super(View,self).__init__(parent)
        Controller.__init__(self)

        # initializing the GUI widgets
        self.initialIPLbl = QLabel(initialIPStr)

        self.initialIPTexBox = QLineEdit()
        self.initialIPTexBox.setText(initialIPEgStr)
        self.initialIPTexBox.selectAll()
        self.initialIPTexBox.setMaximumWidth(93)

        self.endingIPLbl = QLabel(endingIPStr)

        self.endingIPTexBox = QLineEdit()
        self.endingIPTexBox.setText(endingIPEgStr)
        self.endingIPTexBox.selectAll()
        self.endingIPTexBox.setMaximumWidth(93)

        self.testingOnly = QRadioButton()
        self.testingOnly.setText(modeTStr)

        self.uploadAndExecute = QRadioButton()
        self.uploadAndExecute.setText(modeUEStr)
        self.uploadAndExecute.setChecked(True)

        self.uploadOnly = QRadioButton()
        self.uploadOnly.setText(modeUStr)


        self.fileChoosingButton = QPushButton(fileChoosingButtonStr)

        self.interruptButton = QPushButton(interruptButtonName)
        self.interruptButton.setDisabled(True)

        self.actionButton = QPushButton(actionButtonStr)

        self.reporter = QTextBrowser()

        self.closeButton = QPushButton()
        self.closeButton.setMaximumWidth(100)
        self.closeButton.setText(closeButtonStr)

        #actually using the widgets
        layout = QGridLayout()
        self.buttonGroup = QButtonGroup(parent=layout)

        layout.addWidget(self.initialIPLbl,1,0)
        layout.addWidget(self.initialIPTexBox,2,0)
        layout.addWidget(self.endingIPLbl,3,0)
        layout.addWidget(self.endingIPTexBox,4,0)
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
        self.connect(self.initialIPTexBox,
                SIGNAL('editingFinished()'), self.validateIP)
        self.connect(self.endingIPTexBox,
                SIGNAL('editingFinished()'), self.validateIP)

        # mode selection
        self.connect(self.uploadAndExecute,
                SIGNAL('clicked()'), partial(self.setMode,'UE'))
        self.connect(self.uploadOnly,
                SIGNAL('clicked()'), partial(self.setMode,'U'))
        self.connect(self.testingOnly,
                SIGNAL('clicked()'), partial(self.setMode,'T'))

        self.connect(self.fileChoosingButton,
                SIGNAL('clicked()'), self.openFileName)

        # we run the function multithreading using the partial function because
        # it allows to add parameters to our function call, the only parameter
        # here being the function pinger
        self.connect(self.actionButton,SIGNAL('clicked()'),self.runJob)


app = QApplication(sys.argv)
view = View()
view.show()
app.exec_()


