import os, cv2
from glob import glob


images_folder = "data/text/test/images"
texts_folder = "runs/detect/exp7/labels"
assert os.path.exists(images_folder) and os.path.exists(texts_folder)

output = "data/text/test/blur"
if not os.path.exists(output):
    os.mkdir(output)


# * Blur function
def blur(src):
    ksize = 30
    roi = cv2.blur(src, (ksize, ksize))
    return roi


for tf in glob(f"{texts_folder}/*.txt"):
    image_path = tf.replace(texts_folder, images_folder)
    image_path = image_path.replace("txt", "jpg")
    if not os.path.exists(image_path):
        image_path = image_path.replace("jpg", "png")
    if not os.path.exists(image_path):
        print("Image is None about", tf)
        continue

    frame = cv2.imread(image_path)
    with open(tf, "r") as tf:
        lines = tf.readlines()

    # ? draw (blurring)
    for line in lines:
        if not line.startswith("0"):
            continue

        parts = line.rsplit("\n", 1)[0].split(" ")
        cx, cy, w, h = map(float, parts[1:5])
        sx, sy, fx, fy = map(
            int,
            [(cx - w / 2) * frame.shape[1], (cy - h / 2) * frame.shape[0], (cx + w / 2) * frame.shape[1], (cy + h / 2) * frame.shape[0]],
        )

        # ? draw (test)
        # frame = cv2.rectangle(frame, (sx, sy), (fx, fy), (255, 0, 0), 3)
        frame[sy:fy, sx:fx] = blur(frame[sy:fy, sx:fx])
    path = image_path.replace(images_folder, output)
    cv2.imwrite(path, frame)

#     output = cv2.resize(frame, (500, 500))
#     cv2.imshow("output", output)
#     cv2.waitKey(0)

# cv2.destroyAllWindows()
