# $Id: tls_ftpd.py 757 2010-11-08 09:51:04Z g.rodola $

"""An RFC-4217 asynchronous FTPS server supporting both SSL and TLS.

Requires PyOpenSSL module (http://pypi.python.org/pypi/pyOpenSSL).
"""

from pyftpdlib import ftpserver
from pyftpdlib.contrib.handlers import TLS_FTPHandler

authorizer = ftpserver.DummyAuthorizer()
authorizer.add_user('user', '12345', 'c:\\', perm='elradfmw')
authorizer.add_anonymous('.')
ftp_handler = TLS_FTPHandler
ftp_handler.certfile = 'keycert.pem'
ftp_handler.authorizer = authorizer
# requires SSL for both control and data channel
#ftp_handler.tls_control_required = True
#ftp_handler.tls_data_required = True
ftpd = ftpserver.FTPServer(('127.0.0.1', 8021), ftp_handler)
ftpd.serve_forever()