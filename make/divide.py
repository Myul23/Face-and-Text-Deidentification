# ? train / valid / test
import os
from glob import glob
from shutil import move

import numpy as np


base = "data/text"
assert os.path.exists(base)

train = os.path.join(base, "train")
valid = os.path.join(base, "valid")
test = os.path.join(base, "test")
for f in [train, valid, test]:
    if not os.path.exists(f):
        os.mkdir(f)


total = len(os.listdir(os.path.join(base, "labels")))
lengths = [0, int(total * 0.2), int(total * 0.1)]
lengths[0] = total - lengths[1] - lengths[2]
print(lengths)


for idx, target in enumerate([train, valid, test]):
    image_folder = os.path.join(target, "images")
    text_folder = os.path.join(target, "labels")
    for f in [image_folder, text_folder]:
        if not os.path.exists(f):
            os.mkdir(f)

    images = glob(f"{base}/images/*")
    randoms = np.random.choice(images, size=lengths[idx], replace=False)
    for image in randoms:
        text = image.replace("images", "labels")
        if ".jpg" in text:
            text = text.replace("jpg", "txt")
        else:
            text = text.replace("png", "txt")
        # print(image, text)

        image_path = image.replace(base, target)
        text_path = text.replace(base, target)
        # print(image, image_path, sep="\t")
        # print(text, text_path, sep="\t")
        move(image, image_path)
        move(text, text_path)
    print(target, "finished")
