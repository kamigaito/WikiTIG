import base64
import sys
import os

dirname = sys.argv[1]

for file_name in os.listdir(dirname):
    file_path = dirname + "/" + file_name
    with open(file_path, "rb") as img_file:
        b64_string = base64.b64encode(img_file.read())
    print(file_name + "\t" + b64_string.decode("'utf-8'"))
