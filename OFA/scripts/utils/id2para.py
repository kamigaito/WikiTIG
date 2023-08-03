import json
import sys

GOLD = sys.argv[1]
GEN = sys.argv[2]
OUTPUT = sys.argv[3]

title2ref = {}
with open(GOLD) as f_in:
    for line in f_in:
        title, img, table, title, b64 = line.strip().split("\t")
        title2ref[title] = table

with open(GEN) as f_in:
    gen = json.load(f_in)

pairs = []
for line in gen:
    hyp = line["caption"]
    ref = title2ref[line["image_id"]]
    pairs.append({"hyp" : hyp, "ref" : ref})

with open(OUTPUT, "w") as f_out:
    json.dump(pairs, f_out)
