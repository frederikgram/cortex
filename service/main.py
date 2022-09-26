""" Entrypoint for the application. """

import io
import cv2
import base64 
import numpy as np
import base64
import requests
import PIL

from fastapi import FastAPI, Request
from PIL import Image

from .sift import analyze_frame

app = FastAPI()

@app.get("/")
async def cortex(info: Request):

    req_info = await info.json()

    if req_info['template'] == None:
        return "No template was provided"
    
    if req_info['frame'] == None:
        return "No frame was provided"
    
    try: 
        frame = Image.open(io.BytesIO(base64.b64decode(req_info['frame'])))
        frame= np.array(frame)
    except PIL.UnidentifiedImageError:
        return "Given frame is not a valid image"

    try: 
        template = Image.open(io.BytesIO(base64.b64decode(req_info['template'])))
        template = np.array(template)
    except PIL.UnidentifiedImageError:
        return "Given template is not a valid image"

    try:
        boxes = analyze_frame(frame, template)
    except Exception as e:
        return str(e)

    return boxes

