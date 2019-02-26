import matplotlib.pyplot as plt
from matplotlib.text import Text
from ast import literal_eval
from itertools import takewhile

# To come in as args
xWidth = 60
fps = 30
fn = "frame_lists\\cavs_agent_out.py"
yLimit = 4

def textFor(x, _):
    x = x / fps
    if int(x) == x:
        return str(int(x))
    else:
        s = str(x)
        return s[s.index("."):]

# Don't give me any 29.19 nonsense
assert fps % 5 == 0
fifthSec = fps // 5


# Probably just constants
yPad = 0.4
smoothHalfWidth = fifthSec
smoothWidth = 2 * smoothHalfWidth

# Read file and re-calculate diffs
with open(fn,"r") as fs:
    df = literal_eval(fs.read())




for xFrame in range(df[-1]):
    ax = plt.axes()

    # Put a vertical through the current value, background
    plt.plot([xFrame, xFrame], [1-2*yPad, yLimit + 2*yPad], color="grey", lineWidth = 3)


    # Also plot a thin moving average line
    # Bit tricky to compute

    diffs = [b - a for a,b in zip(df, df[1:])]
    i = 0
    firstSegment = list(takewhile(lambda v : v < df[0] + smoothWidth, df))
    j = len(firstSegment) - 1
    score = sum(diffs[k]**2 for k in range(j))
    score += diffs[j] * (df[0] + smoothWidth - df[j])

    xs = []
    ys = []
    for x in range(df[0], df[-1] - smoothWidth):
        xs.append(x + smoothHalfWidth)
        ys.append(score / smoothWidth)
        
        # Losing a frame at i, and advancing i if necessary
        score -= diffs[i]
        if df[i+1] == x+1:
            i += 1

        # Advancing j if necessary, and gaining a frame
        # This way around because [x+smoothWidth] = [(x+1) + (smoothWidth-1)] so is just gained next time
        if df[j+1] == x+smoothWidth:
            j += 1
        score += diffs[j]
        
        
    plt.plot(xs,ys, color='xkcd:salmon', linewidth = 2)



    # Considered drawing #video-frames since last drawn frame, but that was too spiky
    # Instead, for each video frame, draw the #video-frames that the game-frame lasted for
    #   This means the graph is flat wherever the image is unchanged
    # It can still kick 2-1-2-1-2-1 but I think that's good

    xs = []
    ys = []

    for n, m in zip(df, df[1:]):
        xs.append(n)
        step = m-n
        ys.append(step)
        if n < m - 1:
            xs.append(m-1)
            ys.append(step)
            
    plt.plot(xs, ys, color='xkcd:darkgreen', linewidth = 5)


        

        



    # Y limits and ticks
    ys = list(range(0, yLimit+1))
    plt.ylim([1-yPad,yLimit+yPad])
    plt.yticks(ys, [str(x) for x in ys], fontsize = "large")


    # X limits and ticks : every 0.2 is common to PAL / NTSC 25/30fps

    xMin = xFrame - (xWidth // 2)
    xMax = xFrame + (xWidth // 2)
    plt.xlim([xMin, xMax])

    tickMarks = list(range(xMin + (-xMin % fifthSec), xMax - (xMax % fifthSec) + 1, fifthSec))

    ax.xaxis.set_major_locator(plt.MultipleLocator(fps))
    ax.xaxis.set_minor_locator(plt.MultipleLocator(fifthSec))
    ax.xaxis.set_major_formatter(plt.FuncFormatter(textFor))

    ax.tick_params(labelsize="xx-large")

    width, height = plt.gcf().get_size_inches() # should be 4:3
    # Aiming for 320x240, but I can't find a way to still have a bounding box, but it be more minimal.
    # So currently we aim above (384 x 288?) and then crop in clean_plots.py
    plt.savefig(r'tmp_plots\plot_{:06}'.format(xFrame), dpi=(320+64)/width)


    if xFrame % fps == 0:
        print("{} seconds..".format(xFrame // fps))

    plt.clf()
