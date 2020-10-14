%load_ext autoreload
%autoreload 2
from checksumdir import dirhash
from pathlib import Path

from fs_ops.sender import Sender

d = Path('D:/Data/raw_sync_test/hash_tests') 
d.exists()
p = d/"F2020-09-11_08-31-54_M200910_03_60.d"

dirhash(p, 'sha256')

s = Sender('192.168.1.200:9002')
s.greet()
s.get_check_sum(r'D:\Data\raw_sync_test\hash_tests\F2020-09-11_08-31-54_M200910_03_60.d')