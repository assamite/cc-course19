""" Main file for step 1 """
import warnings
import os
import shutil
from PIL import Image
import numpy as np
import json

from kolme_muusaa.step_1 import assembler, classifier, downloader, producer
from kolme_muusaa import settings as s
from kolme_muusaa.utils import get_unique_save_path_name, debug_log, remove_images


__PRODUCE_ARTIFACTS_MODE__ = False


def execute(word_pairs:list, n_art:int, threshold=0.5, n_images_per_word:int=10):
    """Generates artifacts to be evaluated.

    New images are saved under __STEP_1_EVAL_DIR__.
     eval dir
    Parameters
    ----------
    word_pairs: list
        List of pairs of words.
    n_art: int
        Number of artifacts to be produced.

    """

    # Create the *eval* folder if it doesn't exist (with __init__.py)
    if not os.path.exists(s.__STEP_1_EVAL_DIR__):
        os.makedirs(s.__STEP_1_EVAL_DIR__)
        open(os.path.join(s.__STEP_1_EVAL_DIR__, "__init__.py")).close()

    # Clear content of eval dir
    if __PRODUCE_ARTIFACTS_MODE__ == False:
        if s.__DO_NOT_DELETE_DIR__ not in os.listdir(s.__STEP_1_EVAL_DIR__):
            remove_images(s.__STEP_1_EVAL_DIR__)

    # Delete obsolete temporary files
    if os.path.exists(s.__JSON_ART_DATA_STEP_1__):
        if s.__DO_NOT_DELETE_DIR__ not in os.listdir(s.__STEP_1_EVAL_DIR__):
            debug_log(f"Deleting temporary JSON_DICT {s.__JSON_ART_DATA_STEP_1__}.. ", end="")
            os.remove(s.__JSON_ART_DATA_STEP_1__)
            debug_log("Done")

            # Provide an empty dictionary
            with open(os.path.join(s.__JSON_ART_DATA_STEP_1__), "w") as json_file:
                json_file.write("{}")

    words = set([w for wp in word_pairs for w in wp])

    # Download images for words, skipping those where there are already enough images.
    for w in words:
        word_dir = os.path.join(s.__STEP_1_CACHE_DIR__, w)
        if os.path.exists(word_dir):
            dirlist = os.listdir(word_dir)

            if s.__SATURATED_DIR__ in dirlist:
                warnings.warn("No more images for '{w}' are available. Skipping..".format(w=w))
                continue

            if len(dirlist) < n_images_per_word:
                if not s.__DO_NOT_DELETE_DIR__ in dirlist:
                    remove_images(word_dir)

            else:
                debug_log(f"We have enough cached images for '{w}'. Skipping..")
                continue
        downloader.download(word=w, n_images=n_images_per_word)


    # Now learn the parameters for assembling the artifacts and judge them
    ready_list = list()

    while len(ready_list) < n_art:

        # Amount of artifacts left to produce
        artifacts_left = n_art - len(ready_list)
        debug_log(f"Should now produce {artifacts_left} artifact.. [Ready: {len(ready_list)}, Target: {n_art}]")
        debug_log(word_pairs)

        for i in range(artifacts_left):
            wp = word_pairs[i % len(word_pairs)]
            len_1 = len([im for im in os.listdir(os.path.join(s.__STEP_1_CACHE_DIR__, wp[0])) if (im.endswith(".png") or im.endswith(".jpg"))])
            len_2 = len([im for im in os.listdir(os.path.join(s.__STEP_1_CACHE_DIR__, wp[1])) if (im.endswith(".png") or im.endswith(".jpg"))])

            # Skip pair if there are not enough images
            if len_1 < 2:
                debug_log(f"Not enough images for {wp[0]}: {len_1}")
                continue

            if len_2 < 2:
                debug_log(f"Not enough images for {wp[1]}: {len_2}")
                continue



            assembling_parameters, image_path_1, image_path_2 = producer.produce_assembling_parameters(
                word_pair=wp
            )
            art_path = assembler.assemble_images_from_params(assembling_parameters, image_path_1, image_path_2, wp)
            art_name = os.path.basename(art_path)[:-4]

            # Save metadata
            json_data_dict = {}
            if os.path.exists(s.__JSON_ART_DATA_STEP_1__):
                with open(s.__JSON_ART_DATA_STEP_1__) as json_file:
                    json_data_dict = json.load(json_file)
            json_data_dict[art_name] = {
                "word_pair": wp,
                "base_image_1": os.path.basename(image_path_1)[:-4],
                "base_image_2": os.path.basename(image_path_2)[:-4],
                "assembling_parameters": assembling_parameters,
                "art_path": art_path
            }
            # Safe save
            with open(s.__JSON_ART_DATA_STEP_1__ + ".tmp", "w") as json_file:
                json.dump(json_data_dict, json_file)
            if os.path.exists(s.__JSON_ART_DATA_STEP_1__):
                os.remove(s.__JSON_ART_DATA_STEP_1__)
            os.rename(s.__JSON_ART_DATA_STEP_1__ + ".tmp", s.__JSON_ART_DATA_STEP_1__)

        debug_log(f"Generation completed using: {word_pairs}")

        if __PRODUCE_ARTIFACTS_MODE__ == True:
            debug_log("Produce mode is enabled. Not evaluating.")
            return {}

        # Evaluate the produced artifacts
        evals = classifier.evaluate_all()

        # Decide what to do based on evaluation
        with open(s.__JSON_ART_DATA_STEP_1__) as json_file:
            json_data_dict = json.load(json_file)
        for art_path, art_dict in evals:
            im_eval = art_dict["evaluation"]
            art_name = os.path.basename(art_path)[:-4]
            json_data_dict[art_name]["evaluation"] = im_eval
            if im_eval > threshold:
                debug_log(f"{art_name} good with: {im_eval} > {threshold}")
                ready_art_path = get_unique_save_path_name(s.__RESOURCES_STEP_1_READY__,
                                                             art_name,
                                                             "png")
                os.rename(art_path, ready_art_path)
                json_data_dict[art_name]["art_path"] = ready_art_path
                ready_list.append((ready_art_path, json_data_dict[art_name]))
            else:
                debug_log(f"{art_name} bad with {im_eval} <= {threshold}")
                discarded_art_path = get_unique_save_path_name(s.__RESOURCES_STEP_1_DISCARDED__,
                                                           art_name,
                                                           "png")
                os.rename(art_path, discarded_art_path)
                json_data_dict[art_name]["art_path"] = discarded_art_path

            # Update file so we have it in case of failure
            # Safe save
            with open(s.__JSON_ART_DATA_STEP_1__ + ".tmp", "w") as json_file:
                json.dump(json_data_dict, json_file)
            os.remove(s.__JSON_ART_DATA_STEP_1__)
            os.rename(s.__JSON_ART_DATA_STEP_1__ + ".tmp", s.__JSON_ART_DATA_STEP_1__)

        if len(ready_list) < n_art:
            debug_log(f"Not enough art. Only [{len(ready_list) }/{n_art}]. Getting more inspiration..")

    # >>> end of big while

    # Finally save art metadata
    json_file_name = get_unique_save_path_name(directory=s.__RESOURCES_DIR__,
                                        basename="art_data",
                                        extension="json")
    debug_log(f"Saving final JSON_DICT {json_file_name}..", end="")
    with open(json_file_name, "w") as json_file:
        json.dump(json_data_dict, json_file)
    debug_log("Done")

    # Delete non needed stuff
    if s.__DO_NOT_DELETE_DIR__ not in os.listdir(s.__STEP_1_EVAL_DIR__):
        debug_log(f"Deleting temporary JSON_DICT {s.__JSON_ART_DATA_STEP_1__}.. ", end="")
        os.remove(s.__JSON_ART_DATA_STEP_1__)
        debug_log("Done")

    return ready_list


if __name__ == "__main__":

    import sys
    sys.path.append(s.__GENERAL_PROJECT_ROOT__)

    import inputs

    word_list = []
    for i in range(1):
        word_list += inputs.get_input(use_samples=False)[1]
        print(f"Len of list: {len(word_list)}")
    print(f"Len of list: {len(word_list)}")
    word_list = set(word_list)
    print(f"Len of set: {len(word_list)}")
    print(word_list)
    __PRODUCE_ARTIFACTS_MODE__ = True
    execute(list(word_list), n_art=10000, threshold=-1)

    # execute([("adorable", "pet")], 5)


