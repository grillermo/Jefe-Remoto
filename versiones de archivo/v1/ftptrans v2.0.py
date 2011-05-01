#-------------------------------------------------------------------------------
# Name:        Ftp Admin Sender
# Purpose:     this script allows you to send file script to several different
#              clients that run an ftp server.
#              I wrote this to help me distribute software and updates remotely
# Author:      Guillermo Siliceo Trueba
#
# Created:     05/03/2011
# Copyright:   (c) Guillermo Siliceo Trueba 2011
# Licence:     GPL v2.0
# version:     1.0
# Notes:       In this version i used OO programming and the following extra
#              libraries:
#              easygui
#NOT WORKING VERSION, ONLY FOR REFERENCE#NOT WORKING VERSION, ONLY FOR REFERENCE
#NOT WORKING VERSION, ONLY FOR REFERENCE#NOT WORKING VERSION, ONLY FOR REFERENCE
#NOT WORKING VERSION, ONLY FOR REFERENCE#NOT WORKING VERSION, ONLY FOR REFERENCE
#NOT WORKING VERSION, ONLY FOR REFERENCE#NOT WORKING VERSION, ONLY FOR REFERENCE
#NOT WORKING VERSION, ONLY FOR REFERENCE#NOT WORKING VERSION, ONLY FOR REFERENCE
#-------------------------------------------------------------------------------
from sys import argv
from ftplib import FTP
import ipaddr
import os

def connection(ip,user,password):
    ftp = FTP(ip)
    ftp.timeout = 1
    ftp.login(user,password)
    return ftp

def upload(ftp,file):
    os.chdir("c:\\c\\ftptrans")
    ftp.storbinary("STOR " + file, open(file, "rb"), 1024)

## CONSTANTS ,change here the script hardcoded parameters
#ftp loging information
user = 'labsia'
password = 'labsia'

# error we output when the parameters are sent wrong
usage_error = 'ftptransfer.py limite-inferior-rango-ip \
limite-superior-rango-ip archivo-comprimido.zip script-python.py \n \
     ejemplo: ftptransfer.py 192.168.1.1 192.168.1.254 archivo.doc'

# regular expresion for IP like 255.255.255.0
IPregex = '((?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3})((?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?))'
# got it from http://www.regular-expressions.info/regexbuddy/ipaccurate.html

## CHECKING the user input
if len(argv) != 4:
    print("Número incorrecto de parametros")
    exit(usage_error)

startIP, endIP, file = argv[1], argv[2], argv[3]

# We create our match object
startIP = re.match(IPregex,startIP)
endIP = re.match(IPregex,endIP)

# Checking that our regex gets a match(a valid IP)
if startIP == None or endIP == None:
    print("Escriba IPs validas del tipo 255.255.255.0")
    exit(usage_error)

# The first 3 octects of our IPs
firstThirdInitialIp = re.match(IPregex,startIP).group(1)
firstThirdEndingIp = re.match(IPregex,endIP).group(1)

# Checking that our IPs belong to the same subnet
if firstThirdInitialIp != firstThirdEndingIp:
    print ("Las direcciones IP tienen que estar en el mismo rango de subnet")
    exit(usage_error)

# The last octect of our IPs
startingIP = int(startIP.group(2))
endingIP = int(endIP.group(2))

##UPLOADING our file
# and now we can finally upload our files in bulk
for ip in range(startingIP,endingIP+1):
    currentIP = firstThirdInitialIp+str(ip)
    #first we check that the machine is alive
    if os.system("C:\\Windows\\System32\\ping "+currentIP+" -n 1 -i 6"):
        print("No se pudo establecer conexion con la IP "+currentIP)
    else:
        print("Subiendo el archivo %s a la IP %s"%(file, currentIP),)
        try:
            ftp = connection(currentIP,user,password)
        except:
            print("No se pudo conectar a la IP "+currentIP)
        upload(ftp,file)

try:
    ftp.quit() #lets get out of here
except:
    exit()
