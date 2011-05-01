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
from os import path
from configobj import ConfigObj

class cfgCreator():
    def __init__(self,CONFIGURATIONFILE):
        ''' This class implements the methods needed to configure clients.
        At init it writes the configuration file.cfg '''
        if not path.isfile(CONFIGURATIONFILE):
            self.config = ConfigObj(CONFIGURATIONFILE)
            self.config['INSTALLED'] = 'False'
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
        if type(serverIP) != str:
            print 'the argument must be a string'
            raise
        self.config['SERVERIP'] = serverIP
        self.config['PORT'] = PORT
        self.config['TIMEOUT'] = TIMEOUT
        self.config.write()


def main():
    pass

if __name__ == '__main__':
    main()