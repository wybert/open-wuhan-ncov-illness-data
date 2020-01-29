from moviepy.editor import *
import os

path = "figs/"
img = []
for fileName in os.listdir(path):
    img.append(path + fileName)

print(img)
clips = [ImageClip(m).set_duration(2)
      for m in img]

concat_clip = concatenate_videoclips(clips, method="compose")

print("writing...")
# concat_clip.write_videofile("test.mp4", fps=24)

concat_clip.write_gif("circle.gif",fps=15)
