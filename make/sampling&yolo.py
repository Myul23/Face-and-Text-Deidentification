# import os
# from glob import glob
# import cv2


# base = "data/after/cocotext-v20/data"
# output = "data/after/cocotext-v20/sampling"
# for f in glob(f"{base}/*.jpg"):
#     image = cv2.imread(f)

#     dst = cv2.resize(image, (image.shape[1] // 3, image.shape[0] // 3))
#     with open(f.replace("jpg", "txt"), "r") as tf:
#         lines = tf.readlines()
#     text = ""
#     for l in lines:
#         temp = list(map(float, l.split(" ")))
#         t = map(round, [temp[0], temp[1] * dst.shape[1], temp[2] * dst.shape[0], temp[3] * dst.shape[1], temp[4] * dst.shape[0]])
#         text += " ".join(list(map(str, t))) + "\n"
#     # print(text[:-1])

#     path = os.path.join(output, f.rsplit("\\", 1)[1])
#     cv2.imwrite(path, dst)
#     with open(path.replace("jpg", "txt"), "w") as tf:
#         tf.write(text[:-1])


# ? make ones
# import os
# from glob import glob
# import cv2


# base = "data/after/cocotext-v20/data"
# output = "data/after/cocotext-v20/bigones"
# if not os.path.exists(output):
#     os.mkdir(output)

# times = 3
# for f in glob(f"{base}/*.jpg"):
#     image = cv2.imread(f)
#     with open(f.replace("jpg", "txt"), "r") as tf:
#         lines = tf.readlines()

#     for idx, l in enumerate(lines):
#         temp = list(map(float, l.split(" ")))
#         t = [temp[1] * image.shape[1], temp[2] * image.shape[0], temp[3] * image.shape[1], temp[4] * image.shape[0]]
#         t = list(map(int, [temp[0], t[0] - t[2] / 2, t[1] - t[3] / 2, t[2], t[3]]))

#         try:
#             img = cv2.resize(image[t[2] : t[2] + t[4], t[1] : t[1] + t[3], :], dsize=(0, 0), fx=times, fy=times)
#             text = " ".join(list(map(str, [t[0], 0, 0, t[3] * times, t[4] * times])))

#             # save
#             name = f.rsplit("\\", 1)[1].rsplit(".", 1)[0] + f"_{idx}.jpg"
#             path = os.path.join(output, name)
#             cv2.imwrite(path, img)
#             with open(path.replace("jpg", "txt"), "w") as tf:
#                 tf.write(text)
#         except cv2.error:
#             pass


# ? make yolo format
import os
from glob import glob
from shutil import move

import cv2


base = "data/before"
output = "data/before"
output_images = os.path.join(output, "images")
output_texts = os.path.join(output, "labels")
if not os.path.exists(output_images):
    os.mkdir(output_images)
if not os.path.exists(output_texts):
    os.mkdir(output_texts)


for t in glob(f"{base}/*.txt"):
    image = glob(t.replace("txt", "png"))
    if len(image) < 1:
        continue

    img = cv2.imread(image[0])
    with open(t, "r") as tf:
        lines = tf.readlines()

    text = ""
    for l in lines:
        temp = list(map(int, l.split(" ")))
        temp = list(map(int, [temp[0], temp[1] + temp[3] / 2, temp[2] + temp[4] / 2, temp[3], temp[4]]))
        temp = [temp[0], temp[1] / img.shape[1], temp[2] / img.shape[0], temp[3] / img.shape[1], temp[4] / img.shape[0]]
        text += " ".join(list(map(str, temp))) + "\n"

    name = t.rsplit("\\", 1)[1]
    path = os.path.join(output_images, name.replace("txt", "png"))
    move(image[0], path)
    path = os.path.join(output_texts, name)
    with open(path, "w") as tf:
        tf.write(text[:-1])
