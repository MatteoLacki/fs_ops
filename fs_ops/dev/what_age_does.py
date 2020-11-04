from fs_ops.utils import age
import os

path = 'C:/Projects/test.txt'

with open(path, 'w') as f:
	f.write('Hello World')

age(path, 's')

with open(path, 'a') as f:
	f.write('Good bye')

age(path, 's', os.path.getmtime)
