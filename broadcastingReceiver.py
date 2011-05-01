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
            if msg[:4] == 'PING':
                print 'received PING signal from', address[0]
                print 'sending STOP signal back to', address[0]
                resser.sendto('STOP', address)
                self.emit(SIGNAL('updateMachines'),msg[4:],address[0])
            else:
                print 'unidentified signal (server-side):', msg, 'from', address, '-> IGNORED'

class TesterClass(QObject):
    def __init__(self):
        QObject.__init__(self)
        self.machines = {}
        self.scanner = Scanner()
        self.connect(self.scanner, SIGNAL('updateMachines'),self.testingSignal)
        self.scanner.listen()

    def testingSignal(self,msg,address):
        self.machines[msg[3:]] = address[0]
        print str(self.machines)


def main():
    start = TesterClass()

if __name__ == '__main__':
    main()