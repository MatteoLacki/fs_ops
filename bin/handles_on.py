"""Check if handles are there.
"""
import argparse

from fs_ops.base import no_handles


Path = lambda p: pathlib.Path(p).expanduser().resolve()


ap = argparse.ArgumentParser(description='Sync files/folders.',
                             formatter_class=argparse.ArgumentDefaultsHelpFormatter)
ARG = ap.add_argument
ARG("source", type=Path, help="The file or folder to check handles for.")

ap = ap.parse_args()

if no_handles(ap.source):
    print(f"File/folder {ap.source} has no handles.")
else:
    print(f"File/folder {ap.source} has handles on.")

