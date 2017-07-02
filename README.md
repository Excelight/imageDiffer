# ImageDiffer: Find the difference of images


## How to use

The input should be one image that consists of several similar images. Maybe have and arrangement like nx1 or 1xn. ImageDiffer can help you to figure out the main difference between them.
```sh
usage: imageDiffer [-h] -f IMAGE_PATH [-d {h,v}] [-c COUNT]
                   [-b BACKGROUND_COLOR]

Process image diff

optional arguments:
  -h, --help            show this help message and exit
  -f IMAGE_PATH, --file IMAGE_PATH
                        the input image path
  -d {h,v}, --direction {h,v}
                        h: stands for horizontal; v: stands for vertical;
                        default to h
  -c COUNT, --count COUNT
                        the count to split the image into; default to 2
  -b BACKGROUND_COLOR, --bgcolor BACKGROUND_COLOR
                        the r,g,b color of background; default to 255,255,255
```
Here's the example to use the default configuration to find difference.
```
python imageDiffer.py -f input.jpg
```
