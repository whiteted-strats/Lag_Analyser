#!/usr/local/bin/python3
# Adapted from http://tsaith.github.io/combine-images-into-a-video-with-python-3-and-opencv-3.html
# Mostly stepping through the plots more carefully.

import cv2
import argparse
import os

# Construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", required=False, default='output.mp4', help="output video file")
ap.add_argument("-fps", "--framespersecond", required=False, default = '30.0', help="output frames per second, float")
ap.add_argument("-dir", "--directory", required=False, default = ".", help="source directory")
args = vars(ap.parse_args())

# Arguments
output = args['output']
fps = float(args['framespersecond'])

images = []
for f in os.listdir(args['directory']):
    assert f.startswith("plot_") and f.endswith(".png"), "Doesn't look like you passed the plot folder"
    n = int(f[5:-4])
    images.append((n, f))

images.sort()

# Determine the width and height from the first image
image_path = os.path.join(args['directory'], images[0][1])
frame = cv2.imread(image_path)
cv2.imshow('video',frame)
height, width, channels = frame.shape

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'mp4v') # Be sure to use lower case
out = cv2.VideoWriter(output, fourcc, fps, (width, height))

for i, (n, image) in enumerate(images):
    assert i == n
    
    image_path = os.path.join(args['directory'], image)
    frame = cv2.imread(image_path)

    out.write(frame) # Write out frame to video. Will fail silently if it's the wrong resolution

    cv2.imshow('video',frame)
    if (cv2.waitKey(1) & 0xFF) == ord('q'): # Hit `q` to exit
        break

# Release everything if job is finished
out.release()
cv2.destroyAllWindows()

print("The output video is {}".format(output))
