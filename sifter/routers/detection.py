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
from logic.detect import detect, batch_detect
# Models
from models.detection_models import DetectionPayload, DetectionResponse, DetectionBatchResponse, DetectionBatchPayload

router: APIRouter = APIRouter()

@router.post("/sift", response_model=List[DetectionResponse])
async def _detect(payload: DetectionPayload):
    """Detect route for the API"""

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

    response = [DetectionResponse(matches=boxes)]

    return response


@router.post("/sift/batch", response_model=List[DetectionBatchResponse])
async def _batch_detect(payload: List[DetectionBatchPayload]):
    """Detect route for the API"""

    try:
        frames = []
        for frame in payload:
            frames.append(
                np.array(Image.open(io.BytesIO(base64.b64decode(frame.frame))))
            )
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
        template = Image.open(io.BytesIO(base64.b64decode(payload[0].template)))
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
        boxes = batch_detect(frames, template, payload[0].threshold)
    except Exception as general_exception:
        print(general_exception)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(general_exception),
        )

    response = [DetectionBatchResponse(matches=boxes)]

    return response