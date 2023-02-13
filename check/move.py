import os
from glob import glob
from shutil import copy


base = "data/after/cocotext-v20/data"
output = "data/text"
assert os.path.exists(base) and os.path.exists(output)

image_folder = os.path.join(output, "images")
text_folder = os.path.join(output, "labels")
if not os.path.exists(image_folder):
    os.mkdir(image_folder)
if not os.path.exists(text_folder):
    os.mkdir(text_folder)


for image in glob(f"{base}/*.jpg"):
    new_path = image.replace(base, image_folder)
    copy(image, new_path)
for text in glob(f"{base}/*.txt"):
    new_path = text.replace(base, text_folder)
    copy(text, new_path)
