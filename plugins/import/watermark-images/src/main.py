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
from supervisely_lib.project.project_meta import ProjectMeta



DEFAULT_DS_NAME = 'ds'

# Watermark text constants
FONT_PATH = '/workdir/fonts/VeraMono.ttf'
FONT_SIZE = 16

# Don't change this one
FSOCO_IMPORT_BORDER_THICKNESS = 140
FSOCO_IMPORT_LOGO_HEIGHT = 100


def find_input_datasets():
    root_files_paths = set(fs.list_files(TaskPaths.DATA_DIR, filter_fn=sly.image.has_valid_ext))
    files_paths = set(fs.list_files_recursively(TaskPaths.DATA_DIR, filter_fn=sly.image.has_valid_ext))
    files_paths = files_paths - root_files_paths

    if len(root_files_paths) + len(files_paths) == 0:
        raise RuntimeError(f'Input directory is empty! Supported formats list: {sly.image.SUPPORTED_IMG_EXTS}.')

    datasets = defaultdict(list)
    for path in files_paths:
        ds_name = os.path.relpath(os.path.dirname(path), TaskPaths.DATA_DIR).replace(os.sep, '__')
        datasets[ds_name].append(path)

    default_ds_name = (DEFAULT_DS_NAME + '_' + sly.rand_str(8)) if DEFAULT_DS_NAME in datasets else DEFAULT_DS_NAME
    for path in root_files_paths:
        datasets[default_ds_name].append(path)

    return datasets


def convert():
    task_settings = load_json_file(sly.TaskPaths.TASK_CONFIG_PATH)
    in_datasets = find_input_datasets()

    convert_options = task_settings['options']

    logo_file_name = "logo.png"

    pr = sly.Project(os.path.join(sly.TaskPaths.RESULTS_DIR, task_settings['res_names']['project']),
                     sly.OpenMode.CREATE)
    # Set meta file to FSOCO template at end to avoid being set to default-initialized ProjectMeta
    meta_json = load_json_file("meta.json")
    pr.set_meta(ProjectMeta.from_json(meta_json))
    sly.logger.info(
        'Set project meta file to FSOCO template.')
    for ds_name, img_paths in in_datasets.items():
        # Read watermark logo image
        logo_path = [path for path in img_paths if path.endswith(logo_file_name)]
        if len(logo_path) != 1:
            sly.logger.error("You either have no logo in the project directory or more than one.")
            sly.logger.info("Got following logo paths: {}".format(logo_path))
            return 1
        logo_path = logo_path.pop()
        logo_img = cv2.imread(logo_path)
        # Filter out logo file to avoid adding it to the dataset
        img_paths = [path for path in img_paths if not path.endswith(logo_file_name)]
        sly.logger.info(
            'Found {} files with supported image extensions in Dataset {!r}.'.format(len(img_paths), ds_name))
        ds = pr.create_dataset(ds_name)
        progress = sly.Progress('Dataset: {!r}'.format(ds_name), len(img_paths))
        for img_path in img_paths:
            try:
                if not img_path == logo_path:
                    watermark_date = last_modified = time.ctime(os.path.getmtime(img_path))
                    creation_time = time.ctime(os.path.getctime(img_path))
                    if not last_modified:
                        watermark_date = creation_time
                    item_name = os.path.basename(img_path)

                    img = cv2.imread(img_path)
                    img = watermark(img, logo_img, watermark_date)
                    cv2.imwrite(img_path, img)

                ds.add_item_file(item_name, img_path, _use_hardlink=True)
            except Exception as e:
                exc_str = str(e)
                sly.logger.warn('Input sample skipped due to error: {}'.format(exc_str), exc_info=True, extra={
                    'exc_str': exc_str,
                    'dataset_name': ds_name,
                    'image_name': img_path,
                })
            progress.iter_done_report()

    if pr.total_items == 0:
        raise RuntimeError('Result project is empty! All input images have unsupported format!')

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

    #fsoco = cv2.resize(fsoco, (logo_height, logo_height))
    
    # Update image shape after borders have been updated
    img_height = img.shape[0]
    # Insert logo into image
    #img[0:logo_height, :logo_height] = fsoco
    # print(img_height)
    img[(img_height - FSOCO_IMPORT_BORDER_THICKNESS):img_height - logo_border_diff, FSOCO_IMPORT_BORDER_THICKNESS:] = logo 
    # Length of this static text (Vera) in pixel
    # See https://www.math.utah.edu/~beebe/fonts/afm-widths.html
    txt_len = 250
    # Add text for creation and modification time
    # Text's anchor is its bottom left corner
    text_anchor = (FSOCO_IMPORT_BORDER_THICKNESS, img_height - 30)
    # text_anchor_bot = (FSOCO_IMPORT_BORDER_THICKNESS + txt_len, img_height - 30)

    anchors = [text_anchor]
    texts = ["Uploaded on:  UTC  " + watermark_text]
    img = draw_text_on_img(img, anchors, texts)
    return img


def resize_logo(img_logo):
    # Add black border to the top side to introduce a gap between the logo and the image
    img_logo = cv2.copyMakeBorder(img_logo, 10, 0, 0, 0, cv2.BORDER_CONSTANT, value=[0, 0, 0])
    # Resize while keeping aspect ratio
    # FSOCO_IMPORT_LOGO_HEIGHT / image_height
    scale_pct = FSOCO_IMPORT_LOGO_HEIGHT / float(img_logo.shape[0])
    resized_width = int(img_logo.shape[1] * scale_pct)
   
    resized_img_logo = cv2.resize(img_logo, (resized_width, FSOCO_IMPORT_LOGO_HEIGHT))
    
    return resized_img_logo
    
       
def draw_text_on_img(cv_img, anchors, texts):
    
    assert(len(anchors) is len(texts))
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
    np_img=np.array(pil_img)  

    # convert to a opencv image, notice the COLOR_RGB2BGR which means that 
    # the color is converted from RGB to BGR format
    cv_img=cv2.cvtColor(np_img, cv2.COLOR_RGB2BGR) 
    
    return cv_img

def cvmat_to_pil(cv_img):
    # From https://stackoverflow.com/questions/43232813/convert-opencv-image-format-to-pil-image-format
    # convert from opencv to PIL. Notice the COLOR_BGR2RGB which means that 
    # the color is converted from BGR to RGB
    pil_img=Image.fromarray(cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB))
    
    return pil_img
    
    
def main():
    convert()
    sly.report_import_finished()


if __name__ == '__main__':
    sly.main_wrapper('WATERMARK_IMPORT_IMAGES', main)
