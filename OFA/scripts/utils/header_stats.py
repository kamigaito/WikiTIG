"""
This script calculates statitics of frequencies for values in each header.
"""

import json
import sys
import collections
import numpy as np

def accumulate_counts(ref_table, count_lists):
    extract_cells(ref_table, count_lists)

def extract_cells(table, count_lists):
    for row in table.split("<>"):
        cols = row.split("|")
        if len(cols) == 2:
            for cid, col in enumerate(cols):
                if col != "":
                    if cid == 0:
                        header = col
                    else:
                        if header not in count_lists:
                            count_lists[header] = {}
                        if col not in count_lists[header]:
                            count_lists[header][col] = 0
                        count_lists[header][col] += 1

def main():
    REF = sys.argv[1]
    count_lists = {}
    with open(REF) as f_in:
        for line_id, line in enumerate(f_in):
            cols = [col.strip() for col in line.split("\t")]
            if len(cols) == 2:
                uniq_id, ref = [col.strip() for col in line.split("\t")]
            elif len(cols) == 5:
                uniq_id, img_id, ref, uniq_id, base64 = [col.strip() for col in line.split("\t")]
            else:
                assert(False)
            accumulate_counts(ref, count_lists)
    type_freq = []
    appear_freq = []
    for key in count_lists.keys():
        type_freq.append(len(count_lists[key].keys()))
        appear_freq.append(sum([count_lists[key][col] for col in count_lists[key].keys()]))
    print("Avg. type freq. for each header:")
    print("mean: ", np.mean(type_freq))
    print("std: ", np.std(type_freq))
    print("max: ", np.max(type_freq))
    print("min: ", np.min(type_freq))
    print("Avg. appearance freq. for each header:")
    print("mean: ", np.mean(appear_freq))
    print("std: ", np.std(appear_freq))
    print("max: ", np.max(appear_freq))
    print("min: ", np.min(appear_freq))

if __name__=="__main__":
    main()
