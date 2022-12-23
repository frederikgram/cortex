""" Logic for the API routes """


# Typing Dependencies
from typing import List

# FastApi Dependencies
from fastapi import APIRouter, Body, Depends, HTTPException, Request, status

from logic.frames import get_frames
from models.fetcher_models import FetcherRequest, FetcherResponse

import base64
import cv2


router: APIRouter = APIRouter()


@router.post("/get_frames", response_model=FetcherResponse)
async def get_frames_route(payload: FetcherRequest = Body(...)):
    """ Download video from url and convert to frames

    Args:
        url (str): url of video to download

    Returns:
        frame (np.array): frame of video

    """

    # Get url from payload
    url: str = payload.url
    

    try:
        frames = get_frames(url, "youtube")
    except Exception as general_exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error downloading video",
        ) from general_exception


    # Convert to base64
    frames = [base64.b64encode(cv2.imencode(".jpg", frame)[1]).decode() for frame in frames]

    return FetcherResponse(frames=frames)