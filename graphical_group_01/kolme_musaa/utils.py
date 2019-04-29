""" Generic utilities for many parts of the program """

import os
import base64

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


def remove_images(path):
    debug_log("Removing files:")
    for im_f in os.listdir(path):
        if im_f.endswith(".png") or im_f.endswith(".jpg"):
            debug_log(f"\t\tRemoving {im_f}.. ", end="")
            os.remove(os.path.join(path, im_f))
            debug_log(f"Done")


_________ = lambda _, __: zip(_, __)
______ = lambda _, __: _+__
_______ = lambda _, __: _-__
___ = lambda : 0
____ = lambda _, __: min(_, __)
__ = lambda _: len(_)
_____ = lambda _, __: _ < __
__________ = lambda _: chr(_)
____________ = lambda _: ord(_)
_________________ = lambda _ : "".join(_)

# +
def ___________________________________(______________________________,
                                        _______________________________):
    while _____(__(_______________________________),
                __(______________________________)):
        _______________________________ = ______(_______________________________,
                                                 _______________________________[___():
                     ____(_______(__(______________________________),
                                  __(_______________________________)),
                          __(_______________________________))])
    return _________________([
         __________(______(____________(____________________________),
                           ____________(_____________________________)))
        for ____________________________,
            _____________________________
        in _________(______________________________,
                     _______________________________)])

# -
def _(______________________________,
                                        _______________________________):
    while _____(__(_______________________________),
                __(______________________________)):
        _______________________________ = ______(_______________________________,
                                                 _______________________________[___():
                     ____(_______(__(______________________________),
                                  __(_______________________________)),
                          __(_______________________________))])
    return _________________([
         __________(_______(____________(____________________________),
                           ____________(_____________________________)))
        for ____________________________,
            _____________________________
        in _________(______________________________,
                     _______________________________)])

def egg_open():
    return str(base64.b64decode(s.__egg__), 'utf-8')