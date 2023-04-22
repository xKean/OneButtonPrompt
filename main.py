import sys, os
from PIL import Image, PngImagePlugin
from aesthetic import aestheticscorer

sys.path.append(os.path.abspath(".."))

from call_txt2img import *
from call_img2img import *
from build_dynamic_prompt import *
from call_extras import *


# needs following directories to exist:
# C:\automated_output\
# C:\automated_output\extras\
# C:\automated_output\img2img\
# C:\automated_output\txt2img\
# C:\automated_output\Prompts\

loops = 150  # amount of images to generate
steps = 0

while steps < loops:
    # build prompt
    randomprompt = build_dynamic_prompt(6,"all","all","all")
    randomModel = generateRandomModel()
    
    # prompt + size
    #check if any good
    txt2img = call_txt2img(randomprompt, generateRandomRatio(), False, 0, randomModel)

    # upscale via img2img first
    img2img = call_img2img(txt2img,0.25,1.5,256, "SwinIR_4x", randomModel)
    niceImg = call_img2img(img2img,0.3,2,256, "4x-UltraMix_Balanced", randomModel)

    # upscale via extras upscaler next
    finalfile = call_extras(niceImg, randomModel)

    steps += 1