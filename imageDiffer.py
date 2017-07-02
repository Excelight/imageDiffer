#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: excelight

from PIL import Image, ImageFilter, ImageChops
import argparse

def imageSplit(path, direction, count, bgColor):
    """
    Split the image into several sub images

    Args:
        path:       The path of the original image.
        direction:  The direction of how to splilt the image. 1: horizontal, 2: vertical
        count:      Split The image into @count sub images.
        bgColor:    The background color used to segement the image and background

    Returns:
        The list of subimages
    """
    im = Image.open(path)
    _orign_width, _origin_height = im.size
    subImages = []
    if 'v' == direction:
        width = _orign_width
        height = _origin_height / count
        for i in range(count):
            subImages.append(im.crop((0, height * i, width, height * (i + 1))))
        pass
    else:
        width = _orign_width / count
        height = _origin_height
        for i in range(count):
            subImages.append(im.crop((width * i, 0, width * (i + 1), height)))

    subTrimedImages = []
    for subIm in subImages:
        subTrimedImages.append(imageTrim(subIm, bgColor))
    return subTrimedImages

def imageTrim(imageIn, bgColor):
    """
    Trim white spaces of the image

    Args:
        imageIn:    The original image.
        bgColor:    The background of the image which will be cropped.

    Returns:
        The trimed image.
    """
    imBg = Image.new(imageIn.mode, imageIn.size, bgColor)
    diff = ImageChops.difference(imageIn, imBg)
    diff = ImageChops.add(diff, diff, scale=2.0, offset=-100)  # you may adjust scale or offset here if necessary
    bbox = diff.getbbox()
    if bbox:
        return imageIn.crop(bbox)


if __name__ == "__main__":
    # processing args
    parser = argparse.ArgumentParser(prog="imageDiffer", description='Process image diff')
    parser.add_argument('-f', '--file', required=True, metavar='IMAGE_PATH', help='the input image path')
    parser.add_argument('-d', '--direction', default='h', choices=['h', 'v'],
                        help='h: stands for horizontal; v: stands for vertical; default to  h')
    parser.add_argument('-c', '--count', default=2, type=int, help='the count to split the image into; default to 2')
    parser.add_argument('-b', '--bgcolor', default="255,255,255", metavar="BACKGROUND_COLOR",
                        help='the r,g,b color of background; default to 255,255,255')
    args = parser.parse_args()
    IMAGE_PATH  = args.file
    DIRECTION   = args.direction
    SPLIT_COUNT = args.count
    BACKGROUND_COLOR = tuple([int(i) for i in args.bgcolor.split(',')])

    # Start
    # Split into several sub images
    splitedImgs = imageSplit(IMAGE_PATH, DIRECTION, SPLIT_COUNT, BACKGROUND_COLOR)
    baseImg = splitedImgs[0]
    # Find differences
    diffs = []
    for i, subImg in enumerate(splitedImgs):
        if 0 == i:
            continue
        diffs.append(ImageChops.difference(baseImg, subImg))
    # Show
    for diff in diffs:
        diff.show()
