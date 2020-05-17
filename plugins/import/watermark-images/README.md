# FSOCO Image Import

This plugin allows you to upload images without any annotations in the correct format for contributing to FSOCO. 
Additionally, it will generate a watermark for the images with your team's logo and timestamp for the upload time.

## Watermark Details

The generated watermark will consist of your team's logo and a timestamp.
The logo will be resized to a height of `100px`, while keeping the aspect ratio unchanged. To guarantee a crisp version of your logo and avoid unexpected distortions, use a version of your logo that fits these constraints.
Furthermore, the background on which the logo will be placed is black. To guarantee a good result, use a version of your logo with a black background. 
Transparency is not guaranteed to work; as creating a black background is very easy and fast, we have chosen not to increase the complexity of this tool to handle all minutiae of transparency with OpenCV.

## Input files structure

You have to drag and drop one directory with images. The directory's name defines the dataset's name.
This plugin will check for the logo file `logo.png` in the root directory of the uploaded directory. The root directory in the example below would be `my_folder1/`.
If this plugin doesn't find a logo file or finds more than one possible version, it won't be able to finish the upload.
```
 my_folder1
    ├── logo.png
    ├── meta.json
    ├── img_01.JPG
    ├── img_02.jpeg
    ├── ...
    └── img_03.jpg

```
While uploading the data, Supervisely will prompt you to name the created project. The name of the folder you uploaded, in this case `my_folder1`, will be the name of the dataset within the newly created project.

Should you run into any issues, please inspect the task's log file before contacting us directly.

## Example Watermarked Images

<img src="https://www.fsoco-dataset.com/assets/img/tools/watermarked_mms.jpg" alt="FSOCO watermark mucmotorsport image" width="600">
<img src="https://www.fsoco-dataset.com/assets/img/tools/watermarked_amz.jpg" alt="FSOCO watermark amz image" width="600">