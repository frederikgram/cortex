
import cv2
import os
import time

import numpy as np
import cv2
import os
import time

from decouple import config
from typing import *


def download_video_youtube(url: str, file_loc: str):
    """ Download video from url and convert to frames
    
    Args:
        url (str): url of video to download

    Returns:
        frame (np.array): frame of video
            

    """

    print(url)

    try: 
        print("Downloading Youtube Video")
        os.system("youtube-dl -o " + file_loc + " -f mp4 " + url)
    except Exception as general_exception:
        print("Error downloading video")
        print(general_exception)
        raise general_exception
    return True


def get_frames(url: str, source: str = "youtube") -> List[np.array]:
    """ Download video from url and convert to frames
    
    Args:
        url (str): url of video to download

    Returns:
        frame (np.array): frame of video

    """
    

    file_loc = str(time.time()) + ".mp4"

    try:
        if source == "youtube":
            download_video_youtube(url, file_loc)


        cap = cv2.VideoCapture(file_loc)

        # Check if camera opened successfully
        if (cap.isOpened() == False):
            print("Error opening video stream or file")

        frames = list()

        # Convert video to frames
        while (cap.isOpened()):
            # Capture frame-by-frame
            ret, frame = cap.read()
            if ret == True:
                frames.append(frame)
            # Break the loop
            else:
                break

        # When everything done, release the video capture object
        cap.release()
    except Exception as general_exception:
        print("Error downloading video")
        print(general_exception)
        raise general_exception
    finally:
        # Remove video file
        if os.path.exists(file_loc):
            os.remove(file_loc)

    # Downscale all frames
    downscale_factor = int(config("DOWNSCALE_FACTOR", default=1))
    frames = [cv2.resize(frame, (frame.shape[1] // downscale_factor, frame.shape[0] // downscale_factor)) for frame in frames]


    return frames
