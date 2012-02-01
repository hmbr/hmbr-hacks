#!/usr/bin/env python

import socket
import getopt
import sys

DEFAULT_HOST = "localhost"
DEFAULT_PORT = 11211
FLUSH_COMMAND = "flush_all"
END_COMMAND = "\r\n"
COMMAND_OK = "OK\r\n"


def help_msg():
    print """
    Usage : script [OPTIONS] [TIME_TO_EXPIRE]
    OPTIONS:
        [--help]                    this help
        [-h | --host] <host>        host
        [-p | --port] <port>        port
    TIME_TO_EXPIRE is the time to expire, can be any non-negative number
    """


def main():
    host = DEFAULT_HOST
    port = DEFAULT_PORT
    time = 0

    try:
        opts, args = getopt.getopt(sys.argv[1:], "h:p:",
                ["host=", "port=", "help"])
    except getopt.GetoptError:
        help_msg()
        sys.exit()

    for o, a in opts:
        if o in ("--help"):
            help_msg()
            sys.exit()
        if o in ("-h", "--host"):
            host = a
        if o in ("-p", "--port"):
            if (a.isdigit() == True):
                port = int(a)
            else:
                help_msg()
                sys.exit()

    if (len(args) == 1):
        if (args[0] == "now"):
            time = 0
        elif (args[0].isdigit() == True):
            time = int(args[0])
        else:
            help_msg()
            sys.exit()
    elif (len(args) > 1):
        help_msg()
        sys.exit()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.connect((host, port))

        server.send("{} {} {}".format(FLUSH_COMMAND, time, END_COMMAND))

        data = server.recv(1024)
        if (data != COMMAND_OK):
            print data
        server.close()

    except socket.error:
        help_msg()
        sys.exit()

if __name__ == '__main__':
    main()
