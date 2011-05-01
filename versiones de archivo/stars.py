import math, random, sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import subprocess

class Window(QWidget):

    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        self.thread = Worker()
        label = QLabel(self.tr("Number of stars:"))
        self.spinBox = QSpinBox()
        self.spinBox.setMaximum(10000)
        self.spinBox.setValue(100)
        self.startButton = QPushButton(self.tr("&Start"))
        self.viewer = QTextBrowser()
        self.viewer.setFixedSize(300, 300)

        # caputador de se?ales
        self.connect(self.thread, SIGNAL("finished()"), self.updateUi)
        self.connect(self.thread, SIGNAL("terminated()"), self.updateUi)
        self.connect(self.thread, SIGNAL("output(QRect, QImage)"), self.addImage)
        self.connect(self.startButton, SIGNAL("clicked()"), self.runJob)

        layout = QGridLayout()
        layout.addWidget(label, 0, 0)
        layout.addWidget(self.spinBox, 0, 1)
        layout.addWidget(self.startButton, 0, 2)
        layout.addWidget(self.viewer, 1, 0, 1, 3)
        self.setLayout(layout)

        self.setWindowTitle(self.tr("Simple Threading Example"))

    def runJob(self):
        self.spinBox.setReadOnly(True)
        self.startButton.setEnabled(False)
        self.thread.render()

    def addImage(self, rect, image):

        self.viewer.update(rect)

    def updateUi(self):

        self.spinBox.setReadOnly(False)
        self.startButton.setEnabled(True)

class Worker(QThread):

    def __init__(self, parent = None):

        QThread.__init__(self, parent)
        self.exiting = False

    def __del__(self):

        self.exiting = True
        self.wait()

    def render(self):
        self.start()

    def run(self):

        # Note: This is never called directly. It is called by Qt once the
        # thread environment has been set up.

        machine = '192.168.1.102'
        currentPing = subprocess.Popen('ping '+machine,
                                stdout=subprocess.PIPE,
                                shell=True)
        returnStr = currentPing.stdout.read()
        self.viewer.append(returnStr)

        self.emit(SIGNAL("output(QRect, QImage)"),
                  QRect(x - self.outerRadius, y - self.outerRadius,
                        self.outerRadius * 2, self.outerRadius * 2), image)
        n -= 1


if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
