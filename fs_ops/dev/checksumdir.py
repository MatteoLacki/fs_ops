%load_ext autoreload
%autoreload 2
from checksumdir import dirhash
from pathlib import Path
from collections import Counter
import logging
import itertools

from fs_ops.utils import age
from fs_ops.base import cp
from fs_ops.sender import Sender
from fs_ops.checksums import check_sum, file_check_sum, all_source_hashes_aggree


logging.basicConfig(filename='test.log',
                    level=logging.INFO)

source = Path(r"D:\Data\raw\F2020-11-09_10-34-00_M201106_044_412.d")
target = Path(r"M:\RAW\F2020-11-09_10-34-00_M201106_044_412.d")
server = Sender('192.168.1.100:9002')
server.greet()
target_hash = server.get_check_sum(target)

all_source_hashes_aggree(source, target, server)


age(source)

def min_age(source):
    if source.is_file():
        paths = {source}
    else:
        paths = set(itertools.chain(source.glob("*"),
                                    source.glob("**/*")))
    return min(age(path) for path in paths)

min_age(source)
