import tarfile
from os import path as op
from read_gutenberg import readmetadata

def check_local_data(directory=None):
    """
    Checks if local copy of the Gutenberg data is available in ./data

    Args: Directory where to check for the data. Defaults to ./data

    Returns: Boolean - does the file exist.
    """

    if directory is None:
        directory = op.join(op.dirname(__file__), "data")

    if not op.exists(directory):
        return False

    if not op.exists(op.join(directory, "rdf-files.tar.bz2")):
        return False

    return True


def download_gutenberg(dest=None):
    """
    Downloads the Gutenberg dataset (zipped).

    Args: Destination folder. Defaults to project data-folder.
    """

    # Default to data directory
    if dest is None:
        dest = op.join(op.dirname(__file__), "data")

    if check_local_data(dest):
        print("Data already exists in the directory. Continue, without download...")
        return

    # Create directory if not exist
    if not op.exists(dest):
        import os
        os.mkdir(dest)

    import urllib.request


    dest_fp = op.join(dest, "rdf-files.tar.bz2")
    print("Downloading the Gutenberg dataset to {}".format(dest_fp))

    url = "https://www.gutenberg.org/cache/epub/feeds/rdf-files.tar.bz2"
    print(urllib.request.urlretrieve(url, dest_fp)[1])
    
    return


def gutenberg_preprocess():
    """
    Reads titles from Gutenberg dataset to pickle.
    Note: Requires the data to reside in .data-folder.
    """
    if not check_local_data():
        raise FileNotFoundError("The dataset does not exist in .data." +
                                " Call download_gutenberg, or relocate file to .data")

    metadata = readmetadata()

    cleaned = dict()

    for k, v in metadata.items():
        
        if v["language"] is None:
            continue
        elif "en" not in v["language"]:
            continue
        
        if v["title"] is None:
            continue

        book_info = dict()
        book_info["title"] = v["title"]
        book_info["subjects"] = v["subjects"]
        cleaned[k] = book_info
    
    import pickle

    with open(op.join(op.dirname(__file__), "data", "titles.pickle"), "wb+") as w:
        pickle.dump(cleaned, w)
    

if __name__ == "__main__":
    download_gutenberg()
    gutenberg_preprocess()