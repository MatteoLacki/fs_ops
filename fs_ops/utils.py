import os
from random import choice
from string import ascii_letters, digits
import time


def random_folder_name(k=20):
    """Generate a random name for a folder.

    Args:
        k (int): The length of the out string.
    Returns:
        A folder names.
    """
    return ''.join(choice(ascii_letters+digits) for n in range(int(k)))


def age(file_path, unit='h'):
    """Get file age.

    Args:
        file_path (str): Path to file.
        unit (str): 's' for seconds, 'm' for minutes, 'h' for hours, 'd' for days."""
    age_in_s = time.time() - os.path.getctime(file_path)
    return {'s': age_in_s,
            'm': age_in_s/60,
            'h': age_in_s/3600,
            'd': age_in_s/86400 }[unit]