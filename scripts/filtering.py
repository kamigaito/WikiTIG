import json

with open("./extracted/enwiki2008.jsonl") as f_in, open("./extracted/images.txt", "w") as f_out:
    images = set()
    for line in f_in:
        line = line.strip()
        article = json.loads(line)
        box = article["infobox"]
        is_skip = True
        if len(box) > 1:
            if (len(box[0]) == 1 and box[0][0]["text"] != "" and "images" not in box[0][0]) and (len(box[1]) == 1 and "images" in box[1][0]):
                is_skip = False
        if not is_skip:
            for image in box[1][0]["images"]:
                images.add(image["src"])
    for image in images:
        f_out.write(image + "\n")
