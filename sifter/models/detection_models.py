""" Detection models for Response and Payload """

from pydantic import BaseModel
from typing import List, Dict


class DetectionResponse(BaseModel):
    """ Response model for the detection API"""
    
    bounding_box: Dict[str, int]
    confidence: float
    num_matches: int
    num_good_matches: int


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
    matches: List[DetectionResponse]