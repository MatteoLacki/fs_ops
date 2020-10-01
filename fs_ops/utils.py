from random import choice
from string import ascii_letters, digits


def random_folder_name(k=20):
    """Generate a random name for a folder.

    Args:
        k (int): The length of the out string.
    Returns:
        A folder names.
    """
    return ''.join(choice(ascii_letters+digits) for n in range(int(k)))
