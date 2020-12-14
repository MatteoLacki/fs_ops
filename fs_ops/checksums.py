import itertools
import hashlib
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

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
    from checksumdir import dirhash
    return dirhash(folder_path, algo)


def check_sum(path):
    path = Path(path).expanduser().resolve()
    if not path.exists():
        raise RuntimeError(f"Path missing: {path}")
    if path.is_dir():
        return folder_check_sum(path)
    elif path.is_file():
        return file_check_sum(path)
    else:
        raise RuntimeError("How the fuck did we get here???")


def check_sums_aggree(path_a, path_b, **kwds):
    return check_sum(path_a, **kwds) == check_sum(path_b, **kwds)


# This could be done much faster with async.
def all_source_hashes_aggree(source, target, server):
    if source.is_file():
        paths = {source}
    else:
        paths = set(itertools.chain(source.glob("*"),
                                    source.glob("**/*")))
    OK = True
    for file in paths:
        if file.is_file():
            target_file = str(file).replace(str(source), str(target))
            source_hash = check_sum(file)
            message = f"{file} has {source_hash}. "
            target_hash = server.get_check_sum(target_file)
            message += f"{target_file} has {target_hash}. "
            if source_hash == target_hash:
                message += "Hashes aggreed."
            else:
                message += "Hashes did no aggree. FUCK!"
            logger.info(message)
            OK &= source_hash == target_hash
            if not OK:
                break
    return OK
