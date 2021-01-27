#!/usr/bin/env python
from PIL import Image
from PIL import ImageDraw
from samplebase import SampleBase
from rgbmatrix import graphics, RGBMatrix, RGBMatrixOptions
import time

# command to run program
# sudo ./Franklin_test.py --led-rows=32 --led-cols=64 --led-slowdown-gpio=4

options = RGBMatrixOptions()
options.hardware_mapping = 'adafruit-hat'

class TestFranklin(SampleBase):
    def __init__(self, *args, **kwargs):
        super(TestFranklin, self).__init__(*args, **kwargs)
        
    def run(self):
        boxcanvas = self.matrix.CreateFrameCanvas()
        boxColor = graphics.Color(128,0,128)

        # position variables for drawing board
        col_pos_x1 = 0
        col_pos_y1 = 2
        col_pos_x2 = 0
        col_pos_y2 = 31

        row_pos_x1 = 0
        row_pos_y1 = 2
        row_pos_x2 = 63
        row_pos_y2 = 2

        x = True

        while x is True:
            # draw in one column
            graphics.DrawLine(boxcanvas, col_pos_x1, col_pos_y1, col_pos_x2, col_pos_y2, boxColor)
            col_pos_x1 += 1 
            col_pos_x2 += 1
            graphics.DrawLine(boxcanvas, col_pos_x1, col_pos_y1, col_pos_x2, col_pos_y2, boxColor) 
            col_pos_x1 += 3
            col_pos_x2 += 3
            #boxcanvas = self.matrix.SwapOnVSync(boxcanvas)
            #time.sleep(2)
            # draw in rows
            graphics.DrawLine(boxcanvas, row_pos_x1, row_pos_y1, row_pos_x2, row_pos_y2, boxColor) 
            row_pos_y1 += 1
            row_pos_y2 += 1
            graphics.DrawLine(boxcanvas, row_pos_x1, row_pos_y1, row_pos_x2, row_pos_y2, boxColor) 
            row_pos_y1 += 3
            row_pos_y2 += 3
            boxcanvas = self.matrix.SwapOnVSync(boxcanvas)


# Main Function
if __name__=="__main__":
    test_frank = TestFranklin()
    if (not test_frank.process()):
        test_frank.print_help()
