# Lag_Analyser & Video generator
A script built on ffmpeg for determining the lag frames in a run of GE / PD, and further tool built on OpenCV for creating a video of the lag graph.
Analysis requires ffmpeg and ffprobe (https://www.ffmpeg.org/), Windows builds can be found @ https://ffmpeg.zeranoe.com/builds/
Also requires a few common python libraries: see the top of the file.
The video generator requires opencv (https://opencv.org/) installed as a Python library. Also requires matplotlib and PIL.

Currently outputs:
* A python list of video-frame numbers where it has detected GE / PD has drawn a new frame
* Each of the frames pulled out by ffmpeg, in /frames/
* After running make_plots -> clean_plots -> render_video (and maybe creating the plots, tmp_plots folders) it will output a 320x240 video of the lag graph. Generating the graph takes a little while atm.

Potential future features:
* Cleverer comparison of frames, accepting a small change if it is contained to one area: for instance note that Bond animating in the outro is thought to be 1 frame.
* Automated reading of the timer in PD, and syncing with that
* A bit less slow..

Tested carefully on the start of Caverns agent and (after a tweak) it's entirely accurate on the first 5s.
Tested sporadically elsewhere in the run and it seems good.
SAMPLE RUN : https://youtu.be/pXqxylSmQaQ
