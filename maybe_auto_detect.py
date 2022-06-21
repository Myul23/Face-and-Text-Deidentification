import os
from time import sleep
from shutil import move

import numpy as np
import cv2

import matplotlib.pyplot as plt


# ? folder existence check
def folder_exitence(output_path):
    images_folder = os.path.join(output_path, "images")
    texts_folder = os.path.join(output_path, "annotations")

    temp = os.listdir(output_path)
    if images_folder.rsplit("/")[1] not in temp:
        try:
            os.mkdir(images_folder)
            print("make images folder")
        except FileExistsError as error:
            print("images folder exists")
    if texts_folder.rsplit("/")[1] not in temp:
        try:
            os.mkdir(texts_folder)
            print("make annotations folder")
        except FileExistsError as error:
            print("annotations folder exists")

    print()
    return images_folder, texts_folder


# ? detection
def detection(data_path, images_folder, texts_folder, text_class_number, check=False, check_function="train2014"):
    for folder_path in os.listdir(data_path):
        if check:
            if folder_path != check_function:
                continue

        # print(folder_path)
        folder_path = os.path.join(data_path, folder_path)
        if os.path.isfile(folder_path):
            continue

        for img_address in os.listdir(folder_path):
            print(img_address, end=" / ")
            img_total_address = os.path.join(folder_path, img_address)
            if not os.path.isfile(img_total_address):
                continue

            output_image_path = os.path.join(images_folder, img_address)
            output_text_path = os.path.join(texts_folder, img_address.rsplit(".", 1)[0] + ".txt")
            img = cv2.imread(img_total_address)
            cv2.imshow("origin", img)

            img_black = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # check with threshold function
            # cv2.imshow("adaptive threshold", cv2.adaptiveThreshold(img_black, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 2))
            # cv2.imshow("Otsu's threshold", cv2.threshold(img_black, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1])
            # cv2.waitKey(0)

            # ? Canny's Edge Detection
            window_name = "Canny Edge Detection Visualization"
            cv2.namedWindow(window_name)
            # callback function overwritting
            def onChange(x):
                pass

            cv2.createTrackbar("low value", window_name, 0, 255, onChange)
            cv2.createTrackbar("high value", window_name, 0, 255, onChange)
            cv2.imshow(window_name, img_black)

            # * edge detection tracking
            image = None
            while cv2.waitKey(300) != ord("c"):
                low = cv2.getTrackbarPos("low value", window_name)
                high = cv2.getTrackbarPos("high value", window_name)
                image = cv2.Canny(img_black, low, high)
                cv2.imshow(window_name, image)
                # low < high여야 하지만, function이 알아서 swap
            if image is None:
                print("wrong")
                exit(-1)
            cv2.destroyWindow(window_name)

            # ? erode & dilate loop
            images = []
            k = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))  # cv2.MORPH_EPLIPSE, cv2.MORPH_RECT
            images.append(cv2.erode(cv2.dilate(image, k), k))

            window_name = "find proper binary image"
            cv2.imshow(window_name, images[-1])
            key = cv2.waitKey(0)

            while key != ord("c"):
                # 침식, 영역 줄이기
                if key == ord("a"):
                    print("erode", end=" / ")
                    images.append(cv2.erode(images[-1], k))
                # 팽창, 영역 넗히기
                elif key == ord("d"):
                    print("dilate", end=" / ")
                    images.append(cv2.dilate(images[-1], k))
                # binary를 뒤집고 싶을 때 (reverse)
                elif key == ord("r"):
                    print("reverse", end=" / ")
                    images.append(cv2.bitwise_not(images[-1]))
                # ctrl + z
                elif key == ord("z") and len(images) > 1:
                    print("before", end=" / ")
                    images.pop()
                else:
                    key = cv2.waitKey(0)
                    continue

                cv2.imshow(window_name, images[-1])
                key = cv2.waitKey(0)

            # ? contouring & select bounding box
            # parameter explanation : https://076923.github.io/posts/Python-opencv-21/

            points = list(cv2.findContours(images[-1], cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)[0])
            # remove small area
            index = 0
            while index < len(points):
                if cv2.contourArea(points[index]) < 150:
                    points.pop(index)
                else:
                    index += 1

            text = ""
            index = 0
            while index < len(points):
                x, y, w, h = cv2.boundingRect(points[index])

                origin = img.copy()
                cv2.rectangle(origin, (x, y), (x + w, y + h), (200, 200, 200), 2)
                cv2.imshow("origin", origin)

                key = cv2.waitKey(0)
                if key == ord("z"):
                    if index > 0:
                        index -= 1
                    continue
                elif key == ord("c"):
                    text = " ".join([text, text_class_number, str(x / img.shape[0]), str(y / img.shape[1]), str(w), str(h)]) + "\n"
                index += 1
            # print(text)

            if len(text) > 0:
                print(len(text.split("\n")) - 1, end=" / ")
                move(img_total_address, output_image_path)
                with open(output_text_path, "w") as f:
                    f.write(text)
            print("finish")


if __name__ == "__main__":
    text_class_number = "1"
    data_path = "making"
    output_path = "making_origin"

    images_folder, texts_folder = folder_exitence(output_path)
    detection(data_path, images_folder, texts_folder, text_class_number, check=True, check_function="train2014")

    print("the end")
    cv2.destroyAllWindows()
