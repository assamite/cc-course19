from __future__ import division, print_function

import os
import cv2
from .style_help.utils import preserve_colors_np
from .style_help.utils import get_img, resize_to, center_crop
import time
from .style_help.wct import WCT


#GLOBAL VARS
CHECKPOINTS = ['style_help/models/relu5_1', 'style_help/models/relu4_1', 'style_help/models/relu3_1', 'style_help/models/relu2_1', 'style_help/models/relu1_1']
                                                #List of checkpoint directories
RELU_TARGETS = ['relu5_1', 'relu4_1', 'relu3_1', 'relu2_1', 'relu1_1']
                                                #List of reluX_1 layers, corresponding to --checkpoints
VGG_PATH = 'style_help/models/vgg_normalised.t7' #Path to vgg_normalised.t7
CONTENT_PATH = '../images/content'              #Content image or folder of images
STYLE_PATH = '../images/style'                  #Style image or folder of images
OUT_PATH = 'images/output'                      #Output folder path
OUTPUT_PATH = 'images/output.jpg'
KEEP_COLORS = False                             #Preserve the colors of the style image
DEVICE = '/cpu:0'                               #Device to perform compute on, e.g. /gpu:0 I only have one GPU so loading this one in cpu.
STYLE_SIZE = 0                                  #Resize style image to this size before cropping, default 512
CROP_SIZE = 0                                   #Crop square size, default 256
CONTENT_SIZE = 0                                #Resize short side of content image to this
PASSES = 1                                      # of stylization passes per content image
ALPHA = 1                                       #Alpha blend value
CONCAT = False                                  #Concatenate style image and stylized output
ADAIN = False                                   #Use AdaIN instead of WCT
SWAP5 = False                                   #Swap style on layer relu5_1
SS_ALPHA = 0.6                                  #Style swap alpha blend
SS_PATH_SIZE = 3                                #Style swap patch size
SS_STRIDE = 1                                   #Style swap stride
PATH = os.path.dirname(os.path.realpath(__file__))

print (f'Loading StyleTransfer module on {DEVICE}.........')
 # Load the WCT model

checkpoints = []
for i in CHECKPOINTS:
    i = os.path.join(PATH,i)
    checkpoints.append(i)

wct_model = WCT(checkpoints=checkpoints,
                                relu_targets=RELU_TARGETS,
                                vgg_path=os.path.join(PATH, VGG_PATH),
                                device=DEVICE,
                                ss_patch_size=SS_PATH_SIZE,
                                ss_stride=SS_STRIDE)

print ('StyleTransfer module loaded!')


def stylize(alpha=ALPHA, content_path = CONTENT_PATH, style_path = STYLE_PATH, output_path = OUTPUT_PATH, style_size=STYLE_SIZE,
             crop_size=CROP_SIZE, keep_colors=KEEP_COLORS, passes=PASSES,swap5=SWAP5, concat=CONCAT):

    print('Starting the style transfer process...')
    start = time.time()

    content_img = get_img(content_path)
    if CONTENT_SIZE > 0:
        content_img = resize_to(content_img, CONTENT_SIZE)

    style_img = get_img(style_path)

    if style_size > 0:
        style_img = resize_to(style_img, style_size)
    if crop_size > 0:
        style_img = center_crop(style_img, crop_size)
    if keep_colors:
        style_img = preserve_colors_np(style_img, content_img)

    # Run the frame through the style network
    stylized_rgb = wct_model.predict(content_img, style_img, alpha, swap5, SS_ALPHA, ADAIN)
    if passes > 1:
        for _ in range(passes - 1):
            stylized_rgb = wct_model.predict(stylized_rgb, style_img, alpha, swap5, SS_ALPHA, ADAIN)

    cv2.imwrite(output_path, stylized_rgb)

    print("Finished style transfer in {}s".format(time.time() - start))
