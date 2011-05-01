from os import environ
from thread import start_new_thread
import socket as sk

def main():
    MACHINENAME = 'LOLA'
    PORT = 50007
    TIMEOUT = 5
    SERVERIP = '148.214.82.69'
    reportIn()

def reporter(SERVERIP, MACHINENAME, PORT=50007,TIMEOUT=5):
    scannerSock = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
    scannerSock.setsockopt(sk.SOL_SOCKET, sk.SO_BROADCAST, 1)
    scannerSock.settimeout(TIMEOUT)
    print 'Broadcasting PING the username %s'%MACHINENAME
    scannerSock.sendto('PING' + MACHINENAME, (SERVERIP, PORT))
    print 'PING message sent'
    while True:
        try:
            msg, address = scannerSock.recvfrom(1024)
            print 'waiting for the STOP message'
        except sk.timeout:
            print 'scanner timeout'
            break
        if msg[:4] == 'STOP':
            print 'received STOP signal from', address
            break
        else:
            print 'unidentified signal (client-side):', msg, 'from', address, '-> IGNORED'
    scannerSock.close()
    return True

def startReporting(SERVERIP, MACHINENAME):
    start_new_thread(reporter,(SERVERIP, MACHINENAME))

if __name__ == '__main__':
    main()