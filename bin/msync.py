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
ARG('--debug', action='store_true', help='Run in debug mode.')


ap = ap.parse_args()
if ap.debug:
    pprint(ap.__dict__)


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
        cp(s,t)
        if age(s) >= ap.min_delete_hours:
            rm(s) 
        else:
            print(f'{s} is too young to delete: {age(s)}')
    else:
        print(f'{s} is too young to copy: {age(s)}')  


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



