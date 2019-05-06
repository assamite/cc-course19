""" Evaluates the quality of an assembling artwork """

import os

import numpy as np
import tensorflow as tf
from PIL import Image
from tensorflow import keras

import kolme_muusaa.settings as s
from kolme_muusaa.utils import debug_log

__MODEL_PATH__ = os.path.join(s.__RESOURCES_DIR__, "models", "classifier.data")


def get_evaluation_model():
    model = create_model()
    model.load_weights(__MODEL_PATH__)
    return model


def evaluate_all(model=None):
    evals = list()
    eval_dir = s.__STEP_1_EVAL_DIR__

    for im_path in os.listdir(eval_dir):
        if not (im_path.endswith(".png") or im_path.endswith(".jpg")):
            print(f"Skipping evaluation of {im_path} because it's not a recognised image format.")
            continue

        image_path = os.path.join(eval_dir, im_path)

        evals.append((image_path, {'evaluation': evaluate(image_path, model=model)}))

    return evals


def evaluate(image_path, threshold=0.5, model=None):
    """Evaluates the goodness of an image artifact by its scaled average.

    Parameters
    ----------
    image_path: str
        path to an image that is supported by PIL

    Returns
    -------
    float:
        value grade for the artifact

    """

    if model == None:
        try:
            # Restore the weights
            model = create_model()
            model.load_weights(__MODEL_PATH__)
        except Exception as e:
            debug_log("Error: ", e)
            debug_log(f"Classifier {__MODEL_PATH__} not found or invalid. Using randomness..")
            return np.random.rand()

    image = Image.open(image_path).resize((s.__IMAGE_SIDE_SIZE_NN__, s.__IMAGE_SIDE_SIZE_NN__)).convert('RGB')

    # Evaluation
    image_matrix = np.array(image, dtype=np.float) / 255.0
    image_matrix = (np.expand_dims(image_matrix, 0))

    predictions_single = model.predict(image_matrix)[0][0]  # Probability of good!

    return float(predictions_single)


def create_model():
    # Part of the code in this file comes from:
    # https://www.tensorflow.org/tutorials/keras/basic_classification
    # https://adventuresinmachinelearning.com/keras-tutorial-cnn-11-lines/

    num_classes = 2
    input_shape = (s.__IMAGE_SIDE_SIZE_NN__, s.__IMAGE_SIDE_SIZE_NN__, 3)

    model = keras.Sequential([

        # Layer 1
        keras.layers.Conv2D(
            filters=32,
            kernel_size=(5, 5),
            strides=(1, 1),
            activation='relu',
            input_shape=input_shape
        ),

        # Layer 2
        keras.layers.MaxPooling2D(
            pool_size=(2, 2),
            strides=(2, 2)
        ),

        # Layer 3
        keras.layers.Conv2D(
            filters=64,
            kernel_size=(5, 5),
            activation='relu'
        ),

        # Layer 4
        keras.layers.MaxPooling2D(
            pool_size=(2, 2)
        ),

        # Layer 5
        keras.layers.Flatten(),

        # Layer 6
        keras.layers.Dense(
            units=1000,
            activation='relu'
        ),

        # Layer 7
        keras.layers.Dense(
            1,
            activation='sigmoid'
        )
    ])

    # Compile the model
    model.compile(optimizer='adam',
                  loss='binary_crossentropy',
                  metrics=['accuracy'])

    return model


def train_classifier(n_epochs):
    """Before running this function, use prepare_dataset and separate_train_validation"""

    data_train_path = os.path.join(s.__STEP_1_DATASET_DIR__, "train")
    data_validation_path = os.path.join(s.__STEP_1_DATASET_DIR__, "validation")

    train_datagen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1. / 255, horizontal_flip=True)
    test_datagen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1. / 255, horizontal_flip=True)

    train_generator = train_datagen.flow_from_directory(
        directory=data_train_path,
        target_size=(s.__IMAGE_SIDE_SIZE_NN__, s.__IMAGE_SIDE_SIZE_NN__),
        batch_size=16,
        class_mode='binary')

    print("Class indices:", train_generator.class_indices)

    validation_generator = test_datagen.flow_from_directory(
        directory=data_validation_path,
        target_size=(s.__IMAGE_SIDE_SIZE_NN__, s.__IMAGE_SIDE_SIZE_NN__),
        batch_size=16,
        class_mode='binary')

    for image_batch, label_batch in train_generator:
        print("Image batch shape: ", image_batch.shape)
        print("Label batch shape: ", label_batch.shape)
        break

    # Checkpoint path
    checkpoint_dir = os.path.join(s.__RESOURCES_DIR__, "checkpoints")
    os.makedirs(checkpoint_dir, exist_ok=True)
    checkpoint_path = os.path.join(checkpoint_dir, "classifier.ckpt")

    # Model path
    os.makedirs(__MODEL_PATH__, exist_ok=True)
    print("Model path:", __MODEL_PATH__)

    # Create checkpoint callback
    checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(checkpoint_path,
                                                             save_weights_only=True,
                                                             verbose=1)

    model = create_model()

    model.fit_generator(
        train_generator,
        steps_per_epoch=2000,
        epochs=n_epochs,
        validation_data=validation_generator,
        validation_steps=800,
        callbacks=[checkpoint_callback]
    )

    # Saving model weights
    model.save_weights(__MODEL_PATH__)
    print("Model saved at: " + __MODEL_PATH__)

    test_loss, test_acc = model.evaluate(validation_generator)

    print('Test accuracy:', test_acc)

    for image_batch, label_batch in validation_generator:
        print("Image batch shape: ", image_batch.shape)
        print("Label batch shape: ", label_batch.shape)
        break
    img = image_batch[0]

    # Add the image to a batch where it's the only member. Keras always needs lists.
    print("Single test image shape: ", img.shape)

    if len(img.shape) < 4:
        img = (np.expand_dims(img, 0))
        print("Single test image shape (updated): ", img.shape)

    predictions_single = model.predict(img)
    print("Single test image prediction: ", predictions_single)

    print("Resetting model to test save..")
    model = None

    # Restore the weights
    model = create_model()
    model.load_weights(__MODEL_PATH__)

    test_loss, test_acc = model.evaluate(validation_generator)

    print('Test accuracy:', test_acc, "(Reloaded model)")


def prepare_dataset():
    """
    Ensures that a dataset is ready and available. Later use separate_train_validation.
    """
    import json
    import urllib3
    import certifi
    import shutil
    from kolme_muusaa.step_1 import downloader

    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())

    aggregate_dir = os.path.join(s.__STEP_1_DIR__, "all_data")
    star_dir = os.path.join(s.__RESOURCES_DIR__, "stars")
    json_dict_path = os.path.join(s.__STEP_1_DATASET_DIR__, "art_data.json")
    good_dir = os.path.join(s.__STEP_1_DATASET_DIR__, "good")
    bad_dir = os.path.join(s.__STEP_1_DATASET_DIR__, "bad")
    print("Warning, if 'star' dir already exist some results can be lost!")

    os.makedirs(aggregate_dir, exist_ok=True)
    os.makedirs(star_dir, exist_ok=True)
    os.makedirs(good_dir, exist_ok=True)
    os.makedirs(bad_dir, exist_ok=True)

    with open(json_dict_path) as json_file:
        json_dict: dict = json.load(json_file)

    len_dict = len(json_dict)

    for i, art_name in enumerate(json_dict.keys()):
        current_art_dict: dict = json_dict[art_name]
        art_path = os.path.join(aggregate_dir, art_name + ".png")
        art_url = "http://kolmemuusaa.tryfcomet.com/" + art_name + ".png"

        num = i + 1
        print(f"[{num}/{len_dict}]", end=" - ")

        if 'evaluation' in current_art_dict:

            if not os.path.exists(art_path):
                print("Not found. Downloading..", end=" ")
                downloader.save_file(file_url=art_url, file_path=art_path, pool_manager=http)
                print("Done!", end=" - ")

            if current_art_dict['evaluation'] > 0.5:

                if 'star' in current_art_dict and current_art_dict['star'] == True:
                    shutil.copyfile(os.path.join(aggregate_dir, art_name + ".png"),
                                    os.path.join(star_dir, art_name + ".png"))
                    print("<Star>", end=" ")

                os.rename(os.path.join(aggregate_dir, art_name + ".png"),
                          os.path.join(good_dir, art_name + ".png"))
                print(f"'{art_name}' moved to 'good'")
            else:
                os.rename(os.path.join(aggregate_dir, art_name + ".png"),
                          os.path.join(bad_dir, art_name + ".png"))
                print(f"'{art_name}' moved to 'bad'")
        else:
            print(f"'{art_name}' skipped")


def separate_train_validation(validation_split: float = 0.2):
    """
    If you prepared a dataset with prepare_dataset, run this to split training and validation sets.

    Parameters
    ----------
    validation_split

    Returns
    -------

    """
    for class_name in ["good", "bad"]:
        if not os.path.isdir(os.path.join(s.__STEP_1_DATASET_DIR__, class_name)):
            continue

        dir_path = os.path.join(s.__STEP_1_DATASET_DIR__, class_name)

        print(dir_path)

        dir_len = len(os.listdir(dir_path))
        validation_limit = int(dir_len * validation_split)
        class_validation_path = os.path.join(s.__STEP_1_DATASET_DIR__, "validation", class_name)
        class_train_path = os.path.join(s.__STEP_1_DATASET_DIR__, "train", class_name)

        os.makedirs(class_validation_path, exist_ok=True)
        os.makedirs(class_train_path, exist_ok=True)

        for i, image_name in enumerate(os.listdir(dir_path)):

            print(f"[{i + 1}/{dir_len}] ", end=" - ")

            if i < validation_limit:
                os.rename(
                    os.path.join(dir_path, image_name),
                    os.path.join(class_validation_path, image_name)
                )
                print(f"'{image_name}' moved to validation/{class_name}")
            else:
                os.rename(
                    os.path.join(dir_path, image_name),
                    os.path.join(class_train_path, image_name)
                )
                print(f"'{image_name}' moved to validation/{class_name}")


def download_dataset():
    debug_log("Downloading dataset..")
    import zipfile  # No need to import otherwise
    from kolme_muusaa.step_1 import downloader
    model_zip_path = os.path.join(s.__STEP_1_DIR__, "dataset_kolme_musaa.zip")
    downloader.save_file(file_url="https://archive.org/download/all_data_kolme_muusaa/dataset_kolme_musaa.zip",
                         file_path=model_zip_path)

    debug_log("Dataset downloaded! Extracting zip file..")
    with zipfile.ZipFile(model_zip_path, "r") as zip_archive:
        zip_archive.extractall(s.__STEP_1_DIR__)
    debug_log("Done!")


if __name__ == "__main__":
    # prepare_dataset()
    # separate_train_validation()
    if not os.path.exists(s.__STEP_1_DATASET_DIR__):
        debug_log("Dataset not found.", end=" ")
        download_dataset()
    train_classifier(n_epochs=100)
