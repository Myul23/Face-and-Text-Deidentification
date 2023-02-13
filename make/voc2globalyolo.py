import os


base = "data/after/PennFudanPed/Annotation"
output = "data/after/PennFudanPed/yolo"
for f in os.listdir(base):
    with open(os.path.join(base, f), "r") as t:
        lines = t.readlines()

    text = ""
    for l in lines:
        if not l.startswith("Bounding"):
            continue
        for s in ["(", ",", "-", ")", "\n"]:
            l = l.replace(s, " ")

        temp = l.split(" ")
        t = list(map(int, [temp[20], temp[22], temp[27], temp[29]]))
        t = [1, t[0], t[1], t[2] - t[0], t[3] - t[1]]
        text += " ".join(list(map(str, t))) + "\n"
    # print(text[:-1])

    with open(os.path.join(output, f), "w") as t:
        t.write(text[:-1])


# ? xml
import os
import xml.etree.ElementTree as ET


base = "data/after/Test/Annotations"
output = "data/after/Test/yolo"
if not os.path.exists(output):
    os.mkdir(output)


for f in os.listdir(base):
    tree = ET.parse(os.path.join(base, f))
    root = tree.getroot()

    text = ""
    for o in root.findall("object"):
        for b in o.findall("bndbox"):
            xmin = b.find("xmin").text
            ymin = b.find("ymin").text
            xmax = b.find("xmax").text
            ymax = b.find("ymax").text
            t = list(map(int, [xmin, ymin, xmax, ymax]))
            t = [1, t[0], t[1], t[2] - t[0], t[3] - t[1]]
            text += " ".join(list(map(str, t))) + "\n"
    # print(text[:-1])

    with open(os.path.join(output, f.replace("xml", "txt")), "w") as t:
        t.write(text[:-1])
