""" General settings for the application """

import os

__DEBUG_MODE__ = True

# Project directories
__KOLME_MUUSAA_PROJECT_ROOT__ = os.path.dirname(os.path.realpath(__file__))
__PROJECT_ACCESS_INTERFACE__ = os.path.dirname(__KOLME_MUUSAA_PROJECT_ROOT__)
__GENERAL_PROJECT_ROOT__ = os.path.dirname(__PROJECT_ACCESS_INTERFACE__)

__STEP_1_DIR__ = os.path.join(__KOLME_MUUSAA_PROJECT_ROOT__, "step_1")
__STEP_2_DIR__ = os.path.join(__KOLME_MUUSAA_PROJECT_ROOT__, "step_2")
__STEP_3_DIR__ = os.path.join(__KOLME_MUUSAA_PROJECT_ROOT__, "step_3")

__STEP_1_EVAL_DIR__ = os.path.join(__STEP_1_DIR__, "eval_dir")

__RESOURCES_DIR__ = os.path.join(__PROJECT_ACCESS_INTERFACE__, "resources")
__RESOURCES_STEP_1_READY__ = os.path.join(__RESOURCES_DIR__, "step_1_ready")

# Image definitions
__IMAGE_WIDTH__ = 500
__IMAGE_HEIGHT__ = 500
__COLOR_CHANNELS__ = 3