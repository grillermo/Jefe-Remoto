#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      grillermo
#
# Created:     07/07/2011
# Copyright:   (c) grillermo 2011
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python
import socket as sk
from thread import start_new_thread

from PyQt4.QtCore import QObject,SIGNAL

class Scanner(QObject):
    def __init__(self,HOST='',PORT=50007):
        QObject.__init__(self)
        self.HOST = HOST
        self.PORT = PORT

    def listen(self):
        start_new_thread(listener,())

    def listener(self):
        resser = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
        resser.setsockopt(sk.SOL_SOCKET, sk.SO_REUSEADDR, 1)
        resser.setsockopt(sk.SOL_SOCKET, sk.SO_BROADCAST, 1)

        resser.bind((HOST, PORT))
        resser.settimeout(None)

        while True:
            msg, address = resser.recvfrom(1024)
            if msg[:5] == 'HELLO':
                print 'received HELLO signal from', address[0]
                print 'sending STOP signal back to', address[0]
                resser.sendto('STOP', address)
                self.emit(SIGNAL('addMachines'),msg[5:],address[0])
            else:
                print 'unidentified signal (server-side):', msg, 'from', address, '-> IGNORED'

def PingMachines(emmiter,machinesItems):
    start_new_thread(pingThem,(emmiter,machinesItems))

def pingThem(machinesItems,timeout=2):
    ''' Emits a signal each time a machine is found alive '''
    for ip in machinesItems.keys():
        _result = ping.do_one(ip,timeout)
        print _result
        if type(_result) == float:
            isAlive = True
            print 'ip %s alive'%ip
        else:
            isAlive = False
            print 'ip %s dead'%ip
        emmiter.emit(SIGNAL('updateStatus'),self.machinesItems[ip],isAlive)

class TestTheScanner(QObject):
    def __init__(self):
        QObject.__init__(self)
        self.scanner = Scanner()
        self.connect(self.scanner, SIGNAL('addMachines'),self.testingSignal)
        self.scanner.listen()

    def testingSignal(self,msg,address):
        self.machines[msg[3:]] = address[0]
        print str(self.machines)

def main():
    start = TestTheScanner()

if __name__ == '__main__':
    main()
