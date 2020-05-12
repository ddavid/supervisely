# coding: utf-8

import os
import time

import cv2
import numpy as np
from collections import defaultdict
from PIL import Image, ImageDraw, ImageFont

import supervisely_lib as sly
from supervisely_lib import fs
from supervisely_lib import TaskPaths
from supervisely_lib.io.json import load_json_file

# Watermark text constants
FONT_PATH = '/workdir/fonts/VeraMono.ttf'
FONT_SIZE = 16

# Don't change this one
FSOCO_IMPORT_BORDER_THICKNESS = 140
FSOCO_IMPORT_LOGO_HEIGHT = 100


def watermark(img, logo, watermark_text):
    # Resize logo
    logo = resize_logo(logo)

    # Dimension stuff
    img_height = img.shape[0]
    logo_height = logo.shape[0]
    img_width = img.shape[1]
    logo_width = logo.shape[1]
    width_diff = img_width - logo_width
    logo_border_diff = FSOCO_IMPORT_BORDER_THICKNESS - FSOCO_IMPORT_LOGO_HEIGHT

    # Border dimensions
    top = bottom = left = right = FSOCO_IMPORT_BORDER_THICKNESS
    # Make borders
    img = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_ISOLATED)
    # Pad logo for easier concatenating
    logo = cv2.copyMakeBorder(logo, 0, 0, 0, (width_diff + FSOCO_IMPORT_BORDER_THICKNESS), cv2.BORDER_ISOLATED)

    # fsoco = cv2.resize(fsoco, (logo_height, logo_height))

    # Update image shape after borders have been updated
    img_height = img.shape[0]
    # Insert logo into image
    # img[0:logo_height, :logo_height] = fsoco
    # print(img_height)
    img[(img_height - FSOCO_IMPORT_BORDER_THICKNESS):img_height - logo_border_diff,
    FSOCO_IMPORT_BORDER_THICKNESS:] = logo
    # Length of this static text (Arial) in pixel
    # See https://www.math.utah.edu/~beebe/fonts/afm-widths.html
    txt_len = 180
    # Add text for creation and modification time
    # Text's anchor is its bottom left corner
    text_anchor_top = (FSOCO_IMPORT_BORDER_THICKNESS, img_height - 30)
    text_anchor_bot = (FSOCO_IMPORT_BORDER_THICKNESS + txt_len, img_height - 30)

    anchors = [text_anchor_top, text_anchor_bot]
    texts = ["Created on:", watermark_text]
    img = draw_text_on_img(img, anchors, texts)
    return img


def resize_logo(img_logo):
    # Resize while keeping aspect ratio
    # FSOCO_IMPORT_LOGO_HEIGHT / image_height
    scale_pct = FSOCO_IMPORT_LOGO_HEIGHT / float(img_logo.shape[0])
    resized_width = int(img_logo.shape[1] * scale_pct)

    resized_img_logo = cv2.resize(img_logo, (resized_width, FSOCO_IMPORT_LOGO_HEIGHT))

    return resized_img_logo


def draw_text_on_img(cv_img, anchors, texts):
    assert (len(anchors) is len(texts))
    pil_img = cvmat_to_pil(cv_img)
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)

    pil_draw = ImageDraw.Draw(pil_img)

    for anchor, text in zip(anchors, texts):
        pil_draw.text(anchor, text, font=font, fill=(255, 255, 255))

    cv_img = pil_to_cvmat(pil_img)
    return cv_img


def pil_to_cvmat(pil_img):
    # From https://stackoverflow.com/questions/43232813/convert-opencv-image-format-to-pil-image-format
    # use numpy to convert the pil_image into a numpy array
    np_img = np.array(pil_img)

    # convert to a opencv image, notice the COLOR_RGB2BGR which means that
    # the color is converted from RGB to BGR format
    cv_img = cv2.cvtColor(np_img, cv2.COLOR_RGB2BGR)

    return cv_img


def cvmat_to_pil(cv_img):
    # From https://stackoverflow.com/questions/43232813/convert-opencv-image-format-to-pil-image-format
    # convert from opencv to PIL. Notice the COLOR_BGR2RGB which means that
    # the color is converted from BGR to RGB
    pil_img = Image.fromarray(cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB))

    return pil_img
