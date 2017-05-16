#!/usr/bin/python
"""Simple Python Server."""
import argparse
from bbr_logging import debug_print, debug_print_error, debug_print_verbose
import socket
import sys
import time


class Flags(object):
    """Dictionary object to store parsed flags."""

    PORT = "port"
    SIZE = "size"
    parsed_args = None


def parse_args():
    """Parse experimental parameters from the commandline."""
    parser = argparse.ArgumentParser(
        description="Process experimental params.")
    parser.add_argument(Flags.PORT, type=int,
                        help="Enter the port number to connect to.",
                        default=5050)
    parser.add_argument('--size', dest=Flags.SIZE, type=int,
                        help="Size of messages to send.",
                        default=1024)

    Flags.parsed_args = vars(parser.parse_args())
    debug_print_verbose("Parse: " + str(Flags.parsed_args))


def _handle_connection(conn, size):
    num_msg = 0
    start_time = time.time()
    while True:
        conn.settimeout(1.0)
        try:
            msg = conn.recv(size)
        except socket.timeout:
            msg = None
        if not msg:
            break
        num_msg += 1
    elapsed_time = time.time() - start_time
    debug_print_verbose("Num msg: " + str(num_msg))
    debug_print_verbose("Size: " + str(size) + " bytes")
    debug_print_verbose("Time: " + str(elapsed_time))
    goodput = (num_msg * size * 8) / elapsed_time / 1e6
    debug_print("Goodput: " + str(goodput))


def run_server():
    """Run the server continuously."""
    port = Flags.parsed_args[Flags.PORT]
    size = Flags.parsed_args[Flags.SIZE]

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        s.bind(('', port))
    except socket.error:
        debug_print_error("bind error")
        sys.exit(-1)

    s.listen(1)  # only have 1 connection
    debug_print("Awaiting connection on port %d" % port)

    while (True):
        conn, _ = s.accept()
        debug_print("Accepted connection")
        _handle_connection(conn, size)
    s.close()

if __name__ == '__main__':
    parse_args()
    run_server()