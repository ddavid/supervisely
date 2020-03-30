# Import Watermarked Images

This plugin allows you to upload only images without any annotations. 
Additionally, it will generate a watermark for the images with your team's logo.

#### Input files structure

You have to drag and drop one or few directories with images. Directory name defines Dataset name.
This plugin will also check for the logo `.png` file in  your uploaded folder.
If it doesn't find one, it won't be able to finish the upload.
```
 .
 └── my_folder1
    ├── logo.png
    ├── img_01.JPG
    ├── img_02.jpeg
    ├── ...
    └── img_03.jpg

```

As a result we will get a project with one watermarked dataset with the name: `my_folder1`.
