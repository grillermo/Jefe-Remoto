# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\c\jefeRemoto\master\mainWindow.ui'
#
# Created: Sat Jun 11 15:13:02 2011
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(648, 469)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/resources/server-icon.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.gridLayout_2 = QtGui.QGridLayout(Dialog)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.tabWidget = QtGui.QTabWidget(Dialog)
        self.tabWidget.setEnabled(True)
        self.tabWidget.setFocusPolicy(QtCore.Qt.NoFocus)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.clientTab = QtGui.QWidget()
        self.clientTab.setObjectName(_fromUtf8("clientTab"))
        self.gridLayout_5 = QtGui.QGridLayout(self.clientTab)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.groupBox = QtGui.QGroupBox(self.clientTab)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.groupBox)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.userLbl = QtGui.QLabel(self.groupBox)
        self.userLbl.setObjectName(_fromUtf8("userLbl"))
        self.horizontalLayout_3.addWidget(self.userLbl)
        self.usernameTextBox = QtGui.QLineEdit(self.groupBox)
        self.usernameTextBox.setText(_fromUtf8(""))
        self.usernameTextBox.setObjectName(_fromUtf8("usernameTextBox"))
        self.horizontalLayout_3.addWidget(self.usernameTextBox)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.passwordLbl = QtGui.QLabel(self.groupBox)
        self.passwordLbl.setObjectName(_fromUtf8("passwordLbl"))
        self.horizontalLayout_3.addWidget(self.passwordLbl)
        self.passwordTextBox = QtGui.QLineEdit(self.groupBox)
        self.passwordTextBox.setObjectName(_fromUtf8("passwordTextBox"))
        self.horizontalLayout_3.addWidget(self.passwordTextBox)
        self.gridLayout_5.addWidget(self.groupBox, 0, 0, 1, 1)
        self.groupBox_2 = QtGui.QGroupBox(self.clientTab)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.gridLayout_3 = QtGui.QGridLayout(self.groupBox_2)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.ubuntuChoice = QtGui.QRadioButton(self.groupBox_2)
        self.ubuntuChoice.setEnabled(False)
        self.ubuntuChoice.setFocusPolicy(QtCore.Qt.NoFocus)
        self.ubuntuChoice.setObjectName(_fromUtf8("ubuntuChoice"))
        self.horizontalLayout.addWidget(self.ubuntuChoice)
        self.osxChoice = QtGui.QRadioButton(self.groupBox_2)
        self.osxChoice.setEnabled(False)
        self.osxChoice.setFocusPolicy(QtCore.Qt.NoFocus)
        self.osxChoice.setObjectName(_fromUtf8("osxChoice"))
        self.horizontalLayout.addWidget(self.osxChoice)
        self.windowsChoice = QtGui.QRadioButton(self.groupBox_2)
        self.windowsChoice.setEnabled(True)
        self.windowsChoice.setFocusPolicy(QtCore.Qt.NoFocus)
        self.windowsChoice.setIconSize(QtCore.QSize(16, 16))
        self.windowsChoice.setChecked(True)
        self.windowsChoice.setObjectName(_fromUtf8("windowsChoice"))
        self.horizontalLayout.addWidget(self.windowsChoice)
        self.gridLayout_3.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.gridLayout_5.addWidget(self.groupBox_2, 1, 0, 1, 1)
        self.groupBox_3 = QtGui.QGroupBox(self.clientTab)
        self.groupBox_3.setEnabled(True)
        self.groupBox_3.setFlat(False)
        self.groupBox_3.setCheckable(False)
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.gridLayout_4 = QtGui.QGridLayout(self.groupBox_3)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.textEdit = QtGui.QTextEdit(self.groupBox_3)
        self.textEdit.setFocusPolicy(QtCore.Qt.NoFocus)
        self.textEdit.setAcceptDrops(False)
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.gridLayout_4.addWidget(self.textEdit, 0, 0, 1, 1)
        self.generateClientButton = QtGui.QCommandLinkButton(self.groupBox_3)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/resources/present_64.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.generateClientButton.setIcon(icon1)
        self.generateClientButton.setObjectName(_fromUtf8("generateClientButton"))
        self.gridLayout_4.addWidget(self.generateClientButton, 1, 0, 1, 1)
        self.gridLayout_5.addWidget(self.groupBox_3, 2, 0, 1, 2)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/resources/user_64.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.clientTab, icon2, _fromUtf8(""))
        self.serverTab = QtGui.QWidget()
        self.serverTab.setObjectName(_fromUtf8("serverTab"))
        self.gridLayout = QtGui.QGridLayout(self.serverTab)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayoutActionBtns = QtGui.QHBoxLayout()
        self.horizontalLayoutActionBtns.setObjectName(_fromUtf8("horizontalLayoutActionBtns"))
        self.uploadButton = QtGui.QCommandLinkButton(self.serverTab)
        self.uploadButton.setAcceptDrops(False)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/resources/plus_64.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.uploadButton.setIcon(icon3)
        self.uploadButton.setCheckable(False)
        self.uploadButton.setAutoRepeat(False)
        self.uploadButton.setObjectName(_fromUtf8("uploadButton"))
        self.horizontalLayoutActionBtns.addWidget(self.uploadButton)
        self.uploadAndExecuteButton = QtGui.QCommandLinkButton(self.serverTab)
        self.uploadAndExecuteButton.setAcceptDrops(False)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/resources/right_64.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.uploadAndExecuteButton.setIcon(icon4)
        self.uploadAndExecuteButton.setObjectName(_fromUtf8("uploadAndExecuteButton"))
        self.horizontalLayoutActionBtns.addWidget(self.uploadAndExecuteButton)
        self.gridLayout.addLayout(self.horizontalLayoutActionBtns, 4, 0, 1, 1)
        self.fileDropTextLine = QtGui.QLineEdit(self.serverTab)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Segoe UI"))
        font.setPointSize(11)
        font.setWeight(50)
        font.setItalic(True)
        font.setUnderline(False)
        font.setStrikeOut(False)
        font.setBold(False)
        self.fileDropTextLine.setFont(font)
        self.fileDropTextLine.setStyleSheet(_fromUtf8(""))
        self.fileDropTextLine.setDragEnabled(True)
        self.fileDropTextLine.setObjectName(_fromUtf8("fileDropTextLine"))
        self.gridLayout.addWidget(self.fileDropTextLine, 2, 0, 1, 1)
        self.machinesTable = QtGui.QTableWidget(self.serverTab)
        self.machinesTable.setEnabled(True)
        self.machinesTable.setMouseTracking(True)
        self.machinesTable.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.machinesTable.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.machinesTable.setAcceptDrops(False)
        self.machinesTable.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.machinesTable.setAlternatingRowColors(True)
        self.machinesTable.setObjectName(_fromUtf8("machinesTable"))
        self.machinesTable.setColumnCount(4)
        self.machinesTable.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.machinesTable.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.machinesTable.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.machinesTable.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.machinesTable.setHorizontalHeaderItem(3, item)
        self.machinesTable.horizontalHeader().setStretchLastSection(True)
        self.machinesTable.verticalHeader().setStretchLastSection(False)
        self.gridLayout.addWidget(self.machinesTable, 0, 0, 1, 1)
        self.movie_screen = QtGui.QLabel(self.serverTab)
        self.movie_screen.setStyleSheet(_fromUtf8("border-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(255, 178, 102, 255), stop:0.55 rgba(235, 148, 61, 255), stop:0.98 rgba(0, 0, 0, 255), stop:1 rgba(0, 0, 0, 0));"))
        self.movie_screen.setText(_fromUtf8(""))
        self.movie_screen.setAlignment(QtCore.Qt.AlignCenter)
        self.movie_screen.setMargin(0)
        self.movie_screen.setObjectName(_fromUtf8("movie_screen"))
        self.gridLayout.addWidget(self.movie_screen, 1, 0, 1, 1)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/resources/network-receive.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.serverTab, icon5, _fromUtf8(""))
        self.gridLayout_2.addWidget(self.tabWidget, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Jefe Remoto", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("Dialog", "Datos de seguridad", None, QtGui.QApplication.UnicodeUTF8))
        self.userLbl.setText(QtGui.QApplication.translate("Dialog", "Usuario", None, QtGui.QApplication.UnicodeUTF8))
        self.passwordLbl.setText(QtGui.QApplication.translate("Dialog", "Contraseña", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("Dialog", "Generar para:", None, QtGui.QApplication.UnicodeUTF8))
        self.ubuntuChoice.setToolTip(QtGui.QApplication.translate("Dialog", "Solo disponible al correr esta aplicación Ubuntu", None, QtGui.QApplication.UnicodeUTF8))
        self.ubuntuChoice.setText(QtGui.QApplication.translate("Dialog", "Ubuntu(deb)", None, QtGui.QApplication.UnicodeUTF8))
        self.osxChoice.setToolTip(QtGui.QApplication.translate("Dialog", "Solo disponible al correr esta aplicación OsX", None, QtGui.QApplication.UnicodeUTF8))
        self.osxChoice.setText(QtGui.QApplication.translate("Dialog", "OsX(app bundle)", None, QtGui.QApplication.UnicodeUTF8))
        self.windowsChoice.setToolTip(QtGui.QApplication.translate("Dialog", "Solo disponible al correr esta aplicación Windows", None, QtGui.QApplication.UnicodeUTF8))
        self.windowsChoice.setText(QtGui.QApplication.translate("Dialog", "Windows(exe)", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_3.setTitle(QtGui.QApplication.translate("Dialog", "Instrucciones", None, QtGui.QApplication.UnicodeUTF8))
        self.textEdit.setHtml(QtGui.QApplication.translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">1. Haga click en generar clientes para crear un archivo ejecutable nativo para el sistema operativo en el que se ejecuta esta aplicación.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">2. Ejecute el/los cliente/s en cada máquina que desee controlar.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">3. A continuación expere en la pestaña Servidor a que aparezcan las maquinas.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">4. Arrastre o escriba el nombre de un archivo en el campo correspondiente y haga click en la acción que desea ejecutar.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Nota. Los datos de seguridad se guardarán en los clientes.exe y en el servidor.cfg, permitiendo asi una comunicación exclusiva y segura entre ambos. </span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">LABSIA: por motivos de seguridad en este laboratorio el servicio no funcionará en maquinas congeladas.</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.generateClientButton.setText(QtGui.QApplication.translate("Dialog", "Crear Cliente", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.clientTab), QtGui.QApplication.translate("Dialog", "Cliente", None, QtGui.QApplication.UnicodeUTF8))
        self.uploadButton.setText(QtGui.QApplication.translate("Dialog", "Solo enviar archivo", None, QtGui.QApplication.UnicodeUTF8))
        self.uploadAndExecuteButton.setText(QtGui.QApplication.translate("Dialog", "Enviar y ejecutar archivo", None, QtGui.QApplication.UnicodeUTF8))
        self.fileDropTextLine.setText(QtGui.QApplication.translate("Dialog", "Arrastre o escriba aqui el archivo", None, QtGui.QApplication.UnicodeUTF8))
        self.machinesTable.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("Dialog", "Nombre", None, QtGui.QApplication.UnicodeUTF8))
        self.machinesTable.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("Dialog", "Estado", None, QtGui.QApplication.UnicodeUTF8))
        self.machinesTable.horizontalHeaderItem(2).setText(QtGui.QApplication.translate("Dialog", "IP", None, QtGui.QApplication.UnicodeUTF8))
        self.machinesTable.horizontalHeaderItem(3).setText(QtGui.QApplication.translate("Dialog", "Transferencia", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.serverTab), QtGui.QApplication.translate("Dialog", "Servidor", None, QtGui.QApplication.UnicodeUTF8))

##import resources_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

