""" Downloads the required images and saves them in cache """

import urllib3
import json
import os
import certifi
from kolme_musaa.utils import _, egg_open, debug_log, get_unique_save_path_name
import kolme_musaa.settings as s


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

    fields = {
        "key": _(s.__secret__, egg_open()),
        "q": word,
        "image_type": "photo",
        "safesearch": "true",
        "per_page": max(3, min(200, n_images))
    }

    debug_log(f"fields for request:\n{ {key: fields[key] for key in fields.keys() if key != 'key'} }")

    r = http.request(method='GET',
                     url='https://pixabay.com/api/',
                     fields=fields)

    debug_log(r.data)

    data = json.loads(r.data.decode('utf-8'))
    image_urls = [item["largeImageURL"] for item in data["hits"]]
    image_ids = [item["id"] for item in data["hits"]]

    debug_log(f"Image urls: {image_urls}")
    debug_log(f"Len Image urls: {len(image_urls)}")

    save_dir = os.path.join(s.__STEP_1_CACHE_DIR__, word)
    os.makedirs(save_dir, exist_ok=True)

    image_paths = [get_unique_save_path_name(save_dir,
                                             im_id,
                                             im_url.split('.')[-1]) # Get the right image extension
                   for im_id, im_url in zip(image_ids, image_urls)]

    debug_log(f"Image paths: {image_paths}")

    for i, im_url, im_path in zip(range(len(image_urls)), image_urls, image_paths):
        debug_log(f"Downloading *{word}* image [{i+1}/{len(image_urls)}]: {im_url}")
        save_image(im_url, im_path, http)
        debug_log(f"Done! Saved as {im_path}")

    return True


def save_image(image_url, image_path, pool_manager):
    """
    References: https://stackoverflow.com/a/17285906/2219492

    Parameters
    ----------
    image_url
    image_path
    pool_manager

    Returns
    -------

    """
    chunk_size = 2**16

    r = pool_manager.request('GET', image_url, preload_content=False)



    with open(image_path, 'wb') as out:
        while True:
            data = r.read(chunk_size)
            if not data:
                break
            out.write(data)

    r.release_conn()


if __name__ == '__main__':
    print("Testing downloader...")

    download("pet", 5)
