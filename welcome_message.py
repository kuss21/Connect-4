#!/usr/bin/env python
from PIL import Image
from PIL import ImageDraw
from samplebase import SampleBase #need to import on everything. tells argument used
from rgbmatrix import graphics, RGBMatrix, RGBMatrixOptions
import time

# run command for this file:
# sudo ./welcome_message.py --led-rows=32 --led-cols=64 --led-slowdown-gpio=4 

options = RGBMatrixOptions()
options.hardware_mapping = 'adafruit-hat'

class welcome(SampleBase):
    def __init__(self, *args, **kwargs):
        super(welcome, self).__init__(*args, **kwargs)
        self.parser.add_argument('-t', default='Connect 4')

    def run(self):
        wel_canvas = self.matrix.CreateFrameCanvas()
        wel_color = graphics.Color(127,255,212) #RED=(255,0,0), CORAL=(255,127,80), FOREST GREEN=(34,129,34), AQUAMARINE=(127,255,212)
        font = graphics.Font()
        font.LoadFont('../../../fonts/7x13.bdf') #IF WE MOVE THIS FILE, WE NEED TO REWRITE THIS!!!!
        #text will take up 9 lines, cannot make smaller with this font
        pos_wel_x = 0 #this will make the text flush to the L
        pos_wel_y = 9 #this will make the text flush to the top
        wel_text = 'Connect 4'

        xpos_player_1 = 16 # halfway on the left attempt
        ypos_player = 20
        xpos_player_2 = 48 # halfway on the right attempt
        

        while True:
            graphics.DrawText(wel_canvas, font, pos_wel_x, pos_wel_y, wel_color, wel_text)
            ####UPDATE COLORS ASSSOCIATED WITH NUMBERS TO GO WITH BUTTON COLOR########
            graphics.DrawText(wel_canvas, font, xpos_player_1,ypos_player, wel_color, '1') 
            graphics.DrawText(wel_canvas, font, xpos_player_2, ypos_player, wel_color, '2')
            wel_canvas = self.matrix.SwapOnVSync(wel_canvas)

if __name__ == '__main__':
    wel_msg = welcome()
    if (not wel_msg.process()):
        wel_msg.print_help()



