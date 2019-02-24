# Lag_Analyser
A script built on ffmpeg for determining the lag frames in a run of GE / PD
Requires ffmpeg and ffprobe (https://www.ffmpeg.org/), Windows builds can be found @ https://ffmpeg.zeranoe.com/builds/
Also requires a few common python libraries: see the top of the file

Currently outputs:
* A python list of video-frame numbers where it has detected GE / PD has drawn a new frame
* Each of the frames pulled out by ffmpeg, in /frames/
* A graph (at the end of execution) of the number of video frames between drawn game-frames, against time in seconds. So #lag frames + 1

Potential future features:
* Also output a (small) video of the lag graph. This could then be put next to the original video with simple video editting software.
* Automated reading of the timer in PD, and syncing with that

Tested carefully on the start of Caverns agent and (after a tweak) it's entirely accurate on the first 5s.
Tested sporadically elsewhere in the run and it seems good.
