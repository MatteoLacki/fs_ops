"""Matteo's simple rsync clone: msync

No support for check-sums (our LAN is stable).
Simple wrapper around robocopy.
"""
import argparse
import logging
import pathlib
from platform import system
from pprint import pprint
import sys

from fs_ops.utils import age
from fs_ops.base import cp, mv, rm
from fs_ops.sender import Sender
from fs_ops.checksums import check_sum as check_sum_here


Path = lambda p: pathlib.Path(p).expanduser().resolve()

epilog = r"""
Example: python msync.py C:\test V:\test *.raw" --min_copy_hours 4 --min_delete_hours 48 --debug
"""

ap = argparse.ArgumentParser(description='Sync files/folders.',
                             formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                             epilog=epilog)
ARG = ap.add_argument
ARG("source", type=Path, help="The folder to copy from.")
ARG('target', type=Path, help='The (network) folder to sync to.')
ARG('patterns', nargs='+', help='Files/folders/patterns (compatible with python glob) to sync.')
ARG('--min_copy_hours',   type=float,  default  = 4.0,
    help='Minimal age in hours for the file to be copied. For a folder, the age of the youngest file within.')
ARG('--min_delete_hours', type=float,  default = -1,
    help='Minimal age in hours for the file to be deleted. For a folder, the age of the youngest file within. Set to -1 not to remove files.')
ARG('--debug', action='store_true', help='Run in debug mode.')
ARG('--log_path', type=Path, help='Path to store logs.',
    default='~/Projects/fs_ops/sync.log' if system() == 'Linux' else 'C:/Projects/fs_ops/sync.log')
ARG('--server_ip_port', help='the.ip.of.server:port')
ARG('--server_message_encoding', help='Message encoding.', default='cp1251')

ap = ap.parse_args()
if ap.debug:
    pprint(ap.__dict__)

logging.basicConfig(filename=ap.log_path, level=logging.INFO,
                    format='%(asctime)s:%(name)s:%(levelname)s:%(message)s:')



if ap.server_ip_port is not None:
    server = Sender(ap.server_ip_port, ap.server_message_encoding)
    if not server.greet(): 
        print("Server down. Not checking hashes is dangerous. Stopping here!!")
        print("Consider setting up the server or running this script without 'server_ip_port' argument.")
        input("Press a key to finish the program.")
        sys.exit()
    check_sum_there = server.get_check_sum
else:
    check_sum_there = check_sum_here = lambda x: 0


def iter_sources_targes(source, target, patterns):
    for pat in patterns:
        for s in source.glob(pat):
            t = target/s.name 
            yield s,t
st = list(sorted(iter_sources_targes(ap.source, ap.target, ap.patterns)))
if ap.debug:
    pprint(st)


for s,t in st:
    if age(s) >= ap.min_copy_hours:
        logging.info(f'Copying {s} to {t}.')
        local_checksum = check_sum_here(s)
        logging.info(f'Sha256 for {s} = {local_checksum}')
        cp(s,t)
        remote_checksum = check_sum_there(t)
        logging.info(f'Sha256 for {t} = {remote_checksum}')
        if local_checksum != remote_checksum:
            loggin.error(f'{s} and {t} have different checksums.')
            input("Press a key to finish the program.")
            sys.exit()
        else:
            logging.info(f'checksums aggree')
            if ap.min_delete_hours >= 0:
                if age(s) >= ap.min_delete_hours:
                    logging.info(f'Removing {s}.')
                    rm(s) 
                else:
                    logging.info(f'{s} is too young to delete: {age(s)}')
            else:
                logging.info('copy only mode')
    else:
        logging.info(f'{s} is too young to copy: {age(s)}')


