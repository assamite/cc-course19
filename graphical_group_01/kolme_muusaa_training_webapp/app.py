"""Main application access point"""
import logging
import os
import time
import json

from shutil import copyfile

from flask import Flask, render_template, request, send_from_directory, Markup
import werkzeug
import werkzeug.exceptions
# import kolme_muusaa.settings as s


__WEB_APP_PATH__ = os.path.dirname(os.path.realpath(__file__))
# __WEB_APP_PATH__ = os.path.join(s.__PROJECT_ACCESS_INTERFACE__, "kolme_musaa_training_webapp")
__INSTANCE_PATH__ = os.path.join(__WEB_APP_PATH__, "instance")
__EVAL_DIR__ = os.path.join(__INSTANCE_PATH__, "eval_dir")
__DONE_DIR__ = os.path.join(__INSTANCE_PATH__, "done_dir")
__STATIC_DIR__ = os.path.join(__WEB_APP_PATH__, "static")
__LOG_PATH__ = os.path.join(__INSTANCE_PATH__, "log.txt")
__LOCK_PATH__ = os.path.join(__INSTANCE_PATH__, "lock")
__MAX_SLEEP_TIME__ = 5.0 # seconds
__SLEEP_TIME__ = 0.45 # seconds
__ART_DIR__ = "eval"
__PICTURES_BASE_URL__ = "http://kolmemuusaa.tryfcomet.com/"

# If eval is too large, make it smaller using the following command:
# find . -iname '*.png' -exec convert \{} -verbose -resize 256x256\> \{} \;
# From: https://guides.wp-bullet.com/batch-resize-images-using-linux-command-line-and-imagemagick/

def create_app():
    """Application factory function.

    This function generates the app instance and is useful to
    assure that only one instance exists.

    It also retrieves settings fro the configuration
    files to apply them to the application.

    Returns
    -------
    app instance

    """

    instance_path = __INSTANCE_PATH__

    # Creates the instance path if it doesn't exist
    if not os.path.exists(instance_path):
        os.makedirs(instance_path)

    app = Flask(__name__,
                instance_path=instance_path)

    # Logging utility setup
    # if app.config['ENV'] == 'development' or app.config['DEBUG'] == True:
    #     log_level = logging.DEBUG
    # else:
    #     log_level = logging.WARNING
    log_level = logging.DEBUG

    logging.basicConfig(
        format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        level=log_level,
        filename=__LOG_PATH__
    )

    logging.info("\t\t-------- Start --------")

    # @app.route('/eval/<path:filename>')
    @app.route('/json')
    def download_file():
        return send_from_directory(__INSTANCE_PATH__, "art_data.json")

    # Intercepts generic server errors and logs them
    @app.errorhandler(werkzeug.exceptions.HTTPException)
    def handle_errors(e):
        logging.error(str(e))
        return str(e), 500

    # Handles correct favicon
    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(os.path.join(app.root_path, 'static'),
                                   'favicon.ico', mimetype='image/vnd.microsoft.icon')

    # Root page
    @app.route('/', methods=['GET', 'POST'])
    def index():
        """Simple root page.

        The "@app.route('/')" decorator assigns this function
        to the '/' address, so that when you visit '/', a
        request is sent to the server, which will call this function.

        Once this function is called it returns an html page
        produced from the 'index.html' file.

        Returns
        -------
            html page
        """

        info_message = ""
        args = request.values

        logging.info(f"Received the following data: {args}")

        # Update evaluation on user evaluation
        try:
            if "art_name" in args and "evaluation" in args:
                get_lock()
                art_name = args["art_name"]
                evaluation = args["evaluation"]
                with open(os.path.join(__INSTANCE_PATH__, "art_data.json")) as json_file:
                    json_dict = json.load(json_file)
                if art_name in json_dict:
                    current_art_dict = json_dict[art_name]
                    if "evaluation" not in current_art_dict:
                        current_art_dict["evaluation"] = float(evaluation)
                        if "star" in args and args["star"] in ['True' or 'on']:
                            logging.info(f"Image {art_name} starred!")
                            current_art_dict["star"] = True

                        # Safe save
                        with open(os.path.join(__INSTANCE_PATH__, "art_data.json.tmp"), "w") as json_file:
                            json.dump(json_dict, json_file)
                        os.rename(os.path.join(__INSTANCE_PATH__, "art_data.json.tmp"),
                                  os.path.join(__INSTANCE_PATH__, "art_data.json"))

                        info_message = f"Your rating for {art_name} was saved successfully!"
                        logging.info(info_message)
                    else:
                        info_message = f"{art_name} have already been rated in the while.. Try to be faster."
                        logging.info(info_message)
                else:
                    info_message = f"Something went wrong while saving your rating.. Keep trying."
                    logging.error(info_message)
                    logging.error(f"Expected art {art_name} was not found in JSON dictionary!")
                release_lock()
            else:
                logging.info(f"Not enough args to evaluate: {args}.")
        except Exception as e:
            release_lock()
            info_message += " Sorry, something went wrong while saving your evaluation.."
            logging.error(e)


        # Retrieve an image to evaluate
        current_art_name = None

        get_lock()
        try:
            with open(os.path.join(__INSTANCE_PATH__, "art_data.json")) as json_file:
                json_dict = json.load(json_file)
                for art_name in json_dict.keys():
                    if "evaluation" in json_dict[art_name]:
                        logging.debug(f"Evaluation found in art: {art_name}")
                    else:
                        image_lock_path = os.path.join(__INSTANCE_PATH__, art_name + ".lock")
                        if not os.path.exists(image_lock_path):
                            logging.debug(f"Art '{art_name}' is available. Locking..")
                            write_lock(image_lock_path)
                            current_art_name = art_name
                            break
                        else:
                            with open(image_lock_path) as image_lock:
                                lock_time = image_lock.read()
                                try:
                                    if time.time() - float(lock_time) > 60 * 5:
                                        logging.debug(f"Art '{art_name}' has an expired lock, so it is available."
                                                      f" Locking..")
                                        release_lock(image_lock_path)
                                        write_lock(image_lock_path)
                                        current_art_name = art_name
                                        break
                                    else:
                                        logging.debug(f"Art '{art_name}' has a valid lock, so it is unavailable.")
                                except ValueError as e:
                                    logging.warning(str(e) + f"Lock {image_lock_path} string value: '{lock_time}'")
                                    logging.debug(f"Art '{art_name}' has an invalid lock, so it is available."
                                                  f" Locking..")
                                    release_lock(image_lock_path)
                                    write_lock(image_lock_path)
                                    current_art_name = art_name
                                    break

            release_lock()
        except Exception as e:
            release_lock()
            info_message += " Sorry, something went wrong while retrieving an image.."
            logging.error(e)
            current_art_name = None

        # Finally render page
        if current_art_name == None:
            return render_template('index.html',
                                   disable_eval=True,
                                   info_message=info_message,
                                   art_name=Markup("No available images at this time.<br>┐(︶▽︶)┌"))

        else:
            logging.info(f"Serving {current_art_name}..")
            return render_template('index.html',
                               info_message=info_message,
                               art_name=current_art_name,
                               image_path=__PICTURES_BASE_URL__ + f"{current_art_name}.png")

    return app


def write_lock(p=None):
    if p == None:
        p = __LOCK_PATH__
    with open(p, 'w') as lock:
        lock.write(str(time.time()))

def release_lock(p=None):
    if p == None:
        p = __LOCK_PATH__
    os.remove(p)


def get_lock():
    while True:
        if not os.path.exists(__LOCK_PATH__):
            write_lock()
            return
        else:
            with open(__LOCK_PATH__) as lock:
                lock_time = lock.read()
            try:
                if time.time() - float(lock_time) > 5.0:
                    release_lock()
                    write_lock()
                    return
                else:
                    time.sleep(__SLEEP_TIME__)
            except ValueError as e:
                logging.warning(str(e) + f"Lock string value: '{lock_time}'")
                release_lock()
                write_lock()
