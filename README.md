
# Cortex

Cortex is a ... (TODO)


### What is SIFT?
Scale-invariant feature transform, also known as SIFT, is a computer vision algorithm used to detect, describe, and match local features in images. SIFT works by detecting keypoints in an image and then computing a feature vector for each keypoint. The feature vectors are then compared to find matching keypoints between images. SIFT is a patented algorithm, but the patent has expired and the algorithm is now freely available.

Using SIFT, we can find matching keypoints between two images. We can then use the matching keypoints to find the homography between the two images. The homography describes how to transform points in one image to points in the other image.

In the context of this application, SIFT allows us to detect logos or other objects in an image, invariant of scale, rotation, and translation. Combined with its robustness to noise - such as shadows, blurring, or in-game effects such as blood or smoke - we get a very powerful tool which in this project is used to estimate how many impressions advertisements have received during live broadcasts of esports matches.

### Architecture
(TODO)
### Getting Started
(TODO)

![](resources/root_example.png?raw=true)
![](resources/betway_example.png?raw=true)