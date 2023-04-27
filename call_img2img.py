import json
import requests
import io
import base64
import uuid
from PIL import Image, PngImagePlugin
import webuiapi

from random_functions import generateRandomNegative



def call_img2img(resultOld, denoising_strength = 0.25, scale = 1.5, padding = 64, upscaler = "LDSR", randomModel = 'rmadaMergeSD21768_v70'):

    image = resultOld.image
       #params to stay the same
    outputimg2imgfolder = 'C:/automated_output/img2img/'
    outputimg2imgfilename = str(uuid.uuid4())
    outputimg2imgpng = '.png'
    outputimg2imgFull = '{}{}{}'.format(outputimg2imgfolder,outputimg2imgfilename,outputimg2imgpng)

    #rest of prompt things

    sampler_index = 'DPM++ 2M Karras'
    steps = "35"
    prompt = "hello world"
    cfg_scale = 6
    width = "512"
    height = "512"


    api = webuiapi.WebUIApi(host='127.0.0.1',
                            port=7860,
                            sampler=sampler_index,
                            steps=steps)
    api.util_set_model(randomModel)
    if randomModel == "revAnimated_v122" or "dreamshaper_5BakedVae":
        apiOptions = api.get_options()
        apiOptions["CLIP_stop_at_last_layers"] = 2
        api.set_options(apiOptions)

    response = api.img2img(
                    images=[image], 
                    prompt=prompt,
                    negative_prompt=generateRandomNegative(),
                    seed=-1,
                    resize_mode= 0,
                    denoising_strength= denoising_strength,
                    sampler_name= sampler_index,
                    height=height,
                    width=width,
                    steps=steps,
                    batch_size= 8,
                    cfg_scale=cfg_scale,
                        script_name = "SD upscale",
                        script_args = ["",padding, upscaler,scale]
                    )

    
    r = response.image

    pnginfo = PngImagePlugin.PngInfo()
    pnginfo.add_text('parameters', resultOld.image.info["parameters"])
    response.image.info = resultOld.image.info
    r.save(outputimg2imgFull, pnginfo=pnginfo)

    return response

