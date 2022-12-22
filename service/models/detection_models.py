""" Detection models API """

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
