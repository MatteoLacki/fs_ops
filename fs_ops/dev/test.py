%load_ext autoreload
%autoreload 2
from fs_ops.base import cp, mv
import shutil
import pathlib

A = 'tests/A'
res = 'tests'

cp('tests/A', 'tests/res')
mv('tests/A', 'tests/res')
mv('tests/B', 'tests/res2')

source, target = 'tests/A','tests/res'
files = []

source = pathlib.Path(source).expanduser().resolve()
target = pathlib.Path(target).expanduser().resolve()

cp(source, target)
mv(source, target)

mv('tests/B/b', 'tests/res')
# cp('tests/A', 'tests/res')

shutil.copy2(source, target)
