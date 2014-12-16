#!/usr/bin/env python
import os
import sys

import rawpy
import imageio

with open(os.path.join(os.environ['HOME'],'.ph.sh'), 'r') as config:
    library = config.readline().strip()

raws = []

for root, folders, files in os.walk(library):
    for f in files:
        if f.endswith('.CR2'):
            raws.append(os.path.join(root, f))


for raw in raws:
    print('Converting ' + raw + '...')
    image = rawpy.imread(raw)
    rgb = image.postprocess(use_camera_wb=True, no_auto_bright=False, output_bps=16)

    file_name = raw.split('/')[-1].split('.')[0] + '.tiff'
    f = os.path.join(library, 'tiff', file_name)

    print('Saving to ' + f + '...')
    imageio.imsave(f, rgb)
