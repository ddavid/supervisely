# FSOCO Supervisely Import

This plugin allows you to upload Projects that have previously been annotated on Supervisely or converted to Supervisely format from other annotation formats by using one of the [label converters](https://github.com/fsoco/fsoco/tree/master/tools/label_converters).
More about Supervisely format can be read in the [annotation format documentation](https://docs.supervise.ly/data-organization/import-export/supervisely-format).

The directory structure should be the following:

```
my_project
├── meta.json
├── logo.png
├── dataset_name_01
│   ├── ann
│   │   ├── img_x.json
│   │   ├── img_y.json
│   │   └── img_z.json
│   └── img
│       ├── img_x.jpg
│       ├── img_y.jpg
│       └── img_z.jpg
├── dataset_name_02
│   ├── ann
│   │   ├── img_x.json
│   │   ├── img_y.json
│   │   └── img_z.json
│   └── img
│       ├── img_x.jpg
│       ├── img_y.jpg
│       └── img_z.jpg
.
.
.
```

Directory "my_project" contains two folders and a file `meta.json`. For each folder one correspondingly named dataset will be created inside the project. **Exactly** this structure **and** valid SLY annotations are expected by the import plugin. Should you run into any issues, please inspect the task's log file before contacting us directly.

Please remember to use the correct [FSOCO meta.json](http://www.fsoco-dataset.com/assets/meta.json).

If you have previously labeled a dataset on Supervisely, you can use [DTL](https://docs.supervise.ly/data-manipulation/index/data-layers/data) and this [example config](https://www.fsoco-dataset.com/assets/class_mapping_dtl.json) to generate a fitting version of your dataset. With DTL you can first map your classes to the correct FSOCO ones, refer to the [FSOCO meta.json](http://www.fsoco-dataset.com/assets/meta.json) for this step.<br/>
After generating a version of your dataset with a compatible subset of classes, download your dataset, replace its `meta.json` with the one above or adjust its contents to be the same, and upload this slightly modified version of the dataset to Supervisely with this plugin.

## Watermark Details

The generated watermark will consist of your team's logo and an UTC upload timestamp.
Borders for an additional `140px` on each edge will be added to the image.
The logo will be resized to a height of `100px`, while keeping the aspect ratio unchanged. To guarantee a crisp version of your logo and avoid unexpected distortions, use a version of your logo that fits these constraints.
Furthermore, the background on which the logo will be placed is black.
Transparency is not guaranteed to work; as creating a black background is very easy and fast, we have chosen not to increase the complexity of this tool to handle all minutiae of transparency with OpenCV.

## Example Watermarked Images

<img src="https://i.ibb.co/thc1YyP/watermarked-mms.jpg" alt="FSOCO watermark mucmotorsport image" width="600">
<img src="https://i.ibb.co/S5WF5pf/watermarked-amz.png" alt="FSOCO watermark amz image" height="600">
<img src="https://i.ibb.co/LYTqn8R/watermarked-ff.jpg" alt="FSOCO watermark fast forest image" height="600">
