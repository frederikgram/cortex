""" """

import numpy as np
from pydantic import BaseModel
from typing import *
class FetcherRequest(BaseModel):
    url: str

class FetcherResponse(BaseModel):
    frames: List[str]