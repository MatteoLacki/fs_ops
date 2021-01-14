from pathlib import Path
import itertools


def min_age(source, **kwds):
    if source.is_file():
        paths = {source}
    else:
        paths = set(itertools.chain(source.glob("*"),
                                    source.glob("**/*")))
    return min(age(path, **kwds) for path in paths)
