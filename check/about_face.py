# ? 1번 (face) 찾기
import os
from glob import glob


base = "data/before/labels"
assert os.path.exists(base)

texts = glob(f"{base}/*.txt")
# print(texts)


for f in texts:
    with open(f, "r") as tf:
        lines = tf.readlines()

    text = ""
    for line in lines:
        if not line.startswith("1") or len(line) < 2:
            print(line)


# ? 1번 찾아 0번으로 바꾸기
import os
from glob import glob


base = "data/before/labels"
output = "data/text/test/faces"
assert os.path.exists(base) and os.path.exists(output)

texts = glob(f"{base}/*.txt")
# print(texts)

for f in texts:
    with open(f, "r") as tf:
        lines = tf.readlines()

    text = ""
    for line in lines:
        if not line.startswith("1") or len(line) < 2:
            continue
        line = line.replace("1 ", "0 ")
        text += line
    # print(text)

    if len(text) < 2:
        continue
    path = f.replace(base, output)
    with open(path, "w") as tf:
        tf.write(text[:-1])


# ? 1번 (face) 지우기
import os
from glob import glob


base = "data/text"
assert os.path.exists(base)

texts = glob(f"{base}/*/labels/*.txt")
print(texts)

for f in texts:
    with open(f, "r") as tf:
        lines = tf.readlines()

    text = ""
    for line in lines:
        if not line.startswith("0") or len(line) < 2:
            continue
        text += line

    if len(text) < 2:
        image = f.replace("labels", "images")
        try:
            image = image.replace("txt", "jpg")
            os.remove(image)
        except:
            image = image.replace("txt", "png")
            os.remove(image)
        os.remove(f)
    else:
        with open(f, "w") as tf:
            tf.write(text[:-1])


# ? 1번 바꾸기
import os
from glob import glob


base = "data/after/cocotext-v20/data"
assert os.path.exists(base)

texts = glob(f"{base}/*.txt")
# print(texts)


for f in texts:
    with open(f, "r") as tf:
        lines = tf.readlines()

    text = ""
    for line in lines:
        if not line.startswith("0") or len(line) < 2:
            print(line)
