%load_ext autoreload
%autoreload 2
from fs_ops.copy import cp, mv
import shutil
import pathlib

A = 'tests/A'
res = 'tests'

cp('tests/A', 'tests/res')


source, target = 'tests/A','tests/res'
files = []

source = pathlib.Path(source).expanduser().resolve()
target = pathlib.Path(target).expanduser().resolve()

cp(source, target)
mv(source, target)

mv('tests/B/b', 'tests/res/C')
mv('tests/A/a0', 'tests/res')
# cp('tests/A', 'tests/res')

shutil.copy2(source, target)

