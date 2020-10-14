"""Matteo's simple rsync clone: msync

No support for check-sums (our LAN is stable).
Simple wrapper around robocopy.
"""
import argparse
import logging
import pathlib
from platform import system
from pprint import pprint

from fs_ops.utils import age
from fs_ops.base import cp, mv, rm

Path = lambda p: pathlib.Path(p).expanduser().resolve()

ap = argparse.ArgumentParser(description='Sync files/folders.',
                             formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                             epilog=r"Example: python msync.py C:\test V:\test *.raw")
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

ap = ap.parse_args()
if ap.debug:
    pprint(ap.__dict__)

logging.basicConfig(filename=ap.log_path, level=logging.INFO,
                    format='%(asctime)s:%(name)s:%(levelname)s:%(message)s:')

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
        cp(s,t)
        if ap.min_delete_hours >= 0 and age(s) >= ap.min_delete_hours:
            logging.info(f'Removing {s}.')
            rm(s) 
        else:
            logging.info(f'{s} is too young to delete: {age(s)}')
    else:
        logging.info(f'{s} is too young to copy: {age(s)}')



