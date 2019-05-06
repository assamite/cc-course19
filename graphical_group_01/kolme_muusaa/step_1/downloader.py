""" Downloads the required images and saves them in cache """

import urllib3
import json
import os
import certifi
from kolme_muusaa.utils import _, egg_open, debug_log, get_unique_save_path_name
import kolme_muusaa.settings as s
import warnings
import time


def download(word, n_images=100):
    """Retrieves the required images.

    If downloaded are saved in cache, otherwise they're just retrieved from there.

    Parameters
    ----------
    word

    Returns
    -------
    bool:
        Only says if the process terminated correctly.

    """

    # Fields for pixbay from https://pixabay.com/api/docs/#api_search_images

    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())

    for i in range(5):
        fields = {
            "key": _(s.__secret__, egg_open()),
            "q": word,
            "image_type": "photo",
            "safesearch": "true",
            "per_page": max(3, min(200, n_images + i))
        }

        debug_log(f"fields for request:\n{ {key: fields[key] for key in fields.keys() if key != 'key'} }")

        r = http.request(method='GET',
                         url='https://pixabay.com/api/',
                         fields=fields)

        debug_log(f"Response data: {r.data}")

        if "ERROR" in str(r.data, 'utf-8'):
            continue
        else:
            break

    try:
        data = json.loads(r.data.decode('utf-8'))
    except json.decoder.JSONDecodeError as e:
        warnings.warn("Cannot download '{word}'. Bad response: {response}".format(
            word=word,
            response=str(r.data, 'utf-8')
        ))
        return False

    image_urls = [item["largeImageURL"] for item in data["hits"]]
    image_ids = [item["id"] for item in data["hits"]]


    debug_log(f"Image urls: {image_urls}")
    debug_log(f"Len Image urls: {len(image_urls)}")

    save_dir = os.path.join(s.__STEP_1_CACHE_DIR__, word)
    os.makedirs(save_dir, exist_ok=True)

    if len(image_urls) < n_images:
        warnings.warn("Not enough images for {word}. Only {len_image_urls} instead of {n_images}.".format(
            word=word,
            len_image_urls=len(image_urls),
            n_images=n_images
        ))
        open(os.path.join(save_dir, "SATURATED"), 'w').close()
        open(os.path.join(save_dir, "DO_NOT_DELETE"), 'w').close()

    image_paths = [get_unique_save_path_name(save_dir,
                                             im_id,
                                             im_url.split('.')[-1]) # Get the right image extension
                   for im_id, im_url in zip(image_ids, image_urls)]

    debug_log(f"Image paths: {image_paths}")

    for i, im_url, im_path in zip(range(len(image_urls)), image_urls, image_paths):
        debug_log(f"Downloading '{word}' image [{i+1}/{len(image_urls)}]: {im_url}")
        save_file(im_url, im_path, http)
        debug_log(f"Done! Saved as {im_path}")

    return True


def save_file(file_url, file_path, pool_manager=None):
    """
    References: https://stackoverflow.com/a/17285906/2219492

    Parameters
    ----------
    file_url
    file_path
    pool_manager

    Returns
    -------

    """
    chunk_size = 2**16

    if pool_manager is None:
        pool_manager = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())

    r = pool_manager.request('GET', file_url, preload_content=False)

    last_time = time.time()
    i = 0

    with open(file_path, 'wb') as out:
        while True:
            data = r.read(chunk_size)
            if not data:
                break
            out.write(data)
            i += 1
            if time.time() - last_time > 5:
                print(f"Downloaded {i * chunk_size}bytes.. Hold on.. ")
                last_time = time.time()

    r.release_conn()


if __name__ == '__main__':
    print("Testing downloader...")

    download("compassionate", 15)
