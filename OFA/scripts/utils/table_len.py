"""
This script calculates table legths for each split.
"""

import json
import sys
import collections
import numpy as np

def count_cells(table):
    num_cells = 0
    for row in table.split("<>"):
        cols = row.split("|")
        for cid, col in enumerate(cols):
            if col != "":
                num_cells += 1
    return num_cells

def main():
    REF = sys.argv[1]
    table_lens = []
    with open(REF) as f_in:
        for line_id, line in enumerate(f_in):
            cols = [col.strip() for col in line.split("\t")]
            if len(cols) == 2:
                uniq_id, ref = [col.strip() for col in line.split("\t")]
            elif len(cols) == 5:
                uniq_id, img_id, ref, uniq_id, base64 = [col.strip() for col in line.split("\t")]
            else:
                assert(False)
            num_cells = count_cells(ref)
            table_lens.append(num_cells)
    print("Number of cells in tables:")
    print("mean: ", np.mean(table_lens))
    print("std: ", np.std(table_lens))
    print("max: ", np.max(table_lens))
    print("min: ", np.min(table_lens))
    print("Ratio of zero length tables:")
    print(len([1 for l in table_lens if l == 0]) / len(table_lens))

if __name__=="__main__":
    main()
