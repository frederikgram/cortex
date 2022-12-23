""" Detection models for Response and Payload """

from pydantic import BaseModel
from typing import List


class DetectionResponse(BaseModel):
    """Response model for the detection API"""

    matches: List[dict]


class DetectionPayload(BaseModel):
    """Payload model for the detection API"""

    frame: str
    template: str
    threshold: float

class DetectionBatchPayload(BaseModel):
    """Payload batch model for the detection API"""

    frames: List[str]
    template: str
    threshold: float

class DetectionBatchResponse(BaseModel):
    """Response batch model for the detection API"""

    matches: List[List[dict]]