%load_ext autoreload
%autoreload 2
from checksumdir import dirhash
from pathlib import Path

from fs_ops.base import cp
from fs_ops.sender import Sender
from fs_ops.checksums import check_sum

d = Path('D:/Data/raw_sync_test/hash_tests') 
d.exists()
file = "F9-9-2020_14-59-30_Training2_56.d"
p = d/file

source_hash = dirhash(p, 'sha256')
target = Path("M:/RAW_test")/file
cp(p, target)

t = Sender('192.168.1.100:9002')
t.greet()
target_hash = t.get_check_sum(target)

source_hash == target_hash

# t.get_check_sum(target) == check_sum(r'D:\Data\raw_sync_test\hash_tests\F9-9-2020_14-59-30_Training2_56.d')
# t.get_check_sum(r'M:\test_sync2\F9-9-2020_14-59-30_Training2_56.d\analysis.baf') == check_sum(r'D:\Data\raw_sync_test\hash_tests\F9-9-2020_14-59-30_Training2_56.d\analysis.baf')

# check_sum(r'D:\Data\raw_sync_test\HASSh_tests\F9-9-2020_14-59-30_Training2_56.d')