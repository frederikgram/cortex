""""""

import os
import cv2
import json
import argparse
from typing import Iterable, Tuple
from sift import analyze_frame
import numpy as np
import subprocess


def download_vod(video_id: str, path_to_output_dir: str) -> str:
    """
    Downloads a Twitch VOD using twitch-dl
    https://github.com/ihabunek/twitch-dl

    Parameters:
        video_id (str): ID of the video to download
        path_to_output_dir (str): Path to the output directory to save the video to

    Return:
        str: Path to the downloaded video"""

    if not os.path.isdir(path_to_output_dir):
        os.mkdir(path_to_output_dir)
    subprocess.call(
        [
            "twitch-dl",
            "download",
            "--quality",
            "720p",
            "-o",
            f"{os.path.join(path_to_output_dir, video_id)}.mp4",
            "-f",
            "mp4",
            f"{video_id}",
        ]
    )
    return os.path.join(path_to_output_dir, f"{video_id}.mp4")


def to_grayscale_frames(path_to_video: str) -> Iterable[Tuple[bool, np.ndarray]]:
    """
    Convert a video to a series of grayscale frames using OpenCV

    Parameters:
        path_to_video (str): Path to the video to convert

    Returns:
        Iterable: Iterable of grayscale frames
    """

    video_capture = cv2.VideoCapture(path_to_video)
    success, image = video_capture.read()
    while success:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        yield gray
        success, image = video_capture.read()


def pipe(
    template_path: str = None,
    video_id: str = None,
    path_to_output_dir: str = ".",
    verbose=True,
    path_to_vod: str = None,
    debug=True
):
    """
    Parameters:
        template_path (str): Path to the template image to find in the video
        video_id (str): ID of the video to download
        path_to_output_dir (str): Path to the output directory to save the video to
        verbose (bool): Whether or not to print the output of the program
        path_to_vod (str): Path to the video to analyze if it has already been downloaded
        debug (bool): Whether or not to show the frames being analyzed

    Returns:
        [x1,y1,x2,y2]: bottom left and top right coordinates of the template in the frame

    """

    bounding_boxes = dict()

    if video_id == None:
        path_to_vod="root_frame.jpg"

    if template_path == None:
        template_path = "root.png" # Default template

    # If no path to the VOD is given, download it
    if path_to_vod == None:
        print(f"Downloading Twitch VOD: {video_id}")

        if os.path.isfile(f"{video_id}.mp4"):
            os.remove(f"{video_id}.mp4")

        path_to_vod = download_vod(video_id, path_to_output_dir)
        print(path_to_vod)

        if not os.path.isfile(f"{os.path.join(path_to_output_dir,video_id)}.mp4"):
            raise Exception("VOD Download Failed")

    elif not os.path.isfile(path_to_vod):
        raise Exception("Given VOD does not exist")
    else:
        print(f"Using given VOD: {path_to_vod}")


    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)

    frame_generator = to_grayscale_frames

    # Start Scale Invariant Feature Detection
    print(f"Started SIFT Analysis using template: {template_path}")
    
    # Video to Frame Conversion
    for enum, frame in enumerate(frame_generator(path_to_vod)):


        if verbose:
            print(f"Analyzing frame: {enum}")

        try:
            img, bounding_box = analyze_frame(frame, template)

            if debug:
                cv2.imshow("frame", img)
                cv2.waitKey(0)

        except KeyboardInterrupt:
            # Make script interuptable, without losing the data
            # that has been analyzed up to the point of interruption
            break
        except Exception as e:
            print(str(e))
            # Naive Exception, CV2 is a mess, cannot be explicit.
            bounding_box = None

        if not bounding_box == None and len(bounding_box) > 0:
            if verbose:
                print("Found bounding box")
            bounding_boxes[str(enum)] = bounding_box


if __name__ == "__main__":
    pipe(debug=True, verbose=True)
