from PyQt4.QtCore import *
from PyQt4.QtGui import *

p = QProcess()
env = QProcess.systemEnvironment()
env.append( " 192.168.1.106" )
p.setEnvironment(env)
p.start( "ping" )