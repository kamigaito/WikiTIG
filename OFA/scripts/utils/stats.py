"""
This scripts calculate cell frequencies for each type of cells in each split.
"""

import json
import sys
import collections

def accumulate_counts(ref_table, count_lists):
    extract_cells(ref_table, count_lists["ref"])

def freqs(lists):
    c_headers = collections.Counter(lists["headers"])
    c_groups = collections.Counter(lists["groups"])
    c_values = collections.Counter(lists["values"])
    stats = {"headers" : c_headers, "groups" : c_groups, "values" : c_values}
    return stats

def extract_cells(table, count_lists):
    for row in table.split("<>"):
        cols = row.split("|")
        if len(cols) == 1:
            if cols[0] != "":
                group = cols[0]
                count_lists["groups"].append(group)
        elif len(cols) == 2:
            for cid, col in enumerate(cols):
                if col != "":
                    if cid == 0:
                        header = col
                        count_lists["headers"].append(col)
                    else:
                        count_lists["values"].append((header, col))

def calc_stats(count_lists, key):
    refs = freqs(count_lists["ref"])
    print("Number of types:")
    print(len(refs[key]))
    print("Frequency:")
    print(refs[key].total())
    print("List:")
    print(refs[key].most_common() )
                    
def main():
    REF = sys.argv[1]
    KEY = sys.argv[2]
    if KEY not in ["headers", "groups", "values"]:
        print("Choose the key from \"headers\", \"groups\" or \"values\".")
        assert(False)
    count_lists = {"ref" : {"headers" : [], "groups" : [], "values" : []}}
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
    calc_stats(count_lists, KEY)

if __name__=="__main__":
    main()
