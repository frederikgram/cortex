""" Middleware for detecting the template in the frame """

import numpy as np
from service.logic.sift import analyze_frame


def detect(frame: np.array, template: np.array, threshold: np.array):
    """Detects the template in the frame"""

    try:
        result = analyze_frame(frame, template, threshold)
    except Exception as general_exception:
        print(general_exception)
        raise general_exception

    return result
