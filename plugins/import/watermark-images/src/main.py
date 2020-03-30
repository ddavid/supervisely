# coding: utf-8

import os
from collections import defaultdict
import cv2

import supervisely_lib as sly
from supervisely_lib import fs
from supervisely_lib import TaskPaths
from supervisely_lib.io.json import load_json_file


DEFAULT_DS_NAME = 'ds'


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

    for dataset in in_datasets:
        watermark_logo = cv2.imread(convert_options['watermark-logo'])
        for img in dataset:
            img = watermark(img, watermark_logo)


    normalize_exif = convert_options.get('normalize_exif')

    pr = sly.Project(os.path.join(sly.TaskPaths.RESULTS_DIR, task_settings['res_names']['project']),
                     sly.OpenMode.CREATE)

    for ds_name, img_paths in in_datasets.items():
        sly.logger.info(
            'Found {} files with supported image extensions in Dataset {!r}.'.format(len(img_paths), ds_name))

        ds = pr.create_dataset(ds_name)
        progress = sly.Progress('Dataset: {!r}'.format(ds_name), len(img_paths))
        for img_path in img_paths:
            try:
                item_name = os.path.basename(img_path)

                if normalize_exif:
                    img = sly.image.read(img_path)
                    sly.image.write(img_path, img)

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

def watermark(img, logo):

    # Dimension stuff
    img_height = img.shape[0]
    logo_height = logo.shape[0]
    img_width = img.shape[1]
    logo_width = logo.shape[1]
    width_diff = img_width - logo_width
    # print("Width Difference: ", width_diff)

    # Border dimensions
    top = bottom = left = right = logo_height
    # Make borders
    img = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_ISOLATED)
    # Pad logo for easier concatenating
    logo = cv2.copyMakeBorder(logo, 0, 0, 0, (width_diff + logo_height), cv2.BORDER_ISOLATED)

    #fsoco = cv.resize(fsoco, (logo_height, logo_height))

    #img[0:logo_height, :logo_height] = fsoco
    img[img_height:(img_height + logo_height), logo_height:] = logo

    return img


def main():
    convert()
    sly.report_import_finished()


if __name__ == '__main__':
    sly.main_wrapper('IMPORT_IMAGES', main)
