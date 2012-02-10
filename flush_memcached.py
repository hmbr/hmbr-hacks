#!/usr/bin/env python

import socket
import argparse

DEFAULT_HOST = "localhost"
DEFAULT_PORT = 11211
FLUSH_COMMAND = "flush_all"
END_COMMAND = "\r\n"
COMMAND_OK = "OK\r\n"


def main():

    parse = argparse.ArgumentParser(description="flush memcached")
    parse.add_argument('--host', default=DEFAULT_HOST, help="memcached host")
    parse.add_argument('--port', default=DEFAULT_PORT,
            type=int, help="memcached port")
    parse.add_argument('time', help="time to flush", nargs='?',
            default=0, type=int)
    parametros = parse.parse_args()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.connect((parametros.host, parametros.port))

        server.send("{} {} {}".format(FLUSH_COMMAND, parametros.time,
            END_COMMAND))

        data = server.recv(1024)
        if (data != COMMAND_OK):
            print data
        server.close()

    except socket.error:
        parse.print_help()

if __name__ == '__main__':
    main()
