import os
from glob import glob

import numpy as np
import random
import cv2


# 불러오기
images1 = "data/after/pedestrian-detection/Train/JPEGImages"
images2_base = "data/after/cocotext-v20/bigones"

texts1 = "data/after/pedestrian-detection/Train/yolo"
texts2 = "data/after/cocotext-v20/bigones"

output = "data/before"
images2 = glob(f"{images2_base}/*.jpg")


for i, image in enumerate(os.listdir(images1)):
    text1 = glob(f"{texts1}/{image.rsplit('.', 1)[0]}.txt")
    if len(text1) < 1:
        continue

    # TODO select base image, text image
    # 여기서 img1이랑 text를 for문 밖에서 저장하는 방식으로 하면 1 to 10개로 이미지에 붙이는 걸 볼 수 있음.
    # 나아가 save 하는 걸 for문 밖으로 빼서 여러 개 넣고 저장할 수 있음.
    for idx in range(10):
        try:
            img1 = cv2.imread(os.path.join(images1, image))
            path = np.random.choice(images2)
            img2 = cv2.imread(path)

            # TODO image에 따라갈 Bbox masking
            # text image가 확실히 작을 때
            mask1 = np.zeros((img1.shape[0], img1.shape[1]), np.uint8)
            mask2 = np.zeros((img2.shape[0], img2.shape[1]), np.uint8)
            # print(mask2.shape, img2.shape)

            text2 = glob(path.replace(images2_base, texts2).rsplit(".", 1)[0] + ".txt")
            # if len(text2) < 1:
            #     continue
            with open(text2[0], "r") as f:
                data = f.readlines()
            for t in data:
                if len(t) < 1:
                    continue

                # 원 크기 yolo format 가정
                temp = list(map(int, t.split(" ")[1:]))
                # print(temp, mask2.shape, np.ones((temp[3], temp[2]), np.uint8).shape)
                mask2[temp[1] : temp[1] + temp[3], temp[0] : temp[0] + temp[2]] = np.ones((temp[3], temp[2]), np.uint8)

            # TODO 위치 정하기
            minx = img2.shape[1] * 0.2
            maxx = img1.shape[1] - img2.shape[1] * 0.8
            miny = img2.shape[0] * 0.2
            maxy = img1.shape[0] - img2.shape[0] * 0.8
            minx, maxx, miny, maxy = map(round, [minx, maxx, miny, maxy])
            posx = random.randint(-minx, maxx)
            posy = random.randint(-miny, maxy)
            # print(minx, maxx, miny, maxy, posx, posy)

            targetx, width = 0, img2.shape[1]
            if posx < 0:
                targetx = -posx
                posx = 0
                width -= targetx
            elif posx > img1.shape[1] - img2.shape[1]:
                width = img1.shape[1] - posx

            targety, height = 0, img2.shape[0]
            if posy < 0:
                targety = -posy
                posy = 0
                height -= targety
            elif posy > img1.shape[0] - img2.shape[0]:
                height = img1.shape[0] - posy
            # print(img1.shape, img2.shape, targetx, width, targety, height)

            # TODO 덮어쓰기
            img1[posy : posy + height, posx : posx + width, :] = img2[targety : targety + height, targetx : targetx + width, :]
            mask1[posy : posy + height, posx : posx + width] = mask2[targety : targety + height, targetx : targetx + width]

            # TODO save
            text = []
            with open(text1[0], "r") as tf:
                lines = tf.readlines()
            for l in lines:
                if len(l) > 1:
                    text.append(l.split("\n", 1)[0])
            t = [0]
            flag = False
            for h in range(mask1.shape[0]):
                for w in range(mask1.shape[1]):
                    if mask1[h, w] > 0:
                        t.append(w)
                        t.append(h)
                        flag = True
                        break
                if flag:
                    break
            flag = False
            for h in range(mask1.shape[0]):
                h = mask1.shape[0] - h - 1
                for w in range(mask1.shape[1]):
                    w = mask1.shape[1] - w - 1
                    if mask1[h, w] > 0:
                        t.append(w - t[1])
                        t.append(h - t[2])
                        flag = True
                        break
                if flag:
                    break
            text.append(" ".join(list(map(str, t))))

            name = image.rsplit(".", 1)[0] + f"_{idx}.png"
            cv2.imwrite(os.path.join(output, name), img1)
            with open(os.path.join(output, name.replace("png", "txt")), "w") as f:
                f.write("\n".join(text))
        except:
            pass
    print(i, "finished")
print("finish!!")
