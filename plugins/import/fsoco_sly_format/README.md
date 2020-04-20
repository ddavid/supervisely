# FSOCO Import Supervisely format 

This plugin allows you to upload Projects that have previously been annotated on Supervisely or converted to Supervisely format from other annotation formats by using one of the [label converters](https://github.com/ddavid/fsoco/tree/master/scripts/label-converters). // Replace this link with the new official fsoco repository 
More about Supervisely format can be read in the [annotation format documentation](https://docs.supervise.ly/ann_format/).

For this format the structure of directory should be the following:

```
my_project
├── meta.json
├── dataset_name_01
│   ├── ann
│   │   ├── img_x.json
│   │   ├── img_y.json
│   │   └── img_z.json
│   └── img
│       ├── img_x.jpeg
│       ├── img_y.jpeg
│       └── img_z.jpeg
├── dataset_name_02
│   ├── ann
│   │   ├── img_x.json
│   │   ├── img_y.json
│   │   └── img_z.json
│   └── img
│       ├── img_x.jpeg
│       ├── img_y.jpeg
│       └── img_z.jpeg
```

Directory "my_project" contains two folders and a file `meta.json`. For each folder one correspondingly named dataset will be created inside the project. **Exactly** this structure **and** valid SLY annotations are expected by the import plugin. Should you run into any issues, please inspect the task's log file before contacting us directly.

## Watermark Details

The generated watermark will consist of your team's logo and a timestamp.
The logo will be resized to a height of `100px`, while keeping the aspect ratio unchanged. To guarantee a crisp version of your logo and avoid unexpected distortions, use a version of your logo that fits these constraints.
Furthermore, the background on which the logo will be placed is black. To guarantee a good result, use a version of your logo with a black background. 
Transparency is not guaranteed to work; as creating a black background is very easy and fast, we have chosen not to increase the complexity of this tool to handle all minutiae of transparency with OpenCV.

## Example Watermarked Image

<img src="https://i.ibb.co/3p5hKxm/watermarked-mms.jpg" alt="FSOCO watermark mucmotorsport image" width="600">


### Example
In this example we will upload project with one dataset and will name it "Test Project".

![](https://i.imgur.com/Vuhqur1.gif)
