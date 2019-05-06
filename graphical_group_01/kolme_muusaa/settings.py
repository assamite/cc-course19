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
__STEP_1_CACHE_DIR__ = os.path.join(__STEP_1_DIR__, 'cache')
__STEP_1_DATASET_DIR__ = os.path.join(__STEP_1_DIR__, 'dataset')

__RESOURCES_DIR__ = os.path.join(__PROJECT_ACCESS_INTERFACE__, "resources")
__RESOURCES_STEP_1_READY__ = os.path.join(__RESOURCES_DIR__, "step_1_ready")
__RESOURCES_STEP_1_DISCARDED__ = os.path.join(__RESOURCES_DIR__, "step_1_discarded")

# Image definitions
__IMAGE_SIDE_SIZE_NN__ = 128
__IMAGE_SIDE_SIZE__ = 512
__COLOR_CHANNELS__ = 3

__secret__ = '~\x9b\x98\x9c\x9a§\xa0X\x9a\x9c£«Ô\x82ÖÈÑËÛ¡^\x81:\x97\x9e¨¦\xa0\x9a\x82Æ\x9c\x9a¥'
__egg__ = b"TWllbGVuaSBtaW51biB0ZWtldmksIAphaXZvbmkgYWphdHRlbGV2aSAKbMOkaHRlw6R" \
          b"uaSBsYXVsYW1haGFuLCAKc2FhJ2FuaSBzYW5lbGVtYWhhbiwgCnN1a3V2aXJ0dMOkIH" \
          b"N1b2x0YW1haGFuLCAKbGFqaXZpcnR0w6QgbGF1bGFtYWhhbi4gClNhbmF0IHN1dXNzY" \
          b"W5pIHN1bGF2YXQsIApwdWhlJ2V0IHB1dG9lbGV2YXQsIApraWVsZWxsZW5pIGtlcmtp" \
          b"w6R2w6R0LCAKaGFtcGFoaWxsZW5pIGhham9vdmF0LiAKVmVsaSBrdWx0YSwgdmVpa2t" \
          b"vc2VuaSwgCmthdW5pcyBrYXN2aW5rdW1wcGFsaW5pISAKTMOkaGUgbnl0IGthbnNzYS" \
          b"BsYXVsYW1haGFuLCAKc2FhIGtlcmEgc2FuZWxlbWFoYW4gCnlodGVoZW4geWh5dHR5w" \
          b"6RtbWUsIAprYWh0YSdhbHRhIGvDpHl0ecOkbW1lISAKSGFydm9pbiB5aHRlaGVuIHlo" \
          b"eW1tZSwgCnNhYW1tZSB0b2luZW4gdG9pc2loaW1tZSAKbsOkaWxsw6QgcmF1a29pbGx" \
          b"hIHJham9pbGxhLCAKcG9sb2lzaWxsYSBQb2hqYW4gbWFpbGxhLg=="

__SATURATED_DIR__ = "SATURATED"
__DO_NOT_DELETE_DIR__ = "DO_NOT_DELETE"
__JSON_ART_DATA_STEP_1__ = os.path.join(__STEP_1_EVAL_DIR__, "art_data.json")