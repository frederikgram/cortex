""" This module contains the SIFT algorithm for template matching. """

import numpy as np
import cv2 as cv
import cv2 as cv2


def analyze_frame(frame, template, threshold=0.1):
    """ Attempts to perform sub-image template matching on the frame and template using the Scale-Invariant Feature Transform (SIFT) algorithm.
    
    Args:
        frame (str): The frame to analyze.
        template (str): The template to search for in the frame.
        threshold (float): The threshold for the number of matches to be considered a match.

    Returns:
        List[dict]: A list of bounding boxes and confidence scores for each match.

    """

    img1 = template
    img2 = frame


    # Initiate SIFT detector
    sift = cv.SIFT_create()
    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(img1,None)
    kp2, des2 = sift.detectAndCompute(img2,None)
    
    # BFMatcher with default params
    bf = cv.BFMatcher()
    matches = bf.knnMatch(des1,des2,k=2)
    # Apply ratio test
    good = []
    for m,n in matches:
        if m.distance < threshold*n.distance:
            good.append(m)

    good = sorted(good, key = lambda x:x.distance)

    src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1,1,2)
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1,1,2)
    M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
    matchesMask = mask.ravel().tolist()
    h,w = img1.shape[:2]
    pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)

    dst = cv2.perspectiveTransform(pts,M)
    dst += (w, 0)  # adding offset

    response = {
        "bounding_box": 
            {
                "x": int(dst[0][0][0]),
                "y": int(dst[0][0][1]),
                "width": int(dst[2][0][0] - dst[0][0][0]),
                "height": int(dst[2][0][1] - dst[0][0][1]),
            },
        "confidence": len(good) / len(matches),
        "num_matches": len(matches),
        "num_good_matches": len(good),

    }
    
    return response