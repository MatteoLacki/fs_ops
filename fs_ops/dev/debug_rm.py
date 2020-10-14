%load_ext autoreload
%autoreload 2
import os
import pathlib
from pathlib import Path
import shutil
import subprocess

from fs_ops.base import rm

p = Path('D:/Data/raw_test_msync/F2020-09-10_17-31-50_Hela200ng_uL_59.d')
p.exists()

shutil.rmtree(str(p))
shutil.rmtree(str(p))

p.unlink()
os.remove(p)
os.rmdir(p)
os.rmdir(p/"55min Methode Set_59.m")
os.chmod(p/"55min Methode Set_59.m", 0o777)
(p/"55min Methode Set_59.m").unlink()
os.chmod(p, 0o777)
os.rmdir(p)
os.rmdir(p.parent/'test')


folder = r"D:\Data\raw_test_msync\F2020-09-10_16-15-39_Training2_57.d"
cmd = f"del /s /q {folder}"
subprocess.run(cmd, shell=True).returncode

cmd = rf"powershell.exe Remove-Item -Recurse -Force {folder}"
comp_proc = subprocess.run(cmd)
