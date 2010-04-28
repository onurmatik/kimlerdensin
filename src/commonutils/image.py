# -*- coding: utf-8 -*-

from os import path, makedirs
from PIL import Image
from cStringIO import StringIO
from django.conf import settings


def save_image(image, dir, filename=None):
    try:
        content = image['content']
    except TypeError: # no content at all
        raise

    try:
        im = Image.open(StringIO(content))
        im.verify()
    except IOError: # Python Imaging Library doesn't recognize it as an image
        raise

    extension = im.format.lower()
    if extension == 'jpeg':
        extension = 'jpg'

    if not filename:
        # use the original filename of the uploded image
        filename = path.splitext(image['filename'])[0].lower()

    try:
        makedirs('%s%s' % (settings.MEDIA_ROOT, dir))
    except:
        pass

    img_path = '%s%s.%s' % (dir,
                            filename,
                            extension)
    # if the image with the same filename exists, append 'i' to the filename
    if path.exists('%s%s' % (settings.MEDIA_ROOT, img_path)):
        i = 1
        while path.exists('%s%s' % (settings.MEDIA_ROOT, img_path)):
            img_path = '%s%s_%s.%s' % (dir,
                                       filename,
                                       i,
                                       extension)
            i += 1

    file = open('%s%s' % (settings.MEDIA_ROOT, img_path), 'wb')
    try:
        file.write(content)
        file.close()
    except:
        raise
    
    return img_path

