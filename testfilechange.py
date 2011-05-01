original = open("clientMain.py")
forClient = open("clientMainCustom.py","w")
while 1:
    line = original.readline()
    if not line: break
    line = line.replace('USERNAME, PASSWORD, SERVERIP ="","",""',
        'USERNAME, PASSWORD, SERVERIP = "%s", "%s", "%s"'%('lol','huhu','hehe'))
    forClient.write(line)
forClient.close()
original.close()