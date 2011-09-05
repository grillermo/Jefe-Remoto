#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      grillermo
#
# Created:     07/07/2011
# Copyright:   (c) grillermo 2011
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python
from configobj import ConfigObj #allow us to treat a file as a dict, awesome!

def loadData():
    configFile = ConfigObj('configFile.cfg')
    if not path.isfile('configFile.cfg'):
        configExists = False
        configFile.write()
    else:
        configExists = True
    machinesData = ConfigObj('machines.list') ## here we will save our machines list
    if not path.isfile('machines.list'):
        machinesData.write()
    return configFile,machinesData,configExists

def saveConfig(username,password):
    configFile['USERNAME'] = username
    configFile['PASSWORD'] = password
    configFile.write()


def main():
    pass

if __name__ == '__main__':
    main()
