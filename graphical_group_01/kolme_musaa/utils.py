""" Generic utilities for many parts of the program """

import os

import kolme_musaa.settings as s

def debug_log(*args, **kwargs):
    if s.__DEBUG_MODE__ == True:
        print(*args, **kwargs)

def get_unique_save_path_name(directory, basename, extension):
    """Generates a unique filename under the given directory.

    Parameters
    ----------
    directory: str
        path where the file is intended to be saved

    basename: str
        base part of the name to which a suffix can be added

    extension: str
        type of file extension

    Returns
    -------
    str:
        unique pathname including directory and unique filename

    """
    i = 0
    tentative_path = os.path.join(directory, f"{basename}.{extension}")
    if not os.path.exists(tentative_path):
        return tentative_path

    while True:
        i += 1
        tentative_path = os.path.join(directory, f"{basename}_{i}.{extension}")
        if not os.path.exists(tentative_path):
            return tentative_path