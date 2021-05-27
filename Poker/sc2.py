# import os, tempfile, subprocess
# from PIL import Image

# def grab(bbox=None):
#     f, file = tempfile.mkstemp('.png')
#     os.close(f)
#     subprocess.call(['screencapture', '-x', file])
#     im = Image.open(file)
#     im.load()
#     os.unlink(file)
#     if bbox:
#         im = im.crop(bbox)
#     return im

# grab()

# from subprocess import call
# call(["screencapture", "screenshot.jpg"])

# os.system("screencapture screen.png")

import pyscreenshot

# fullscreen
# screenshot=pyscreenshot.grab()
# screenshot.show()

# part of the screen
screenshot=pyscreenshot.grab(bbox=(10,10,500,500))
# screenshot.show()

# save to file
screenshot.save('screenshot2.png')