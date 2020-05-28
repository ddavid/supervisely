# coding: utf-8

import os
import cv2
import json
import time
import supervisely_lib as sly
from supervisely_lib.annotation.label import Label
from supervisely_lib.annotation.annotation import Annotation, AnnotationJsonFields

import fsoco_lib.fsoco_watermark as fsoco


def convert():

    task_settings = json.load(open(sly.TaskPaths.TASK_CONFIG_PATH, 'r'))
    logo_file_name = "logo.png"

    try:
        project_cwd = sly.TaskPaths.DATA_DIR
        sly.logger.info('Import info: Uploaded folder is a Supervisely Project, working from {}'.format(project_cwd))
        sly.logger.info('Current working directory contents: {}'.format(os.listdir(project_cwd)))
        project = sly.Project(project_cwd, sly.OpenMode.READ)
        logo_path = os.path.join(project_cwd, logo_file_name)
        sly.logger.info('Trying to read logo file from path: {}'.format(logo_path))
        logo_img = cv2.imread(logo_path)
        if not os.path.isfile(logo_path):
             sly.logger.error("No logo file found in the root directory.")
             sly.logger.info("Searched for the following logo path: {}".format(logo_path))
             return 1
        watermark_project(project, logo_img)
    except FileNotFoundError:
        possible_projects = sly.fs.get_subdirs(sly.TaskPaths.DATA_DIR)
        if len(possible_projects) != 1:
            raise RuntimeError('Wrong input project structure, or multiple projects are passed.')
        project_cwd = os.path.join(sly.TaskPaths.DATA_DIR, possible_projects[0])
        sly.logger.info('Import info: Uploaded sub-directory is a Supervisely Project, working from {}'.format(project_cwd))
        sly.logger.info('Current working directory contents: {}'.format(os.listdir(project_cwd)))
        project = sly.Project(project_cwd, sly.OpenMode.READ)
        logo_path = os.path.join(project_cwd, logo_file_name)
        sly.logger.info('Trying to read logo file from path: {}'.format(logo_path))
        logo_img = cv2.imread(logo_path)
        if not os.path.isfile(logo_path):
             sly.logger.error("No logo file found in the root directory.")
             sly.logger.info("Searched for the following logo path: {}".format(logo_path))
             return 1

        watermark_project(project, logo_img)
    except Exception as e:
        raise e

    sly.logger.info(
        'Project info: {} dataset(s), {} images(s).'.format(len(project.datasets), project.total_items))
    project.validate()

    project.copy_data(sly.TaskPaths.RESULTS_DIR, dst_name=task_settings['res_names']['project'], _use_hardlink=True)


def watermark_project(project, logo_img):
    meta = project.meta
    sly.logger.info('Project meta attribute: {}'.format(project.meta))
    for dataset in project.datasets:
        img_dir = dataset.img_dir
        ann_dir = dataset.ann_dir
        img_paths = [img_dir + '/' + img_name for img_name in  os.listdir(img_dir)]
        ann_paths = [ann_dir + '/' + ann_name for ann_name in os.listdir(ann_dir)]
        img_progress = sly.Progress('Watermarking Dataset: {!r}'.format(dataset.name), len(img_paths))
        ann_progress = sly.Progress('Adjusting Labels for Watermarked images: ', len(ann_paths))
        # Watermark all images except the logo
        watermark_images(img_paths, logo_img, img_progress)
        # Adjust labels
        adjust_annotations(ann_paths, meta, ann_progress)


def watermark_images(img_paths, logo_img, progress):

    for img_path in img_paths:
        watermark_date = last_modified = time.ctime(os.path.getmtime(img_path))
        creation_time = time.ctime(os.path.getctime(img_path))
        if not last_modified:
            watermark_date = creation_time

        img = cv2.imread(img_path)
        img = fsoco.watermark(img, logo_img, watermark_date)
        cv2.imwrite(img_path, img)
        progress.iter_done_report()


def adjust_annotations(ann_paths, meta, progress):

    for ann_path in ann_paths:
        temp_json_data = None
        with open(ann_path, 'r') as annotation_file:
            temp_annotation = Annotation.from_json(json.load(annotation_file), meta)
            # Adjust Image dimension infos for annotation file
            new_img_size = tuple(map(lambda dim: dim + fsoco.FSOCO_IMPORT_BORDER_THICKNESS * 2, temp_annotation.img_size))
            temp_annotation._img_size = new_img_size
            # Transform labels according to borders added by watermarking
            #translate_label = (lambda label: [label.translate(drow=fsoco.FSOCO_IMPORT_BORDER_THICKNESS, dcol=fsoco.FSOCO_IMPORT_BORDER_THICKNESS)])
            #temp_annotation.transform_labels(translate_label)
            temp_labels = []
            for label in temp_annotation._labels:
                # Do stuff to labels
                # Add border thickness once to each dimension of the bbox points.
                temp_label = label.translate(fsoco.FSOCO_IMPORT_BORDER_THICKNESS, fsoco.FSOCO_IMPORT_BORDER_THICKNESS)
                temp_labels.append(temp_label)
            temp_annotation._labels = temp_labels
            # Save transformed annotation
            temp_json_data = temp_annotation.to_json()
        with open(ann_path, 'w') as annotation_file:
            annotation_file.write(json.dumps(temp_json_data))
        progress.iter_done_report()


def main():
    convert()
    sly.report_import_finished()


if __name__ == '__main__':
    sly.main_wrapper('SLY_FORMAT_IMPORT', main)
