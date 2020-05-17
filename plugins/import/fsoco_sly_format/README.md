# FSOCO Supervisely Import

This plugin allows you to upload Projects that have previously been annotated on Supervisely or converted to Supervisely format from other annotation formats by using one of the [label converters](https://github.com/fsoco/fsoco/tree/master/tools/label_converters).
More about Supervisely format can be read in the [annotation format documentation](https://docs.supervise.ly/ann_format/).

The directory structure should be the following:

```
my_project
├── meta.json
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

## Watermark Details

The generated watermark will consist of your team's logo and an UTC upload timestamp.
The logo will be resized to a height of `100px`, while keeping the aspect ratio unchanged. To guarantee a crisp version of your logo and avoid unexpected distortions, use a version of your logo that fits these constraints.
Furthermore, the background on which the logo will be placed is black.
Transparency is not guaranteed to work; as creating a black background is very easy and fast, we have chosen not to increase the complexity of this tool to handle all minutiae of transparency with OpenCV.

## Example Watermarked Images

<img src="https://www.fsoco-dataset.com/assets/img/tools/watermarked_mms.jpg" alt="FSOCO watermark mucmotorsport image" width="600">
<img src="https://www.fsoco-dataset.com/assets/img/tools/watermarked_amz.jpg" alt="FSOCO watermark amz image" width="600">