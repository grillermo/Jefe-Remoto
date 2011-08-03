#-------------------------------------------------------------------------------
# Application Name:         JefeRemoto
# Module Name:              ServerMain
# Purpose:                  Run services needed in the client
# Author:                   Guillermo Siliceo Trueba
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
#------------------------------------------------------------------------------


from sys import argv, exit
from time import sleep
from os import name, stat, listdir, getcwd, mkdir, system, path, chdir
from subprocess import Popen, PIPE, call
from thread import start_new_thread
import platform
import socket as sk

from ftpserver import *
from configobj import ConfigObj

USER, PASSWORD, SERVERIP = "", "", ""
MAINFOLDER = 'c:\\WINDOWS\\system32\\jefeRemoto'
ARRIVALFOLDERNAME = 'Llegadas'
ARRIVALFOLDER = path.join(MAINFOLDER,ARRIVALFOLDERNAME)

# #######################################
# this code should only run the first time
chdir(MAINFOLDER)

config = ConfigObj('conf.cfg')
if not path.isfile('conf.cfg'):
    try:
        LOCALIP = ([ip for ip in sk.gethostbyname_ex(sk.gethostname())[2] if not ip.startswith("127.")][0])
        MACHINENAME = sk.gethostname()
    except:
        print 'Hubo problemas con la conexión a la red presione una tecla para cerrar este programa'
        raw_input()
        exit()

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
        self.succesfullyReported = False
        if self.reportIn():
            start_new_thread(self.ftpServer,())
        print 'all services started\n'

    def ftpServer(self):
        authorizer = DummyAuthorizer()
        authorizer.add_user(USER,PASSWORD,ARRIVALFOLDER,perm='elradfmw')
        ftp_handler = FTPHandler
        ftp_handler.authorizer = authorizer
        address = (LOCALIP, 21)
        ftpd = FTPServer(address, ftp_handler)
        print 'ftp started succesfully \n'
        ftpd.serve_forever()

    def reportIn(self,PORT=50007,TIMEOUT=10):
        if self.succesfullyReported:
            return 1
        scannerSock = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
        scannerSock.setsockopt(sk.SOL_SOCKET, sk.SO_BROADCAST, 1)
        scannerSock.settimeout(TIMEOUT)
        print 'Sending a HELLO with the username %s\n'%MACHINENAME
        scannerSock.sendto('HELLO' + MACHINENAME, (SERVERIP, PORT))
        print 'PING message sent\n'
        while True:
            try:
                self.msg, self.address = scannerSock.recvfrom(1024)
                print 'waiting for the STOP message\n'
            except sk.timeout:
                print 'scanner timeout\n'
                scannerSock.shutdown(sk.SHUT_RDWR)
                scannerSock.close()
                self.reportIn()
            if self.msg[:4] == 'STOP':
                print 'received STOP signal from\n', self.address
                self.succesfullyReported = 1
                break
            else:
                print 'unidentified signal (client-side):', msg, 'from', address, '-> IGNORED\n'
        print 'succesfully reported back to the server\n'
        scannerSock.close()
        return True

# My implementation-specific code, we have DeepFreeze on our machines and
# we dont want the script to run if the machine is frozen
# just remove it

def main():
    if call('DFC get /ISFROZEN',shell=False): #Deepfreeze docs on remote admin
        pass
    else:
		clientServices()
		while True:
			sleep(60)
if __name__ == '__main__':
    main()
    raw_input()


