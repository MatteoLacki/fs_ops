"""Matteo's simple rsync clone: msync

No support for check-sums (our LAN is stable).
Simple wrapper around robocopy.
"""
import argparse
import pathlib
from platform import system
from pprint import pprint

from fs_ops.utils import age
from fs_ops.base import cp, mv, rm

DEBUG = True
#----------------------------------------------------- Defaults
server_port = '9001'
server_ip = '127.0.1.1' if (DEBUG and system() == "Linux") else '192.168.1.100'
#----------------------------------------------------- Input parsing
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
ARG('--min_delete_hours', type=float,  default = 24.0,
    help='Minimal age in hours for the file to be deleted. For a folder, the age of the youngest file within.')
ARG('--server',  type=str,  default=f"{server_ip}:{server_port}",
    help='IP:PORT of the server that checks the sums.')
ARG('--message_encoding',  type=str,  default='cp1251',
    help='Way the messages are encoded. Defaults to the one used on Windows.')
ap = ap.parse_args()
if DEBUG:
    pprint(ap.__dict__)
#----------------------------------------------------- Filtering older folders.

def iter_sources_targes(source, target, patterns):
    for pat in patterns:
        for s in source.glob(pat):
            t = target/s.name 
            yield s,t

st = list(sorted(iter_sources_targes(ap.source, ap.target, ap.patterns)))
if DEBUG:
    pprint(st)

for s,t in st:
    if age(s) >= ap.min_copy_hours:
        cp(s,t)
        if age(s) >= ap.min_copy_hours:
            rm(s) 
        else:
            print(f'{s} is to young to delete: {age(s)}')
    else:
        print(f'{s} is to young to copy: {age(s)}')  


# Path('~/Projects/fs_ops/res/Z.d').unlink()
# Path('/home/matteo/Projects/fs_ops/res/a.tdf').unlink()
# shutil.rmtree('/home/matteo/Projects/fs_ops/res/Z.d')
# shutil.rmtree('/home/matteo/Projects/fs_ops/res/a.tdf')
# source = Path('/home/matteo/Projects/fs_ops/tests')
# f = '*.d'
# f = 'A.d'
# list(source.glob(f))

# cp('/home/matteo/Projects/fs_ops/tests/A.d/a.tdf',
#    '/home/matteo/Projects/fs_ops/tests')
# cp('/home/matteo/Projects/fs_ops/tests/A.d',
#    '/home/matteo/Projects/fs_ops/res')

# cp('/home/matteo/Projects/fs_ops/tests/A.d/a.tdf',
#    '/home/matteo/Projects/fs_ops/res/z.tdf')
# cp('/home/matteo/Projects/fs_ops/tests/A.d',
#    '/home/matteo/Projects/fs_ops/res/Z.d')



