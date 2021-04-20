#!/usr/bin/env python
from PIL import Image
from PIL import ImageDraw
from samplebase import SampleBase #need to import on everything. tells argument used
from rgbmatrix import graphics, RGBMatrix, RGBMatrixOptions
import time

options = RGBMartixOptions()
options.hardware_mapping = 'adafruit-hat'

class welcome(SampleBase):
    def __init__(self, *args, **kwargs):
        super(welcome, self).__init__(*args, **kwargs)
        self.parser.add_argument('-t', default='Connect 4')

    def run(self):
        end_canvas = self.matrix.CreateFrameCanvas()
