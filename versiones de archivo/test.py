import ping, socket
try:
    delay = ping.do_one('www.google.com', timeout=2)
    print delay
except socket.error, e:
    print "Ping Error:", e