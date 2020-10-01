import shutil
import subprocess
import pathlib

from platform import system


def robocopy(source, target, file_name_list=[], params='/it /r:10 /w:10 /E /z'):
    """Copy files.
    
    /is copies same files:
    /it copies tweaked files.
    /mt16 multithreading with 16 threads
    /E include subdirectories.
    /r:10 repeat 10 times
    /w:10 wait 10" to reestablish connection
    /Z: Copy files in restartable mode (survive network glitch).    
    /COPY:DT /DCOPY:T preserve the date and time stamps.
    /COPY:DAT is default.
    check on: https://docs.microsoft.com/de-de/windows-server/administration/windows-commands/robocopy
    """
    cmd = f"robocopy {str(source)} {str(target)} {' '.join(str(fn) for fn in file_name_list)} {params}"
    return subprocess.run(cmd.split()).returncode


def linuxcopy(source, target, file_name_list=[]):
    target = pathlib.Path(target)
    source = pathlib.Path(source)
    if file_name_list:
        for fn in file_name_list:
            shutil.copy2(str(source/fn), str(target/fn))
    else:
        if source.is_dir():
            # like cp -r /home/test/A /home/test/B
            # must result in /home/test/B/A 
            target = target/source.name
        shutil.copytree(str(source), str(target), dirs_exist_ok=True)
    return 1


def linuxmove(source, target, file_name_list):
    target = pathlib.Path(target)
    source = pathlib.Path(source)
    if file_name_list:
        for fn in file_name_list:
            shutil.move(str(source/fn), str(target/fn))
    else:
        if source.is_dir():
            # like cp -r /home/test/A /home/test/B
            # must result in /home/test/B/A 
            target = target/source.name
            shutil.copytree(str(source), str(target))
            shutil.rmtree(str(source), str(target))
        else:
            target.mkdir(parents=True, exist_ok=True)
            shutil.move(str(source), str(target/source.name))   
    return 1


def cp(source, target, file_name_list=[]):
    """Copy files from source to target.

    Args:
        source (str): Path to source.
        target (str): Path to target.
        file_name_list (list): list of strings
    Returns:
        int: code for success/failure."""
    source = pathlib.Path(source).expanduser().resolve()
    target = pathlib.Path(target).expanduser().resolve()
    if source.is_file():
        file_name_list.append(source.name)
        source = source.parent 
    if system()=='Windows':
        return robocopy(source, target, file_name_list)
    else:
        return linuxcopy(source, target, file_name_list)


def mv(source, target, file_name_list=[]):
    if system()=='Windows':
        return robocopy(source, target, file_name_list, '/it /r:10 /w:10 /E /z /move')
    else:
        return linuxmove(source, target, file_name_list)


def version_folder(p):
    """Find the first free path for storing data by modifying the sample_set_no.

    Starting from: path/sample_set_no/acquired_name
    The procedure checks recursively if that path exists.
    If it does, append a free version number to sample_set_no.

    Args:
        p (str): Path to check and modify.
    """
    i = 0
    q = Path(p)
    while q.exists() and q.is_dir():
        i += 1
        q = p.parent/f"{p.name}__v{i}"
        # q = Path(f"{p.parent}__v{i}")/p.name
    return q


def rm(pth):
    """Removes recursively the folder and everything below in the file tree."""
    pth = Path(pth)
    for child in pth.glob('*'):
        if child.is_file():
            child.unlink()
        else:
            rm_tree(child)
    pth.rmdir()