#!/usr/bin/python

from socket import *
import select
import sys
import threading
import time
import config
import SRCDS

def handler(serversocket):
    while 1:
        try:
            data, addr = serversocket.recvfrom(1024, MSG_DONTWAIT)
            if not data:
                break
            else:
                print data
        except error:
            pass

def main():
    host = config.my_host
    port = config.my_port
    threads = []

    addr = (host, port)
    serversocket = socket(AF_INET, SOCK_DGRAM)
    serversocket.bind(addr)
    serversocket.setblocking(0)

    print "Connecting rcon:"
    TF2Server = SRCDS.SRCDS('74.91.115.129', 27015, config.rconPassword, 10)
    serverStatus = TF2Server.rcon_command('status')
    print "status:"
    print serverStatus
    tournamentInfo = TF2Server.rcon_command('tournament_info')
    print "Tourn info: "
    print tournamentInfo
    retval = tournamentInfo = TF2Server.rcon_command('logaddress_add 69.160.42.187:50500')
    print "logaddr returned: "
    print retval

    print "Server is waiting for data\n"
    t = threading.Thread(target=handler, args=(serversocket,))
    t.daemon = True
    threads.append(t)
    t.start()
    while t.isAlive():
        t.join(1)
    serversocket.close()

if __name__ == "__main__":
    main()