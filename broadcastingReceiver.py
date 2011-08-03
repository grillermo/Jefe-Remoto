# Application Name:        broadcastingReceiver
# Module Name:             ServerMain
# Purpose:              Provide an interface so the clients can connect their
#                       broadcasted signals
# Author:      Guillermo Siliceo Trueba
#
# Created:     23/04/2011
# Licence:
'''
   Copyright 2011 Guillermo Siliceo Trueba

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
'''
#-------------------------------------------------------------------------------
import socket as sk
from time import sleep
from PyQt4.QtCore import QObject,SIGNAL

stop = ''
HOST = ''
PORT = 50007

class Scanner(QObject):
    def __init__(self):
        QObject.__init__(self)

    def listen(self):
        resser = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
        resser.setsockopt(sk.SOL_SOCKET, sk.SO_REUSEADDR, 1)
        resser.setsockopt(sk.SOL_SOCKET, sk.SO_BROADCAST, 1)

        resser.bind((HOST, PORT))
        resser.settimeout(None)

        while True:
            msg, address = resser.recvfrom(1024)
            if msg[:5] == 'HELLO':
##                print 'received HELLO signal from', address[0]
##                print 'sending STOP signal back to', address[0]
                resser.sendto('STOP', address)
                status = 'Conectada'
                self.emit(SIGNAL('addMachines'),msg[5:],address[0])
            else:
                pass
##                print 'unidentified signal (server-side):', msg, 'from', address, '-> IGNORED'

class TesterClass(QObject):
    def __init__(self):
        QObject.__init__(self)
        self.machines = {}
        self.scanner = Scanner()
        self.connect(self.scanner, SIGNAL('addMachines'),self.testingSignal)
        self.scanner.listen()

    def testingSignal(self,msg,address):
        self.machines[msg[3:]] = address[0]
        print str(self.machines)


def main():
    start = TesterClass()

if __name__ == '__main__':
    main()