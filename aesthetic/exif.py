#!/bin/env python

import os
import io
import re
import sys
import warnings
from PIL import Image, ExifTags, TiffImagePlugin, PngImagePlugin

warnings.filterwarnings("ignore", category=UserWarning)


class Exif:
    __slots__ = ('__dict__')
    def __init__(self, image = None):
        super(Exif, self).__setattr__('exif', Image.Exif())
        self.pnginfo = PngImagePlugin.PngInfo()
        self.tags = {**dict(((k, v) for k, v in ExifTags.TAGS.items())), **dict(((k, v) for k, v in ExifTags.GPSTAGS.items()))}
        self.ids = {**dict(((v, k) for k, v in ExifTags.TAGS.items())), **dict(((v, k) for k, v in ExifTags.GPSTAGS.items()))}
        if image is not None:
            self.load(image)

    def __getattr__(self, attr):
        if attr in self.__dict__:
            return self.__dict__[attr]
        return self.exif.get(attr, None)

    def load(self, img: Image):
        img.load() # exif may not be ready
        exif_dict = {}
        try:
            exif_dict = dict(img._getexif().items()) # pylint: disable=protected-access
        except:
            exif_dict = dict(img.info.items())
        for key, val in exif_dict.items():
            if isinstance(val, bytes): # decode bytestring
                val = self.decode(val)
            if val is not None:
                if isinstance(key, str):
                    self.exif[key] = val
                    self.pnginfo.add_text(key, str(val), zip=False)
                elif isinstance(key, int) and key in ExifTags.TAGS: # add known tags
                    if self.tags[key] in ['ExifOffset']:
                        continue
                    self.exif[self.tags[key]] = val
                    self.pnginfo.add_text(self.tags[key], str(val), zip=False)
                    # if self.tags[key] == 'UserComment': # add geninfo from UserComment
                        # self.geninfo = val
                else:
                    print('metadata unknown tag:', key, val)
        for key, val in self.exif.items():
            if isinstance(val, bytes): # decode bytestring
                self.exif[key] = self.decode(val)

    def decode(self, s: bytes):
        remove_prefix = lambda text, prefix: text[len(prefix):] if text.startswith(prefix) else text
        for encoding in ['utf-8', 'utf-16', 'ascii', 'latin_1', 'cp1252', 'cp437']: # try different encodings
            try:
                decoded = s.decode(encoding, errors="strict")
                val = remove_prefix(decoded, 'UNICODE') # remove silly prefix added by old pnginfo/exif encoding
                val = remove_prefix(val, 'ASCII')
                val = re.sub(r'[\x00-\x09]', '', val).strip() # remove remaining special characters
                if len(val) == 0: # remove empty strings
                    val = None
                return val
            except:
                pass
        return None

    def get_bytes(self):
        ifd = TiffImagePlugin.ImageFileDirectory_v2()
        exif_stream = io.BytesIO()
        for key, val in self.exif.items():
            if key in self.ids:
                ifd[self.ids[key]] = val
            else:
                print('metadata unknown exif tag:', key, val)
        ifd.save(exif_stream)
        raw = b'Exif\x00\x00' + exif_stream.getvalue()
        return raw


def read_exif(filename: str):
    try:
        img = Image.open(filename)
        exif = Exif(img)
        print('image:', filename, 'format:', img.format, 'metadata:', exif.exif)
    except Exception as e:
        print('metadata error reading:', filename, e)
    # exif.exif['Software'] = 'This is a Test'
    # img.save('input-scored.jpg', exif=exif.bytes())


if __name__ == '__main__':
    sys.argv.pop(0)
    if len(sys.argv) == 0:
        print('metadata:', 'no files specified')
    for fn in sys.argv:
        if os.path.isfile(fn):
            read_exif(fn)
        elif os.path.isdir(fn):
            for root, dirs, files in os.walk(fn):
                for file in files:
                    read_exif(os.path.join(root, file))
