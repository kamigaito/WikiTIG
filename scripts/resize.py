import sys
import os
import torchvision.transforms as T
from PIL import Image
from PIL import ImageFile

Image.MAX_IMAGE_PIXELS = None
ImageFile.LOAD_TRUNCATED_IMAGES = True

dir_input = sys.argv[1]
dir_output = sys.argv[2]
size = int(sys.argv[3])

for file_name in os.listdir(dir_input):
    file_path = dir_input + "/" + file_name
    print(file_path)
    if os.path.splitext(file_path)[-1].lower() == ".svg":
        print("skip")
        continue
    img = Image.open(file_path)
    if min(img.size) > size:
        transform = T.Resize(size = size)
        img = transform(img)
    if img.format == "PNG":
        if img.mode != "RGBA":
          img = img.convert("RGBA")
    img.save(dir_output + "/" + file_name, quality=100)
