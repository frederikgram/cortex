""" Logic for the API routes """

# Detection Dependencies
import base64
import binascii
import io

import numpy as np
import PIL
from PIL import Image, ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True

# Typing Dependencies
from typing import List
# FastApi Dependencies
from fastapi import APIRouter, Body, Depends, HTTPException, Request, status
# Logic
from logic.detect import detect
# Models
from models.detection_models import DetectionPayload, DetectionBatchPayload, DetectionResponse, DetectionBatchResponse

router: APIRouter = APIRouter()

@router.post("/sift", response_model=DetectionResponse)
async def _detect(payload: DetectionPayload):
    """ Detect route for the API """

    try:
        frame = Image.open(io.BytesIO(base64.b64decode(payload.frame)))
        frame = np.array(frame)
    except (binascii.Error, PIL.UnidentifiedImageError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Given frame is not a valid image",
        )
    except Exception as general_exception:
        print(general_exception)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(general_exception),
        )

    try:
        template = Image.open(io.BytesIO(base64.b64decode(payload.template)))
        template = np.array(template)
    except (binascii.Error, PIL.UnidentifiedImageError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Given template is not a valid image",
        )

    except Exception as general_exception:
        print(general_exception)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(general_exception),
        )

    try:
        boxes = detect(frame, template, payload.threshold)
    except Exception as general_exception:
        print(general_exception)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(general_exception),
        )

    response = DetectionResponse(
        bounding_box=boxes["bounding_box"],
        confidence=boxes["confidence"],
        num_matches=boxes["num_matches"],
        num_good_matches=boxes["num_good_matches"],
    )

    return response
