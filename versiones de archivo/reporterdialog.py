# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'reporterdialog.ui'
#
# Created: Sun Apr 10 14:53:53 2011
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_reporterDialog(object):
    def setupUi(self, reporterDialog):
        reporterDialog.setObjectName(_fromUtf8("reporterDialog"))
        reporterDialog.resize(665, 335)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(reporterDialog.sizePolicy().hasHeightForWidth())
        reporterDialog.setSizePolicy(sizePolicy)
        reporterDialog.setMinimumSize(QtCore.QSize(665, 0))
        reporterDialog.setMaximumSize(QtCore.QSize(665, 16777215))
        self.gridLayout = QtGui.QGridLayout(reporterDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.gridlayout = QtGui.QGridLayout()
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.reporter = QtGui.QTextBrowser(reporterDialog)
        self.reporter.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.reporter.setLineWrapMode(QtGui.QTextEdit.WidgetWidth)
        self.reporter.setObjectName(_fromUtf8("reporter"))
        self.gridlayout.addWidget(self.reporter, 0, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.interruptButton = QtGui.QPushButton(reporterDialog)
        self.interruptButton.setObjectName(_fromUtf8("interruptButton"))
        self.horizontalLayout.addWidget(self.interruptButton)
        self.closeButton = QtGui.QPushButton(reporterDialog)
        self.closeButton.setObjectName(_fromUtf8("closeButton"))
        self.horizontalLayout.addWidget(self.closeButton)
        self.gridlayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        self.gridLayout.addLayout(self.gridlayout, 0, 0, 1, 1)

        self.retranslateUi(reporterDialog)
        QtCore.QObject.connect(self.closeButton, QtCore.SIGNAL(_fromUtf8("clicked()")), reporterDialog.hide)
        QtCore.QMetaObject.connectSlotsByName(reporterDialog)

    def retranslateUi(self, reporterDialog):
        reporterDialog.setWindowTitle(QtGui.QApplication.translate("reporterDialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.reporter.setHtml(QtGui.QApplication.translate("reporterDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.interruptButton.setText(QtGui.QApplication.translate("reporterDialog", "interrumpir", None, QtGui.QApplication.UnicodeUTF8))
        self.closeButton.setText(QtGui.QApplication.translate("reporterDialog", "cerrar", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    reporterDialog = QtGui.QDialog()
    ui = Ui_reporterDialog()
    ui.setupUi(reporterDialog)
    reporterDialog.show()
    sys.exit(app.exec_())

