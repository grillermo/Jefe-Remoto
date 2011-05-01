USER, PASSWORD, SERVERIP ="labsia","labsia","148.214.82.69"
executorFile = 'run.py'
#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      grillermo
#
# Created:     28/04/2011
# Copyright:   (c) grillermo 2011
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

from time import sleep
from os import name, stat, listdir, getcwd, mkdir, system, path
from subprocess import Popen, PIPE, call
from thread import *
import platform
import socket as sk

from ftpserver import *
from configobj import ConfigObj

# #######################################
# this code will only run the first time
config = ConfigObj('conf.cfg')
if not path.isfile('conf.cfg'):
    if name == 'nt':
        ARRIVALFOLDER = getcwd()+'\\files\\'
        mkdir(ARRIVALFOLDER)
    else:
        ARRIVALFOLDER = getcwd()+'/files/'
        mkdir(ARRIVALFOLDER)
    LOCALIP = sk.gethostbyname(sk.gethostname())
    executor = open(ARRIVALFOLDER+'run.py','w')
    executor.close()
    MACHINENAME = sk.gethostname()
    config['LOCALIP'] = LOCALIP
    config['MACHINENAME'] = MACHINENAME
    config['ARRIVALFOLDER'] = ARRIVALFOLDER
    config.write()
else:
    LOCALIP = config['LOCALIP']
    MACHINENAME = config['MACHINENAME']
    ARRIVALFOLDER = config['ARRIVALFOLDER']

class clientServices():
    def __init__(self):
        self.connected = False
        self.startFTP()
        start_new_thread(self.detectChanges,(ARRIVALFOLDER,))
        print 'DEBUG '+'init termino'

    def ftpServer(self):
        authorizer = DummyAuthorizer()
        authorizer.add_user(USER,PASSWORD,ARRIVALFOLDER,perm='elradfmw')
        ftp_handler = FTPHandler
        ftp_handler.authorizer = authorizer
        address = (LOCALIP, 21)
        ftpd = FTPServer(address, ftp_handler)
        ftpd.serve_forever()

    def reportIn(self,SERVERIP,MACHINENAME,PORT=50007,TIMEOUT=5):
        scannerSock = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
        scannerSock.setsockopt(sk.SOL_SOCKET, sk.SO_BROADCAST, 1)
        scannerSock.settimeout(TIMEOUT)
        print 'Broadcasting PING the username %s'%MACHINENAME
        scannerSock.sendto('PING' + MACHINENAME, ('<broadcast>', PORT))
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

    def startFTP(self):
        while self.connected == False:
            sleep(60)
            self.connected = start_new_thread(self.reportIn,(SERVERIP,MACHINENAME))
        start_new_thread(self.ftpServer,())

    def detectChanges(self,folder):
        if platform.system == 'Windows':
            file_to_run = "files\\run.py"
            originalState = stat(file_to_run)[-2]
            while 1:
                sleep(13)
                try:
                    if originalState != stat(older+file_to_run)[-2]:
                        system(file_to_run)
                        print 'hubo cambio motherfocker'
                except:
                    print 'file gone, we just wait until it comes back'
        print 'DEBUG '+' DETECTOR termino'


# My implementation specific code, we have DeepFreeze on our machines and
# we dont want the script to run if the machine is frozen

def isFrozen():
    error = call('DFC get /ISFROZEN',shell=True)
    return error

def main():
    if isFrozen(): #by Deepfreeze docs on remote admin
        pass
    else:
        obj = clientServices()

if __name__ == '__main__':
    main()


# thanks to Tim Golden for the directory changed code
# http://timgolden.me.uk/python/win32_how_do_i/watch_directory_for_changes.html


