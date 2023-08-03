import sys
import os
import random
import torchvision.transforms as T
from PIL import Image
from PIL import ImageFile

Image.MAX_IMAGE_PIXELS = None
ImageFile.LOAD_TRUNCATED_IMAGES = True

dir_input = sys.argv[1]
dir_output = sys.argv[2]
size = int(sys.argv[3])

def crop_center(img):
    w, h = img.size
    assert(h == size or w == size)
    return img.crop(((w - size) // 2,
                         (h - size) // 2,
                         (w + size) // 2,
                         (h + size) // 2))

for file_name in os.listdir(dir_input):
    file_path = dir_input + "/" + file_name
    print(file_path)
    file_ext = os.path.splitext(file_path)[-1].lower()
    if file_ext == ".svg":
        print("skip")
        continue
    img = Image.open(file_path)
    if img.format == "PNG":
        if img.mode != "RGBA":
            img = img.convert("RGBA")
    transform = T.Resize(size = size)
    img = transform(img)
    print(img.size)
    cropped = crop_center(img)
    cropped.save(dir_output + "/" + file_name, quality=100)
