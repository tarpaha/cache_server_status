#!python2
import socket, sys, logging
from argparse import ArgumentParser

def check_server_status(address, port, version):
    s = socket.socket()
    try:

        vprint('Connecting to {}:{}'.format(address, port))
        s.connect((address, port))
        
        vprint('Sending version')
        version_str = '000000{0:02x}'.format(version)
        bytes_sent = s.send(version_str)
        if bytes_sent != len(version_str):
            return (False, 'Error sending cache server version')
        
        vprint('Receiving answer')
        answer = s.recv(1024)
        if answer != version_str:
            return (False, 'Cache server version differ from {} or server did not answer properly'.format(version))
        
        vprint('Server accepted version')

    except Exception as ex:
        return (False, 'Socket error: ' + str(ex))

    finally:
        s.close()

    return (True, None)


def parse_args(default_port, default_version):
    parser = ArgumentParser(description='Check Unity cache server status')
    parser.add_argument('url',
        help='cache server address, can contain port, default port is {}'.format(default_port))
    parser.add_argument('-v', '--version', dest='version', type=int,
        default=default_version,
        help='cache server version, default is ' + str(default_version))
    parser.add_argument('-q', '--quiet', dest='verbose', action='store_false', default=True, help='be quiet')
    args = parser.parse_args()
    (address, port) = split_url(args.url)
    return (address, int(port) if port != None else default_port , args.version, args.verbose)

def split_url(url):
    values = url.split(':')
    return (url, None) if len(values) < 2 else (values[0], values[1])

default_port = 8126
default_version = 254
verbose = True

def vprint(text):
    if verbose:
        print(text)

if __name__== '__main__' :
    (address, port, version, verbose) = parse_args(default_port, default_version)
    (active, error) = check_server_status(address, port, version)
    if not active:
        if verbose:
            logging.error(error)
        sys.exit(1)
    vprint('Cache server status is ON')
