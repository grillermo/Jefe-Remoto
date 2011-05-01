#!/usr/bin/env python


#############################################################################
##
## Copyright (C) 2010 Riverbank Computing Limited.
## Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
## All rights reserved.
##
## This file is part of the examples of PyQt.
##
## $QT_BEGIN_LICENSE:BSD$
## You may use this file under the terms of the BSD license as follows:
##
## "Redistribution and use in source and binary forms, with or without
## modification, are permitted provided that the following conditions are
## met:
##   * Redistributions of source code must retain the above copyright
##     notice, this list of conditions and the following disclaimer.
##   * Redistributions in binary form must reproduce the above copyright
##     notice, this list of conditions and the following disclaimer in
##     the documentation and/or other materials provided with the
##     distribution.
##   * Neither the name of Nokia Corporation and its Subsidiary(-ies) nor
##     the names of its contributors may be used to endorse or promote
##     products derived from this software without specific prior written
##     permission.
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
## "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
## LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
## A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
## OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
## SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
## LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
## DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
## THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
## (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
## OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
## $QT_END_LICENSE$
##
#############################################################################
# ROTA VERSION ROTA VERSION ROTA
# ROTA VERSION ROTA VERSION ROTA
# ROTA VERSION ROTA VERSION ROTA# ROTA VERSION ROTA VERSION ROTA# ROTA VERSION ROTA VERSION ROTA
# ROTA VERSION ROTA VERSION ROTA
# ROTA VERSION ROTA VERSION ROTA# ROTA VERSION ROTA VERSION ROTAvv

from PyQt4 import QtGui, QtCore
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

def setOpenFileName(openFileNameLabel):
    options = QtGui.QFileDialog.Options()
    fileName = QtGui.QFileDialog.getOpenFileName(openFileNameLabel,
                "QFileDialog.getOpenFileName()",
                openFileNameLabel.text(),
                "All Files (*);;Text Files (*.txt)")
    if fileName:
        openFileNameLabel.setText(fileName)

def createIntroPage():
    page = QtGui.QWizardPage()
    page.setTitle(_fromUtf8("Bienvenida"))

    label = QtGui.QLabel("Bienvenido al asistente para transferir y ejecutar\
 archivos en las computadoras de LABSIA")
    label.setWordWrap(True)

    layout = QtGui.QVBoxLayout()
    layout.addWidget(label)
    page.setLayout(layout)

    return page


def createRegistrationPage():
    page = QtGui.QWizardPage()
    page.setTitle("Escoger archivos")
    page.setSubTitle("Please fill both fields.")

    nameLabel = QtGui.QLabel("Name:")
    nameLineEdit = QtGui.QLineEdit()

    emailLabel = QtGui.QLabel("Email address:")
    emailLineEdit = QtGui.QLineEdit()

    openFileNameLabel = QtGui.QLabel()
    openFileNameButton = QtGui.QPushButton("QFileDialog.get&OpenFileName()")

    openFileNameButton = QtGui.QPushButton("QFileDialog.get&OpenFileName()")
    openFileNameButton.clicked.connect(setOpenFileName(openFileNameLabel))

    layout = QtGui.QGridLayout()
    layout.addWidget(nameLabel, 0, 0)
    layout.addWidget(nameLineEdit, 0, 1)
    layout.addWidget(emailLabel, 1, 0)
    layout.addWidget(emailLineEdit, 1, 1)
    layout.addWidget(openFileNameButton, 2, 0)
    layout.addWidget(openFileNameLabel, 2, 1)
    page.setLayout(layout)

    return page


def createConclusionPage():
    page = QtGui.QWizardPage()
    page.setTitle("Conclusion")

    label = QtGui.QLabel("You are now successfully registered. Have a nice day!")
    label.setWordWrap(True)

    layout = QtGui.QVBoxLayout()
    layout.addWidget(label)
    page.setLayout(layout)

    return page


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)

    wizard = QtGui.QWizard()
    wizard.addPage(createIntroPage())
    wizard.addPage(createRegistrationPage())
    wizard.addPage(createConclusionPage())

    wizard.setWindowTitle("Trivial Wizard")
    wizard.show()

    sys.exit(wizard.exec_())
