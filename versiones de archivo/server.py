import os
import conf
from socket import error as sockError
import Queue
import socket as sk
from time import sleep
from thread import start_new_thread

machines = {}

class Scanner():
    def __init__(self):
        self.memqueue = Queue.Queue()
        self.getMember = self.memqueue.get

    # TO BE CALLED BY SERVERS
    def listen(self):
        start_new_thread(self._listenPings,())

    def _listenPings(self):
        resser = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
        resser.setsockopt(sk.SOL_SOCKET, sk.SO_REUSEADDR, 1)
        resser.setsockopt(sk.SOL_SOCKET, sk.SO_BROADCAST, 1)

        resser.bind((conf.HOST, conf.PORT))
        resser.settimeout(None)

        while True:
            msg, address = resser.recvfrom(1024)
            if msg[:4] == 'STOP':
                break
            elif msg[:4] == 'PING':
                print 'received PING signal from', address
                resser.sendto('PACK' + conf.USERNAME, address)
            else:
                print 'unidentified signal (server-side):', msg, 'from', address, '-> IGNORED'

    # TO BE CALLED BY CLIENTS
    def scan(self, userHandler = lambda addr: None):
        start_new_thread(self._refreshMembersList, tuple([userHandler]))

    def _refreshMembersList(self, userHandler):
        print 'Broadcasting...'
        scannerSock = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
        scannerSock.setsockopt(sk.SOL_SOCKET, sk.SO_BROADCAST, 1)
        scannerSock.settimeout(5)
        scannerSock.sendto('PING' + conf.USERNAME, (conf.BROADCAST, conf.PORT))
        while True:
            try:
                msg, address = scannerSock.recvfrom(1024)
            except sk.timeout:
                print 'scanner timeout'
                break
            if msg[:4] == 'PACK':
                print 'received PACK signal from', address, 'calling handler'
                userHandler(msg[4:], address[0])
            else:
                print 'unidentified signal (client-side):', msg, 'from', address, '-> IGNORED'
        scannerSock.close()

class Networker():
    def __init__(self):
        self.scanner = Scanner()
        self.scanner.listen()
        self.reloadMembers()

    def reloadMembers(self):
        print 'reloading members in the list'
        self.scanner.scan(self.userHandler)

    def userHandler(self,username, address):
        if machines.has_key(username) == False :
            machines[username] = address
            self.emit(SIGNAL('updated'))

        print str(machines)

def main():
    iniciar = Networker()

if __name__ == '__main__':
    main()
