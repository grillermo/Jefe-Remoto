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
executorFile = 'run.py'

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
        if start_new_thread(self.reportIn,()):
            start_new_thread(self.detectChanges, ())
            start_new_thread(self.ftpServer,())
        print 'DEBUG '+'init termino'

    def ftpServer(self):
        authorizer = DummyAuthorizer()
        authorizer.add_user(USER,PASSWORD,ARRIVALFOLDER,perm='elradfmw')
        ftp_handler = FTPHandler
        ftp_handler.authorizer = authorizer
        address = (LOCALIP, 21)
        ftpd = FTPServer(address, ftp_handler)
        ftpd.serve_forever()

    def reportIn(self,PORT=50007,TIMEOUT=5):
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

    def detectChanges(self):
        if platform.system == 'Windows':
            file_to_run = "files\\run.py"
            originalState = stat(file_to_run)[-2]
            while 1:
                sleep(60)
                try:
                    if originalState != stat(older+file_to_run)[-2]:
                        system(file_to_run)
                        print 'something changed'
                except:
                    print 'file gone, we just wait until it comes back'
        print 'DEBUG '+' DETECTOR termino'


# My implementation-specific code, we have DeepFreeze on our machines and
# we dont want the script to run if the machine is frozen
# just remove it
def main():
    if call('DFC get /ISFROZEN',shell=False): #Deepfreeze docs on remote admin
        pass
    else:
        clientServices()

if __name__ == '__main__':
    main()


# thanks to Tim Golden for the directory changed code
# http://timgolden.me.uk/python/win32_how_do_i/watch_directory_for_changes.html

