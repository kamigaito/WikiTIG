import json
import os
import sys
import re

JSON_FILE = sys.argv[1]
VQG_FILE = sys.argv[2]
OUT_DIR_1 = sys.argv[3]
OUT_DIR_2 = sys.argv[4]

c_sep = "|"
r_sep = "<>"

c_rep = "/"
r_rep = "//"

img2infobox = {}

with open(JSON_FILE) as f_in:
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
                img2infobox[image["src"]] = article

def decite(text):
    return re.sub(r"\[[0-9]+\]","",text)

def filter_table(table):
    table = decite(table)
    filtered = []
    for row in table.split(r_sep):
        row = row.strip()
        cols = [col.strip() for col in row.split(c_sep)]
        # Group header / Value
        if len(cols) == 1:
            if cols[0] != "":
                filtered.append(cols[0])
        # Row header & Value
        elif len(cols) == 2:
            if cols[0] != "" and cols[1] != "":
                filtered.append(" ".join([cols[0], c_sep, cols[1]]))
    return (" " + r_sep + " ").join(filtered).strip()

with open(VQG_FILE) as f_in, open(OUT_DIR_1 + "/all.tsv", "w") as f_out_exact, open(OUT_DIR_2 + "/all.tsv", "w") as f_out_ease:
    for line in f_in:
        img, code = line.strip().split("\t")
        title = img2infobox[img]["title"].strip()
        caption = img2infobox[img]["infobox"][1][0]["text"].strip()
        if "(" in title:
            name = title.split("(")[0].strip()
        else:
            name = title
        if caption != "" and name.lower() not in caption.lower():
            caption = title + " - " + caption
        box = img2infobox[img]["infobox"]
        rows = []
        for row_id in range(len(box)):
            if row_id in [0, 1]:
                continue
            cols = []
            is_skip = False
            for cell in box[row_id]:
                # Only rows without images
                if "images" in cell:
                    is_skip = True
                    break
                cols.append(cell["text"].strip().replace(r_sep, r_rep).replace(c_sep, c_rep))
            if is_skip:
                continue
            rows.append(c_sep.join(cols))
        table = r_sep.join(rows)
        table = filter_table(table)
        # title caption table img code
        columns = [title,decite(caption),table,img,code]
        body = "\t".join([" ".join(col.split()) for col in columns])
        if table == "":
            continue
        if caption != "":
            f_out_exact.write(body + "\n")
        f_out_ease.write(body + "\n")
