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


def runCompilingJob():
    createClientFile(originalFile,customForClient)
    launchCompiler(toCompile)
    saveClientFile(customForClient)
    ui.tabWidget.setCurrentWidget(ui.serverTab)

def createClientFile(originalFile,customForClient):
    ''' This method will generate a client script for the .py to .exe app
     and then call that app, in this case we are using PyInstaller'''
    username = str(ui.usernameTextBox.text())
    password = str(ui.passwordTextBox.text())
    ip = getLocalIP()

    original = open(originalFile)
    forClient = open(customForClient,"w")
    while 1:
        line = original.readline()
        if not line: break
        line = line.replace('''USER, PASSWORD, SERVERIP ="","",""''',
                            'USER, PASSWORD, SERVERIP = "%s", "%s", "%s"'%
                            (username,password,ip))
        forClient.write(line)
    forClient.close()
    original.close()
    return
    # and now with our script ready we call the compiler

def launchCompiler(filename,flags=' --onefile'):
    ''' Takes a string with the name of our client and calls the compiler
    with the flags hard coded here'''
    command = '%s "%s" %s'%(compiler,filename,flags)
    # remember that compiler and toCompile were create by customizeToOS()
    print command #debugging
    system(command) # block the script until process finishes, thats what
                    # we want
    # once the file is done we save for future use the data the client used
    configFile['USERNAME'] = username
    configFile['PASSWORD'] = password
    configFile.write()
    return
    # the executable is (hopefully)done we can move it where the user wants
    print 'debug compilation \n'+str(text)

def saveClientFile(customForClient):
    options = QFileDialog.ShowDirsOnly
    directory = QFileDialog.getExistingDirectory(
            "Donde desea guardar el ejecutable", getcwd(),options)
    timeString = ' %s%s%s%s%s.exe'%time.localtime()[:5]
    newPath = directory+'\\'+customForClient
    move(customForClient,newPath)
    copy('ftpserver.py',newPath)
    copy('configobj.py',newPath)
    return

def main():
    pass

if __name__ == '__main__':
    main()
