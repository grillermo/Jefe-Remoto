# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\c\jefeRemoto\master\mainWindow.ui'
#
# Created: Sat Jul 30 14:54:04 2011
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
        Dialog.setAutoFillBackground(False)
        self.gridLayout_2 = QtGui.QGridLayout(Dialog)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.tabWidget = QtGui.QTabWidget(Dialog)
        self.tabWidget.setEnabled(True)
        self.tabWidget.setFocusPolicy(QtCore.Qt.NoFocus)
        self.tabWidget.setUsesScrollButtons(True)
        self.tabWidget.setDocumentMode(False)
        self.tabWidget.setTabsClosable(False)
        self.tabWidget.setMovable(False)
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
        self.usernameTextBox.setEnabled(True)
        self.usernameTextBox.setText(_fromUtf8(""))
        self.usernameTextBox.setObjectName(_fromUtf8("usernameTextBox"))
        self.horizontalLayout_3.addWidget(self.usernameTextBox)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.passwordLbl = QtGui.QLabel(self.groupBox)
        self.passwordLbl.setObjectName(_fromUtf8("passwordLbl"))
        self.horizontalLayout_3.addWidget(self.passwordLbl)
        self.passwordTextBox = QtGui.QLineEdit(self.groupBox)
        self.passwordTextBox.setEnabled(True)
        self.passwordTextBox.setObjectName(_fromUtf8("passwordTextBox"))
        self.horizontalLayout_3.addWidget(self.passwordTextBox)
        self.gridLayout_5.addWidget(self.groupBox, 0, 0, 1, 1)
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
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.deleteMachinesButton = QtGui.QCommandLinkButton(self.groupBox_3)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Segoe UI"))
        font.setWeight(50)
        font.setItalic(False)
        font.setBold(False)
        self.deleteMachinesButton.setFont(font)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/resources/delete_64.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.deleteMachinesButton.setIcon(icon1)
        self.deleteMachinesButton.setObjectName(_fromUtf8("deleteMachinesButton"))
        self.horizontalLayout.addWidget(self.deleteMachinesButton)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.generateClientButton = QtGui.QCommandLinkButton(self.groupBox_3)
        self.generateClientButton.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.generateClientButton.sizePolicy().hasHeightForWidth())
        self.generateClientButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Segoe UI"))
        font.setWeight(50)
        font.setItalic(False)
        font.setUnderline(False)
        font.setBold(False)
        self.generateClientButton.setFont(font)
        self.generateClientButton.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.generateClientButton.setAutoFillBackground(False)
        self.generateClientButton.setInputMethodHints(QtCore.Qt.ImhNone)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/resources/present_64.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.generateClientButton.setIcon(icon2)
        self.generateClientButton.setCheckable(False)
        self.generateClientButton.setAutoRepeat(False)
        self.generateClientButton.setAutoExclusive(False)
        self.generateClientButton.setObjectName(_fromUtf8("generateClientButton"))
        self.horizontalLayout.addWidget(self.generateClientButton)
        self.gridLayout_4.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        self.gridLayout_5.addWidget(self.groupBox_3, 1, 0, 1, 2)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/resources/user_64.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.clientTab, icon3, _fromUtf8(""))
        self.serverTab = QtGui.QWidget()
        self.serverTab.setObjectName(_fromUtf8("serverTab"))
        self.gridLayout = QtGui.QGridLayout(self.serverTab)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayoutActionBtns = QtGui.QHBoxLayout()
        self.horizontalLayoutActionBtns.setObjectName(_fromUtf8("horizontalLayoutActionBtns"))
        self.uploadButton = QtGui.QCommandLinkButton(self.serverTab)
        self.uploadButton.setAcceptDrops(False)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/resources/right_64.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.uploadButton.setIcon(icon4)
        self.uploadButton.setObjectName(_fromUtf8("uploadButton"))
        self.horizontalLayoutActionBtns.addWidget(self.uploadButton)
        self.gridLayout.addLayout(self.horizontalLayoutActionBtns, 8, 0, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.chooseFileButton = QtGui.QPushButton(self.serverTab)
        self.chooseFileButton.setObjectName(_fromUtf8("chooseFileButton"))
        self.horizontalLayout_2.addWidget(self.chooseFileButton)
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
        self.fileDropTextLine.setText(_fromUtf8(""))
        self.fileDropTextLine.setDragEnabled(True)
        self.fileDropTextLine.setObjectName(_fromUtf8("fileDropTextLine"))
        self.horizontalLayout_2.addWidget(self.fileDropTextLine)
        self.pingMachinesButton = QtGui.QPushButton(self.serverTab)
        self.pingMachinesButton.setObjectName(_fromUtf8("pingMachinesButton"))
        self.horizontalLayout_2.addWidget(self.pingMachinesButton)
        self.gridLayout.addLayout(self.horizontalLayout_2, 4, 0, 1, 1)
        self.machinesTable = QtGui.QTableWidget(self.serverTab)
        self.machinesTable.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.machinesTable.sizePolicy().hasHeightForWidth())
        self.machinesTable.setSizePolicy(sizePolicy)
        self.machinesTable.setMouseTracking(True)
        self.machinesTable.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.machinesTable.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.machinesTable.setAcceptDrops(False)
        self.machinesTable.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.machinesTable.setAlternatingRowColors(True)
        self.machinesTable.setObjectName(_fromUtf8("machinesTable"))
        self.machinesTable.setColumnCount(5)
        self.machinesTable.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.machinesTable.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.machinesTable.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.machinesTable.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.machinesTable.setHorizontalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.machinesTable.setHorizontalHeaderItem(4, item)
        self.machinesTable.horizontalHeader().setStretchLastSection(True)
        self.machinesTable.verticalHeader().setStretchLastSection(False)
        self.gridLayout.addWidget(self.machinesTable, 1, 0, 1, 1)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/resources/network-receive.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.serverTab, icon5, _fromUtf8(""))
        self.gridLayout_2.addWidget(self.tabWidget, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Jefe Remoto", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("Dialog", "Datos de seguridad", None, QtGui.QApplication.UnicodeUTF8))
        self.userLbl.setText(QtGui.QApplication.translate("Dialog", "Usuario", None, QtGui.QApplication.UnicodeUTF8))
        self.passwordLbl.setText(QtGui.QApplication.translate("Dialog", "Contraseña", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_3.setTitle(QtGui.QApplication.translate("Dialog", "Instrucciones", None, QtGui.QApplication.UnicodeUTF8))
        self.textEdit.setHtml(QtGui.QApplication.translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt; font-weight:600;\">Como utilizar este programa</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt; font-weight:600;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Nota previa: la funcionalidad de crear nuevos clientes está deshabilitada por no estar completa. Esta ayuda será útil para la pestaña de servidor.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">* Inicie este programa antes de iniciar todas las maquinas para que estas puedan reportarse exitosamente.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">* Este programa solo funcionará con las máquinas descongeladas.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">* Si desea enviar archivos para que sean ejecutados estos deben ser .exe .msi .py .ahk .</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">* Cualquier archivo enviado se guardará en las máquinas en la siguiente ruta &quot;c:/windows/system32/jefeRemoto/llegadas&quot;.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Si tiene problemas para detectar las máquinas asegurese de la conectividad física y reinicielas.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Si tienes alguna duda escribeme a @grillermo (mi cuenta de twitter) o a mi correo electrónico guillermo.siliceo@gmail.com</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.deleteMachinesButton.setToolTip(QtGui.QApplication.translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Esto borrará la lista de clientes detectados. Si va a crear un nuevo cliente haga click aquí para empezar con una lista limpia.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.deleteMachinesButton.setStatusTip(QtGui.QApplication.translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\\n<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\\np, li { white-space: pre-wrap; }\\n</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\\n<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Esto borrará la lista de clientes detectados. Si desea una nueva lista haga click aquí.</span></p>\\n<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.deleteMachinesButton.setWhatsThis(QtGui.QApplication.translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Esto borrará la lista de clientes detectados. Si desea una nueva lista haga click aquí.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.deleteMachinesButton.setText(QtGui.QApplication.translate("Dialog", "Limpiar lista de clientes", None, QtGui.QApplication.UnicodeUTF8))
        self.generateClientButton.setText(QtGui.QApplication.translate("Dialog", "Crear Cliente", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.clientTab), QtGui.QApplication.translate("Dialog", "Clientes", None, QtGui.QApplication.UnicodeUTF8))
        self.uploadButton.setToolTip(QtGui.QApplication.translate("Dialog", "Se enviará el archivo a las maquinas palomeadas. Puede seleccionarlas o deseleccionarlas haciendo click en la cabezera de su columna.", None, QtGui.QApplication.UnicodeUTF8))
        self.uploadButton.setStatusTip(QtGui.QApplication.translate("Dialog", "Se enviará el archivo a las maquinas palomeadas. Puede seleccionarlas o deseleccionarlas haciendo click en la cabezera de su columna.", None, QtGui.QApplication.UnicodeUTF8))
        self.uploadButton.setWhatsThis(QtGui.QApplication.translate("Dialog", "Se enviará el archivo a las maquinas palomeadas. Puede seleccionarlas o deseleccionarlas haciendo click en la cabezera de su columna.", None, QtGui.QApplication.UnicodeUTF8))
        self.uploadButton.setText(QtGui.QApplication.translate("Dialog", "Enviar archivo", None, QtGui.QApplication.UnicodeUTF8))
        self.chooseFileButton.setText(QtGui.QApplication.translate("Dialog", "Elegir archivo", None, QtGui.QApplication.UnicodeUTF8))
        self.pingMachinesButton.setToolTip(QtGui.QApplication.translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt; font-weight:600;\">F5</span><span style=\" font-size:8pt;\"> - hace un ping a todas las maquinas en la lista y reporta su estado.</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.pingMachinesButton.setStatusTip(QtGui.QApplication.translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\\n<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\\np, li { white-space: pre-wrap; }\\n</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\\n<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt; font-weight:600;\">F5</span><span style=\" font-size:8pt;\"> - hace un ping a todas las maquinas en la lista y reporta su estado.</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.pingMachinesButton.setWhatsThis(QtGui.QApplication.translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt; font-weight:600;\">F5</span><span style=\" font-size:8pt;\"> - hace un ping a todas las maquinas en la lista y reporta su estado.</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.pingMachinesButton.setText(QtGui.QApplication.translate("Dialog", "Checar conectividad", None, QtGui.QApplication.UnicodeUTF8))
        self.machinesTable.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("Dialog", "Nombre", None, QtGui.QApplication.UnicodeUTF8))
        self.machinesTable.horizontalHeaderItem(2).setText(QtGui.QApplication.translate("Dialog", "Estado", None, QtGui.QApplication.UnicodeUTF8))
        self.machinesTable.horizontalHeaderItem(3).setText(QtGui.QApplication.translate("Dialog", "IP", None, QtGui.QApplication.UnicodeUTF8))
        self.machinesTable.horizontalHeaderItem(4).setText(QtGui.QApplication.translate("Dialog", "Transferencia", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.serverTab), QtGui.QApplication.translate("Dialog", "Servidor", None, QtGui.QApplication.UnicodeUTF8))

import resources_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

