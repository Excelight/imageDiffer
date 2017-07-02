#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
    print _orign_width
    print _origin_height
    im1 = im.crop((0, 0, _orign_width/2, _origin_height))
    im2 = im.crop((_orign_width/2, 0, _orign_width, _origin_height))
    im1Trimed = imageTrim(im1, bgColor)
    im2Trimed = imageTrim(im2, bgColor)
    return [im1Trimed, im2Trimed]

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

    # Starting
    splitedImgs = imageSplit(IMAGE_PATH, DIRECTION, SPLIT_COUNT, BACKGROUND_COLOR)
    im1 = splitedImgs[0]
    im2 = splitedImgs[1]
    ImageChops.difference(im1, im2).show()
