import itertools
import os
import pathlib
from platform import system
import shutil
import subprocess



Path = lambda p: pathlib.Path(p).expanduser().resolve()


def robocopy(source, target, file_name_list=[], params='/it /r:10 /w:10 /E /Z'):
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


def cp_general(source, target):
    source = Path(source)
    target = Path(target)
    if source.is_file():
        shutil.copyfile(source, target)
    else:
        shutil.copytree(source, target)


def cp_windows(source, target):
    source = Path(source)
    target = Path(target)
    if source.is_dir():
        robocopy(source, target)
    else:
        if target.is_dir():
            robocopy(source.parent, target, [source.name])
        elif source.name == target.name:
            robocopy(source.parent, target.parent, [source.name])
        else:
            shutil.copyfile(source, target)


cp = cp_windows if system()=='Windows' else cp_general


def linuxcopy(source, target, file_name_list=[]):
    target = pathlib.Path(target)
    source = pathlib.Path(source)
    if file_name_list:
        for fn in file_name_list:
            shutil.copy2(str(source/fn), str(target/fn))
    else:
        shutil.copytree(str(source), str(target), dirs_exist_ok=True)
    return 1


def linuxmove(source, target, file_name_list):
    target = pathlib.Path(target)
    source = pathlib.Path(source)
    linuxcopy(source, target, file_name_list)
    rm(source) 
    return 1


# def cp(source, target, file_name_list=[]):
#     """Copy files from source to target.

#     Args:
#         source (str): Path to source.
#         target (str): Path to target.
#         file_name_list (list): list of strings
#     Returns:
#         int: code for success/failure."""
#     source = pathlib.Path(source).expanduser().resolve()
#     target = pathlib.Path(target).expanduser().resolve()
#     if source.is_file():
#         file_name_list.append(source.name)
#         source = source.parent 
#     if system()=='Windows':
#         return robocopy(source, target, file_name_list)
#     else:
#         return linuxcopy(source, target, file_name_list)


def mv(source, target, file_name_list=[]):
    if system()=='Windows':
        return robocopy(source, target, file_name_list, '/it /r:10 /w:10 /E /z /move')
    else:
        return linuxmove(source, target, file_name_list)


def version_folder(p):
    """Find the first free path for storing data by modifying the sample_set_no.

    Starting from: path/sample_set_no/acquired_name
    The procedure checks recursively if that path exists.
    If it does, append a free version number to sample_set_no., 
    e.g.              Y:/RES/2019-008/O191017-04
    replaced with:    Y:/RES/2019-008/O191017-04__v1

    Args:
        p (str): Path to check and modify.

    Return:
        pathlib.Path: corrected path.
    """
    i = 0
    q = pathlib.Path(p)
    while q.exists() and q.is_dir():
        i += 1
        q = p.parent/f"{p.name}__v{i}"
        # q = pathlib.Path(f"{p.parent}__v{i}")/p.name
    return q


def rm(p):
    """Removes folder or a file."""
    p = Path(p).expanduser().resolve()
    if system()=='Windows':
        cmd = rf"powershell.exe Remove-Item -Recurse -Force {p}"
        comp_proc = subprocess.run(cmd)
        if comp_proc.returncode != 0:
            print('Error.')
    else:
        if p.is_file():
            p.unlink()
        else:
            print('Trying to delete a folder.')
            shutil.rmtree(str(p), ignore_errors=True)


def no_handles_file(file):
    """Check if a file does not have handles.

    Surprisingly, this works in our case.
    """
    file = str(file)
    if os.path.exists(file):
        try:
            os.rename(file, file+"_")
            os.rename(file+"_", file)
        except PermissionError:
            return False
        except KeyboardInterrupt:
            raise KeyboardInterrupt("You interrupted me.")
        except SystemExit:
            raise SystemExit("System interrupted me.")
    return True


def no_handles(path):
    path = pathlib.Path(path)
    if path.is_file():
        paths = {path}
    else:
        paths = set(itertools.chain(path.glob("*"), path.glob("**/*")))
    return all(no_handles_file(file_path) for file_path in paths)
