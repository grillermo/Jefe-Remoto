#-------------------------------------------------------------------------------
# Name:        configureClient
# Purpose:      generate a .cfg file depending on the requirements
#
# Author:      grillermo
#
# Created:     28/04/2011
# Copyright:   (c) grillermo 2011
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import os

import configobj

class cfgCreator():
    def __init__(self,configurationFile):
        ''' This class implements the methods needed to configure clients.
        At init it writes the configuration file.cfg '''
        if not os.path.isfile(CONFIGURATIONFILE):
            self.config = ConfigObj(CONFIGURATIONFILE)
            self.config.write()

    def setDirs(self,chosenFolder='jeferemoto'):
        if os.name == 'nt':
            HOMEDIR = environ.has_key('HOMEPATH') and environ['HOMEPATH']
            HOMEDIR = HOMEDIR+'\\'+chosenFolder
            ARRIVALFOLDER = HOMEDIR+'\\FILES'
        elif os.name == 'posix':
            HOMEDIR = environ.has_key('HOME') and environ['HOME']
            HOMEDIR = HOMEDIR+'/.'+chosenFolder
            ARRIVALFOLDER = HOMEDIR+'/FILES'
        self.config['HOMEDIR'] = HOMEDIR
        self.config['ARRIVALFOLDER'] = ARRIVALFOLDER
        self.config.write()

    def setSecurityData(self, username,password):
        self.config['USERNAME'] = username
        self.config['PASSWORD'] = password
        self.config.write()

    def setCommunicationData(self,serverIP,PORT=50007,TIMEOUT=5):
        ''' Set the login data the clients will use when broadcasting to
        the server.
        Takes one mandatory argument, a string with the IP of the server.
        Sets the name of the machine as its hostname'''
        if OSname == 'nt':
            process = Popen(['hostname'],stdout=PIPE, stderr=PIPE, shell=True)
            MACHINENAME = process.communicate()[0].rstrip('\r\n')
        elif OSname == 'posix':
            process = Popen(['hostname'],stdout=PIPE, stderr=PIPE, shell=True)
            MACHINENAME = process.communicate()[0].rstrip('\n')
        if type(serverIP) != str:
            print 'the argument must be a string'
            raise
        self.config['MACHINENAME'] = MACHINENAME
        self.config['SERVERIP'] = serverIP
        self.config['PORT'] = PORT
        self.config['TIMEOUT'] = TIMEOUT
        self.config.write()


def main():
    pass

if __name__ == '__main__':
    main()