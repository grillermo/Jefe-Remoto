#!/usr/bin/python

# mainwindow.py

import sys
from PyQt4 import QtGui, QtCore
from os.path import exists
SIGNAL = QtCore.SIGNAL

path = 'c:\\c\\module1.py'

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self.watcher = QtCore.QFileSystemWatcher()
        self.watcher.addPath(path)
        self.connect(self.watcher, SIGNAL("directoryChanged(QString)"),
                     self.printChange)
        self.connect(self.watcher, SIGNAL("fileChanged(QString)"),
                     self.printChange)

    def printChange(self, str1):
        print str1

if exists(path):
    app = QtGui.QApplication(sys.argv)
    main = MainWindow()
    main.hide()
    sys.exit(app.exec_())
else:
    print 'el archivo no existe'