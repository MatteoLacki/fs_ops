"""Matteo's simple rsync clone: msync

No support for check-sums (our LAN is stable).
"Simple" wrapper around robocopy.
General remark: fuck Windows.

Rules:
When we copy things on the server, we then check their hashes.
We only check the hashes of files.
Each time we copy something, we only check the hashes of things that can be copied.
"""
import argparse
import logging
import pathlib
from platform import system
from pprint import pprint
import sys

from fs_ops.utils import min_age
from fs_ops.base import cp, mv, rm, no_handles
from fs_ops.sender import Sender
from fs_ops.checksums import all_source_hashes_aggree


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
    help='Minimal age in hours for the file to be copied. For a folder, the age of the youngest file within. We count time since last modification.')
ARG('--min_delete_hours', type=float,  default = -1,
    help='Minimal age in hours for the file to be deleted. For a folder, the age of the youngest file within. Set to -1 not to remove files.')
ARG('--debug', action='store_true', help='Run in debug mode.')
ARG('--log_path', type=Path, help='Path to store logs.',
    default='~/Projects/fs_ops/sync.log' if system() == 'Linux' else 'C:/Projects/fs_ops/sync.log')
ARG('--server_ip_port', help='the.ip.of.server:port')
ARG('--server_message_encoding', help='Message encoding.', default='cp1251')
ARG('--error_path', type=Path, help='Path to error logs.',
    default='C:/Users/Admin/Desktop/copy_errors.txt')

ap = ap.parse_args()
if ap.debug:
    pprint(ap.__dict__)

logging.basicConfig(filename=ap.log_path, level=logging.INFO,
                    format='%(asctime)s:%(name)s:%(levelname)s:%(message)s:')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logging.getLogger('').addHandler(console)
log = logging.getLogger('syncFiles.py')


if ap.server_ip_port is not None:
    server = Sender(ap.server_ip_port, ap.server_message_encoding)
    if not server.greet(): 
        print("Server down. Not checking hashes is dangerous. Stopping here!!\nConsider setting up the server or running this script without 'server_ip_port' argument.")
        log.error("Server down.")
        input("Press a key to finish the program.")
        sys.exit()
else:
    all_source_hashes_aggree = lambda x: True


def iter_sources_targes(source, target, patterns):
    for pat in patterns:
        for s in source.glob(pat):
            t = target/s.name 
            yield s,t


assert ap.min_copy_hours < ap.min_delete_hours, "You will delete the files that were not copied! Naugthy, naugthy..."


sources_and_targets = list(sorted(iter_sources_targes(ap.source, ap.target, ap.patterns)))
if ap.debug:
    pprint(sources_and_targets)


for s,t in sources_and_targets:
    try:
        age = min_age(s, unit='h')
    except ValueError as e:
        with open(ap.error_path,'a') as f:
            f.write(f"Problem with {s}\n{repr(e)}.\nCheck proper logs at {ap.log_path}!")            
        continue
    if age >= ap.min_copy_hours:
        log.info(f'Copying {s} to {t}.')
        cp(s,t)
        # Check that all files in source have the same hashes as 
        # their equivalents on the target
        if all_source_hashes_aggree(s, t, server):
            if ap.min_delete_hours >= 0:
                if age >= ap.min_delete_hours and no_handles(s):
                    log.info(f'Removing {s}.')
                    try:
                        rm(s)
                    except FileExistsError as e:
                        with open(ap.error_path,'a') as f:
                            f.write(f"Problem with {s}\n{repr(e)}")          
                else:
                    log.info(f'{s} is too young to delete: min age = {age}')
            else:
                log.info('copy only mode')
        else:
            log.error(f'{s} and {t} have different checksums.')
            sys.exit()
    else:
        log.info(f'{s} is too young to copy: min age = {age}')


