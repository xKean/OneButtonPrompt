import json
import requests
import io
import base64
import uuid
from PIL import Image, PngImagePlugin
import webuiapi



def call_extras(oldResult, randomModel = 'rmadaMergeSD21768_v70'):

    image = oldResult.image
    #rest of prompt things
    upscaling_resize = "2"
    upscaler_1 = "4x-UltraSharp"
    upscaler_2 = "R-ESRGAN 4x+"
    
    #params to stay the same
    outputextrasfolder = 'C:/automated_output/extras/'
    outputextrasilename = str(uuid.uuid4())
    outputextraspng = '.png'
    outputextrasFull = '{}{}{}'.format(outputextrasfolder,outputextrasilename,outputextraspng)


    api = webuiapi.WebUIApi(host='127.0.0.1',
                        port=7860,
                        sampler='DPM++ 2M Karras',
                        steps="35")
    
    api.util_set_model(randomModel)
    


    result = api.extra_single_image( image=image,
                                    resize_mode=0,
                                    show_extras_results= False,
                                    upscaler_1= upscaler_1,
                                    upscaling_resize= upscaling_resize,
                                    gfpgan_visibility= 0,
                                    codeformer_visibility= 0.15,
                                    codeformer_weight= 0.1,
                                    upscaling_crop= False,
                                    upscaler_2= upscaler_2,
                                    extras_upscaler_2_visibility= 0.5,
                                    upscale_first= True
    )
    
    r = result.image

    pnginfo = PngImagePlugin.PngInfo()
    pnginfo.add_text('parameters', oldResult.image.info["parameters"])
    r.save(outputextrasFull, pnginfo=pnginfo)

    return result