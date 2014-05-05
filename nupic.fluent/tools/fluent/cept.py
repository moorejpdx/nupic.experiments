# ----------------------------------------------------------------------
# Numenta Platform for Intelligent Computing (NuPIC)
# Copyright (C) 2014, Numenta, Inc.  Unless you have purchased from
# Numenta, Inc. a separate commercial license for this software code, the
# following terms and conditions apply:
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see http://www.gnu.org/licenses.
#
# http://numenta.org/licenses/
# ----------------------------------------------------------------------

import os

#import pycept
from PIL import Image, ImageDraw
import StringIO


CACHE_DIR = "./cache"


class Cept():


  def __init__(self):
#    if 'CEPT_APP_ID' not in os.environ or 'CEPT_APP_KEY' not in os.environ:
#      print("Missing CEPT_APP_ID and CEPT_APP_KEY environment variables.")
#      print("You can retrieve these by registering for the CEPT API at ")
#      print("https://cept.3scale.net/")
#      raise
#
#    self.appId  = os.environ['CEPT_APP_ID']
#    self.appKey = os.environ['CEPT_APP_KEY']

#    self.client = pycept.Cept(self.appId, self.appKey, cache_dir=CACHE_DIR)
    self.lookup = None


  def getBitmap(self, string):
    size = (768, 15)
    temp_im = Image.new('1', size, "white") # create the image
    draw = ImageDraw.Draw(temp_im)   # create a drawing object that is
                                # used to draw on the new image
    text_pos = (2,2) # top-left position of our text
    text = string # text to draw

    # Now, we'll do the drawing and put in a cropped image box
    draw.text(text_pos, text)
    im = temp_im.crop((0, 0, draw.textsize(text)[0]+5, 15 ))

    # cleanup
    del draw

    #drop image into a string stream
    output = StringIO.StringIO()
    im.save(output, format="PNG")
    contents = output.getvalue()
    output.close()

    # convert to bytes
    s = bytearray(contents)
    return {"positions": s}


  def getClosestStrings(self, bitmap, width=128, height=128):
    print "bitmap: " + repr(bitmap)
    time.sleep(5)
    return "whatever"
#    return self.client.bitmapToTerms(width, height, bitmap)
