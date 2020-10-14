from checksumdir import dirhash
import hashlib
from pathlib import Path


def file_check_sum(file_path, algo=hashlib.blake2b, chunksize=8192):
    """algo (hashlib function): E..g hashlib.blake2b, hashlib.md5."""
    with open(file_path, "rb") as f:
        file_hash = algo()
        chunk = f.read(chunksize)
        while chunk:
            file_hash.update(chunk)
            chunk = f.read(chunksize)
    return file_hash.hexdigest()


def folder_check_sum(folder_path, algo='sha256'):
    return dirhash(folder_path, algo)


def check_sum(path):
    path = Path(path).expanduser().resolve()
    if path.is_dir():
        return folder_check_sum(path)
    elif path.is_file():
        return file_check_sum(path)
    else:
        raise RuntimeError("How the fuck did we get here???")


def check_sums_aggree(path_a, path_b, **kwds):
    return check_sum(path_a, **kwds) == check_sum(path_b, **kwds)
