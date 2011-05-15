#-------------------------------------------------------------------------------
# Application Name:        JefeRemoto
# Module Name:             ServerMain
# Purpose:              Run services needed in the client, only using python
#                       standard libraries,
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
USER, PASSWORD, SERVERIP ="","",""

from sys import argv
from time import sleep
from os import name, stat, listdir, getcwd, mkdir, system, path
from subprocess import Popen, PIPE, call
from thread import start_new_thread
import platform
import socket as sk

from ftpserver import *
from configobj import ConfigObj

# #######################################
# this code will only run the first time
config = ConfigObj('conf.cfg')
if not path.isfile('conf.cfg'):
    if platform.system == 'Windows':
        ARRIVALFOLDER = getcwd()
        exe = argv[0]
        print ' opening firewall for \n'+exe
        os.system('netsh firewall set allowedprogram %s JefeRemoto Enable\n'%exe)
    else:
        ARRIVALFOLDER = getcwd()+'/Tools/'
        mkdir(ARRIVALFOLDER)
    LOCALIP = sk.gethostbyname(sk.gethostname())
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

    def reportIn(self,PORT=50007,TIMEOUT=5):
        scannerSock = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
        scannerSock.setsockopt(sk.SOL_SOCKET, sk.SO_BROADCAST, 1)
        scannerSock.settimeout(TIMEOUT)
        print 'Sending a HELLO with the username %s\n'%MACHINENAME
        scannerSock.sendto('HELLO' + MACHINENAME, (SERVERIP, PORT))
        print 'PING message sent\n'
        while True:
            try:
                msg, address = scannerSock.recvfrom(1024)
                print 'waiting for the STOP message\n'
            except sk.timeout:
                print 'scanner timeout\n'
                break
            if msg[:4] == 'STOP':
                print 'received STOP signal from\n', address
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


