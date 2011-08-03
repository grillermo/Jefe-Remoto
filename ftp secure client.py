from ftplib import FTP_TLS
ftps = FTP_TLS('127.0.0.1:8021','user','12345',keyfile='privateKey.key')
ftps.login()           # login anonymously before securing control channel
ftps.prot_p()          # switch to secure data connection
print ftps.retrlines('LIST')