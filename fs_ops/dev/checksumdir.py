%load_ext autoreload
%autoreload 2
from checksumdir import dirhash
from pathlib import Path
from collections import Counter
import logging
import itertools

from fs_ops.utils import age
from fs_ops.base import cp, no_handles
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


file = r"D:\Data\raw\M201203_006_Slot1-1_1_701.d\c37c7911-0a52-4110-96c3-15b5b1718389_1.mcf_idx"

no_handles(r"D:\Data\raw\M201203_006_Slot1-1_1_701.d\SyncHelper")
no_handles(r"D:\Data\raw\M201203_006_Slot1-1_1_701.d\SyncHelper")
no_handles(r"D:\Data\raw - Copy\F2020-11-09_10-34-00_M201106_044_412.d\SyncHelper")
no_handles(r"D:\Data\raw - Copy\F2020-11-09_10-34-00_M201106_044_412.d")

no_handles(r"D:\Data\raw\M201203_006_Slot1-1_1_701.d")
no_handles(r"D:\Data\raw\M201203_006_Slot1-1_1_701.d\analysis.tdf_bin")
