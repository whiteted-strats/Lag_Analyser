# Requires Python 3.6, else the entire subprocess module has probably changed.
# Needs access to ffmpeg ffprobe (windows builds @ https://ffmpeg.zeranoe.com/builds/ )
# Only built for windows

from imageio import imread
import numpy as np
import os
from subprocess import getoutput
import matplotlib.pyplot as plt
import sys


## Originally 1. Tested on the start of a caverns agent run.
##  This found 3 false positives with diff = 1.03, 1.77, 1.81
##  The min value among true positives was 2.93. So 2 seems sensible.
meanSqThreshold = 2

ffmpegOutFile = "ffmpeg_out.txt"


def formatSeconds(s):
    hours = s // 3600
    s = s % 3600
    mins = s // 60
    s = s % 60
    if hours > 0:
        return "{:02}:{:02}:{:02}".format(hours, mins, s)
    elif mins > 0:
        return "{:02}:{:02}".format(mins, s)
    else:
        return "{:02}".format(s)
    
def formatTimestamp(fps, secs, frames):
    frac = float(frames) / fps
    frac = str(frac)
    assert frac.startswith("0.")    # even 0 will be 0.0
    frac = frac[1:7] # 5 dp, not rounding the last

    return formatSeconds(secs) + frac

def getDuration(fn, fps):
    probe_cmd = "ffprobe -i {}".format(fn)
    output = getoutput(probe_cmd)   # This has changed so often in Python 3

    marker = "Duration: "

    start = output.index(marker)
    assert start != -1, "Unable to read duration out of start"
    start += len(marker)
    end = output.index(",", start)
    
    duration = output[start:end]
    print("Duration read as {}".format(duration))
    hours, mins, float_sec = duration.split(":")
    frames = round(float(float_sec) * fps)
    secs = frames // fps
    frames = frames % fps

    secs += int(mins) * 60 + int(hours) * 3600
    return (secs, frames)



def main():
    if len(sys.argv) != 4:
        print("Usage: {} fps input.mp4 output.py".format(sys.argv[0]))
        return
        
    fps = int(sys.argv[1])
    filename = sys.argv[2]
    outputFile = sys.argv[3]


    if not os.path.exists("frames"):
        os.makedirs("frames")

    secs, frames = getDuration(filename, fps)
    frames += secs * fps
    print("Total of {} frames".format(frames))

    # y to overwrite
    cmd = "ffmpeg -y -r {} -i {} -qscale:v 3 \"frames\\frame_%06d.jpg\""
    cmd = cmd.format(fps, filename)

    print("Executing:")
    print(cmd)
    ffmpegOut = getoutput(cmd)
    with open(ffmpegOutFile, "w") as fs:
        fs.write(ffmpegOut)


    print("[Successfully] broken into frames.")

    # ============================================

    print("Computing differences (takes a little longer)..")
    fs = "frames\\frame_{:06}.jpg"
    prev = imread(fs.format(1))
    msds = []
    drawnFrames = []

    for i in range(2, frames-1):
        try:
            curr = imread(fs.format(i))
        except FileNotFoundError:
            frames = i + 1
            print("Only {} frames were output by ffmpeg.".format(frames))
            print("ffmpeg's output has been written to {}".format(ffmpegOutFile))
            print("Continuing..")
            break

        diff = np.square(curr - prev).mean(axis=None)
        prev = curr

        msds.append(diff)
        if diff > meanSqThreshold:
            drawnFrames.append(i-1)

    print("Finished. Writing to output..")
    with open(outputFile, "w") as fs:
        fs.write(str(drawnFrames))

    intervals = [b-a for a,b in zip(drawnFrames, drawnFrames[1:])]

    print("Written. Drawing interval plot :)")
    plt.plot([x / fps for x in drawnFrames[:-1]], intervals)
    plt.show()


if __name__ == "__main__":
    main()
