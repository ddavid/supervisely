import cv2 as cv
import numpy as np

def main():

    img = cv.imread("00000251_skid-pad.jpg")
    logo = cv.imread("mms-logo-black-background.png")
    fsoco = cv.imread("fsoco-favicon-test.png")
    print(img.shape)
    img_height = img.shape[0]
    logo_height = logo.shape[0]
    img_width = img.shape[1]
    logo_width = logo.shape[1]
    width_diff = img_width - logo_width
    print("Width Difference: ", width_diff)

    top = bottom = left = right = logo_height
    # Make border
    img = cv.copyMakeBorder(img, top, bottom, left, right, cv.BORDER_ISOLATED)
    print(img.shape)
    print(logo.shape)
    logo = cv.copyMakeBorder(logo, 0, 0, 0, (width_diff + logo_height), cv.BORDER_ISOLATED)
    print(logo.shape)
    fsoco = cv.resize(fsoco, (logo_height, logo_height))

    img[0:logo_height,:logo_height] = fsoco
    img[img_height:(img_height + logo_height),logo_height:] = logo



    #watermark_img = np.concatenate((img, logo), axis=0)

    print(img.size)

    #watermark_img = ...
    cv.imwrite("watermark-test-black.jpg", img)

if __name__ == '__main__':
    main()