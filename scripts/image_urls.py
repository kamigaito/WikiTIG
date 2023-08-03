import hashlib

with open("./extracted/images.txt") as f_in, open("./extracted/image_urls.txt", "w") as f_out:
    body = ""
    for line in f_in:
        img_name = line.strip()
        img_name = img_name.replace(".svg.png", ".svg")
        hs = hashlib.md5(img_name.encode()).hexdigest()
        img_path = "/".join([hs[0],hs[:2],img_name])
        dirs = ["https://upload.wikimedia.org/wikipedia/commons/",
                "https://upload.wikimedia.org/wikipedia/en/"]
        for prefix in dirs:
            url = prefix + img_path
            f_out.write(url + "\n")
