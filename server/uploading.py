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
import ftplib
from thread import start_new_thread

from PyQt4.QtCore import SIGNAL, QObject

class uploader(QObject):
    def __init__(self,host):
        ''' takes a host in the form of a string ip and returns and ftplib
        object '''
        self.ftpObject = ftplib.FTP(host,timeout=3)
        if configFile.has_key('USERNAME') and configFile.has_key('PASSWORD'):
            username = configFile['USERNAME']
            password = configFile['PASSWORD']
        else:
            username = str(self.ui.usernameTextBox.text())
            password = str(self.ui.passwordTextBox.text())
        self.ftpObject.login(username,password)

    def upload(filename):
        name,folder = path.split(filename)
        os.chdir(folder) # ftplib only works with files in the cwd
        self.emit(SIGNAL('toggleAnimation'))
        for ip in self.machinesData.values():
            print 'uploading to IP ',ip
            item = self.getMachineItem(ip)
            self.table.scrollToItem(item,QAbstractItemView.EnsureVisible)
            try:
                status = 'Enviando archivo...'
                self.updateMachinesTable(item,transferStatus=status)
                self.initFTPObject(ip)
                self.uploadFile(filename)
                status = 'Transferencia exitosa'
                self.updateMachinesTable(item,transferStatus=status)
            except:
                status = 'Transferencia fallida'
                self.updateMachinesTable(item,transferStatus=status)

        self.emit(SIGNAL('toggleAnimation'))
        if name == 'nt':
            sound = "C:\\c\\jefeRemoto\\master\\audio.wav"
            winsound.PlaySound('%s' % sound, winsound.SND_FILENAME)
        os.chdir(self.cwd)

    def uploadFile(filename):
        fileHandler = open(filename,'rb')
        self.ftpObject.storbinary('STOR '+filename, fileHandler)
        fileHandler.close()
        print 'file %s succesfully sent'%filename
        return True




def main():
    pass

if __name__ == '__main__':
    main()
