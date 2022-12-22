
# Cortex

Cortex is a tool for estimating the number of impressions advertisements have received during live broadcasts of esports matches. It is built on top of the [OpenCV](https://opencv.org/) computer vision library and uses the [SIFT](https://en.wikipedia.org/wiki/Scale-invariant_feature_transform) algorithm to detect and match logos in images. 

## Architecture
Cortex is built as a Docker deployable microservice using a Python & FastAPI based backend, and a NodeJS based frontend. The backend is responsible for the image processing and the frontend is responsible for the user interface.  

## What is SIFT?
Scale-invariant feature transform, also known as SIFT, is a computer vision algorithm used to detect, describe, and match local features in images. SIFT works by detecting keypoints in an image and then computing a feature vector for each keypoint. The feature vectors are then compared to find matching keypoints between images. SIFT is a patented algorithm, but the patent has expired and the algorithm is now freely available.

Using SIFT, we can find matching keypoints between two images. We can then use the matching keypoints to find the homography between the two images. The homography describes how to transform points in one image to points in the other image.

In the context of this application, SIFT allows us to detect logos or other objects in an image, invariant of scale, rotation, and translation. Combined with its robustness to noise - such as shadows, blurring, or in-game effects such as blood or smoke - we get a very powerful tool which in this project is used to estimate how many impressions advertisements have received during live broadcasts of esports matches.

## Getting Started

### Starting the Backend
The backend is a Python & FastAPI based microservice. It is built using Docker and can be started using the following command:

```bash
docker build -t cortex_backend
docker run -p 8000:8000 cortex_backend
```

### Starting the Frontend
WARNING: The frontend is currently under development and is not yet functional.

### Kubernetes
The backend can also be deployed to Kubernetes using the provided `kubernetes.yaml` file. The frontend is not yet supported in Kubernetes.

This is the prefered way as this automatically sets up DNS between the frontend and backend. And it also allows for easy scaling of the backend.e:

### Deploying to Google Cloud using Terraform
Work in progress.

## Examples

As can be seen in the examples below, Cortex is able to detect logos in images, even when they are rotated, scaled, or obscured by other objects.

![](resources/root_example.png?raw=true)
![](resources/betway_example.png?raw=true)