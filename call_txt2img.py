import json
import os
import requests
import io
import base64
import uuid
import webuiapi
from PIL import Image, PngImagePlugin
from aesthetic import aestheticscorer

from random_functions import generateRandomNegative

def call_txt2img(passingprompt,ratio,upscale,debugmode, randomModel = 'rmadaMergeSD21768_v70'):

    #set the prompt!
    prompt = passingprompt
    foundgood = False
    negative_prompt = generateRandomNegative()


    #rest of prompt things
    sampler_index = 'DPM++ 2M Karras'
    steps = "35"
    if(debugmode==1):
        steps="10"
    cfg_scale = "7"

    #size
    if(ratio=='wide'):
        width = "768"
        height = "512"
    elif(ratio=='portrait'):
        width = "512"
        height = "768"
    elif(ratio=='ultrawide'):
        width = "1280"
        height = "360"
    else:
        width = "768"
        height = "768"
    #upscaler
    enable_hr = upscale
    if(debugmode==1):
        enable_hr="False"
    denoising_strength = "0.4"
    hr_scale = "2"
    hr_upscaler = "4x-UltraMix_Balanced"
    hr_second_pass_steps = str(round(int(steps)/2))

    

    #params to stay the same
    outputTXT2IMGfolder = 'C:/automated_output/txt2img/'
    outputTXT2IMGfilename = str(uuid.uuid4())
    outputTXT2IMGpng = '.png'
    outputTXT2IMGFull = '{}{}{}'.format(outputTXT2IMGfolder,outputTXT2IMGfilename,outputTXT2IMGpng)
    outputTXT2IMGtxtfolder = 'C:/automated_output/prompts/'
    outputTXT2IMGtxt = '.txt'
    outputTXT2IMGtxtFull = '{}{}{}'.format(outputTXT2IMGtxtfolder,outputTXT2IMGfilename,outputTXT2IMGtxt)

    api = webuiapi.WebUIApi(host='127.0.0.1',
                            port=7860,
                            sampler=sampler_index,
                            steps=steps)
    api.util_set_model(randomModel)
    if randomModel == "revAnimated_v122" or "dreamshaper_5BakedVae":
        apiOptions = api.get_options()
        apiOptions["CLIP_stop_at_last_layers"] = 2
        api.set_options(apiOptions)
    
    runs = 0
    goodNumber = 7
    overallRuns = 0
    averageScoreLast5 = 0
    bestResult = 0
    bestResultScore = 0
    while foundgood == False: 

        response = api.txt2img(
                        prompt=prompt,
                        negative_prompt=negative_prompt,
                        seed=-1,
                        sampler_name= sampler_index,
                        height=height,
                        width=width,
                        steps=steps,
                        
                        cfg_scale=cfg_scale,
                            enable_hr=enable_hr,
                            hr_scale=hr_scale,
                            hr_upscaler=hr_upscaler,
                            denoising_strength=denoising_strength,
                            hr_second_pass_steps = hr_second_pass_steps
                        )


        r = response.image


        pnginfo = PngImagePlugin.PngInfo()
        pnginfo.add_text('parameters', r.info["parameters"])
        r.save(outputTXT2IMGFull, pnginfo=pnginfo)
        score = aestheticscorer.aesthetic_score(outputTXT2IMGFull)
        
        averageScoreLast5 += score
        if score >= goodNumber or debugmode == 1:
                
            foundgood = True
        else:
            if runs == 10:
                goodNumber -= 0.5
                runs = 0
                print("Reduced difficulty to "+str(goodNumber))
            os.remove(outputTXT2IMGFull)
            runs +=1
            overallRuns +=1

            if(overallRuns % 10 == 0 and not overallRuns == 0 and averageScoreLast5 < 55):
                return ""
            

            
            if overallRuns == 25:
                return bestResult
            
            if overallRuns == 1:
                bestResult = response
                bestResultScore = score

            if(overallRuns > 1):
                if bestResultScore < score:
                    bestResultScore = score
                    bestResult = response
                


    if(bestResultScore > score):
        return bestResult
    return response