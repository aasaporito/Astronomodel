#!/usr/bin/python
# Modified from: https://gist.github.com/jaysridhar/94c2802c89d239f38d8eda1b72762eae
import os
from PIL import Image

import logging
Image.MAX_IMAGE_PIXELS = None

logger = logging.getLogger('preprocc')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('preproc.log')
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)

logger.info('-----Image Preprocessing Started-----')

formats = ["BMP", "DIB", "EPS", "GIF", "ICNS", "ICO", "IM", "JPG", "JPEG",
           "J2K", "J2P", "JPX", "MSP", "PCX", "PNG", "PPM", "SGI",
           "SPIDER", "TGA", "TIFF", "WebP", "XBM"]

input_folder = 'Images'  # Path to your folder
out_dir = "PP_Images"
out_format = 'png'
in_file_dir = os.listdir(input_folder)

infiles = in_file_dir

print(len(infiles))
for i in range(6635, len(infiles)):
    logger.info(f"Processing {infiles[i]}")
    fname = infiles[i]

    if os.path.isdir(fname): continue
    base = os.path.basename(fname)
    f, ext = os.path.splitext(base)
    if len(ext) <= 1: continue
    ext = ext[1:]
    if ext.upper() not in formats:
        print('{}: format not supported .. ignoring'.format(fname))
        continue
    image = Image.open(input_folder + "/" + fname)
    opath = os.path.join(out_dir, '{}.{}'.format(f, out_format.lower()))
    image = image.resize((1024, 1024))
    if image.mode == "CMYK":
        image = image.convert("RGB")
    image.save(opath, out_format)
    logger.info(f"Saved {infiles[i]}: {i}/{len(infiles)}")

logger.info(f"Finished processing {len(infiles)}")
logger.info("Exiting")
