
from PIL import Image
import os

for f in os.listdir("tmp_plots"):
    im = Image.open(os.path.join("tmp_plots", f))
    assert im.size == (320+64, 240+48)
    im.crop((32,34,352,274)).save(os.path.join("plots", f))