import json
import sys

GEN = sys.argv[1]
EASE = sys.argv[2]
EXACT = sys.argv[3]
OUTPUT = sys.argv[4]

with open(GEN) as f_in:
    gen = json.load(f_in)

tables = {}
with open(EASE) as f_in:
    line_id = 0
    for line in f_in:
        uniq_id, table = [col.strip() for col in line.split("\t")]
        tables[uniq_id] = " | ".join((" <> ".join(gen[line_id]["hyp"].split("<>"))).split("|"))
        line_id += 1

with open(EXACT) as f_in, open(OUTPUT, "w") as f_out:
    for line in f_in:
        img, code, caption, uniq_id = line.strip().split("\t")
        caption = " <> ".join([caption.split("<>")[0],tables[uniq_id]])
        f_out.write("\t".join([img, code, caption, uniq_id]) + "\n")

