import json
import sys
import collections
import numpy as np

def accumulate_counts(ref_table, gen_table, count_lists):
    extract_cells(ref_table, count_lists["ref"])
    extract_cells(gen_table, count_lists["gen"])

def freqs(lists):
    c_headers = collections.Counter(lists["headers"])
    c_groups = collections.Counter(lists["groups"])
    c_values = collections.Counter(lists["values"])
    stats = {"headers" : c_headers, "groups" : c_groups, "values" : c_values}
    return stats

def calc_score(count_lists):
    refs = freqs(count_lists["ref"])
    gens = freqs(count_lists["gen"])
    f_scores = {}
    for f_type in ["headers", "groups", "values"]:
        if len(refs[f_type].values()) == 0:
            continue
        f_scores[f_type] = f_score(refs[f_type], gens[f_type])
        # debug
        assert(f_score(refs[f_type], refs[f_type]) == 1.0)
        if len(gens[f_type].values()) > 0:
            assert(f_score(gens[f_type], gens[f_type]) == 1.0)
    return f_scores

def f_score(ref, gen):
    # recall
    r_match = 0
    for k in ref.keys():
        if k in gen:
            # clip values
            r_match += min(ref[k], gen[k])
    r = r_match / sum(ref.values())
    # precision
    p_match = 0
    for k in gen.keys():
        if k in ref:
            # clip values
            p_match += min(gen[k], ref[k])
    p = p_match / sum(gen.values())
    if min(p,r) > 0.0:
        return 2.0 * p * r / (p + r)
    else:
        return 0.0

def extract_cells(table, count_lists):
    group = "<ROOT>"
    for row in table.split("<>"):
        row = row.strip()
        cols = [col.strip() for col in row.split("|")]
        if len(cols) == 1:
            if cols[0] == "":
                group = "<ROOT>"
            else:
                group = cols[0]
                count_lists["groups"].append(group)
        elif len(cols) == 2:
            for cid, col in enumerate(cols):
                if cid != 0:
                    if col != "":
                        count_lists["values"].append((header, col))
                else:
                    if col != "":
                        header = col
                        count_lists["headers"].append(col)
                    else:
                        break
                    
def main():
    REF = sys.argv[1]
    GEN_1 = sys.argv[2]
    GEN_2 = sys.argv[3]
    num_samples=10000
    sample_ratio=0.5
    count_lists_1 = {"ref" : {"headers" : [], "groups" : [], "values" : []}, "gen" : {"headers" : [], "groups" : [], "values" : []}}
    count_lists_2 = {"ref" : {"headers" : [], "groups" : [], "values" : []}, "gen" : {"headers" : [], "groups" : [], "values" : []}}
    lines = []
    print(REF)
    with open(REF) as f_in:
        for line in f_in:
            lines.append(line)
    gens_list_1 = []
    gens_list_2 = []
    for f_name_1 in GEN_1.split(","):
        print(f_name_1)
        with open(f_name_1) as f_in:
            gens_list_1.append(json.load(f_in))
    for f_name_2 in GEN_2.split(","):
        print(f_name_2)
        with open(f_name_2) as f_in:
            gens_list_2.append(json.load(f_in))

    win_1 = {"headers" : 0, "groups" : 0, "values" : 0}
    num_reduced = int(len(lines)*sample_ratio)
    ids = list(range(len(lines)))
    for sample_id in range(num_samples):
        print(sample_id)
        count_lists_1 = []
        count_lists_2 = []
        for cid in range(len(gens_list_1)):
            count_lists_1.append({"ref" : {"headers" : [], "groups" : [], "values" : []}, "gen" : {"headers" : [], "groups" : [], "values" : []}})
            count_lists_2.append({"ref" : {"headers" : [], "groups" : [], "values" : []}, "gen" : {"headers" : [], "groups" : [], "values" : []}})
        reduced_ids = np.random.choice(ids,num_reduced,replace=True)
        for line_id in reduced_ids:
            line = lines[line_id]
            # Ref
            cols = [col.strip() for col in line.split("\t")]
            if len(cols) == 2:
                uniq_id, ref = [col.strip() for col in line.split("\t")]
            elif len(cols) == 5:
                uniq_id, img_id, ref, uniq_id, base64 = [col.strip() for col in line.split("\t")]
            else:
                assert(False)
            # Gen 1
            for cid, gens_1 in enumerate(gens_list_1):
                if "hyp" in gens_1[line_id]:
                    gen_1 = gens_1[line_id]["hyp"]
                elif "caption" in gens_1[line_id]:
                    gen_1 = gens_1[line_id]["caption"]
                else:
                    print(gens_1[line_id])
                    assert(False)
                accumulate_counts(ref, gen_1, count_lists_1[cid])
            # Gen 2
            for cid, gens_2 in enumerate(gens_list_2):
                if "hyp" in gens_2[line_id]:
                    gen_2 = gens_2[line_id]["hyp"]
                elif "caption" in gens_2[line_id]:
                    gen_2 = gens_2[line_id]["caption"]
                else:
                    print(gens_2[line_id])
                    assert(False)
                accumulate_counts(ref, gen_2, count_lists_2[cid])
        f_score_lists_1 = []
        for cid in range(len(count_lists_1)):
            f_score_lists_1.append(calc_score(count_lists_1[cid]))
        f_score_lists_2 = []
        for cid in range(len(count_lists_2)):
            f_score_lists_2.append(calc_score(count_lists_2[cid]))
        for k in f_score_lists_1[0].keys():
            f_score_1 = sum([f_score_lists_1[cid][k] for cid in range(len(count_lists_1))])
            f_score_2 = sum([f_score_lists_2[cid][k] for cid in range(len(count_lists_1))])
            if f_score_1 > f_score_2:
                win_1[k] += 1
        print(win_1)
    print(win_1)

if __name__=="__main__":
    main()
