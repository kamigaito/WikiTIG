import json
import sys
import collections

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
                        #count_lists["values"].append((group, header, col))
                        count_lists["values"].append((header, col))
                else:
                    if col != "":
                        header = col
                        count_lists["headers"].append(col)
                    else:
                        break
                    
def main():
    REF = sys.argv[1]
    GEN = sys.argv[2]
    count_lists = {"ref" : {"headers" : [], "groups" : [], "values" : []}, "gen" : {"headers" : [], "groups" : [], "values" : []}}
    with open(GEN) as f_in:
        gens = json.load(f_in)
    with open(REF) as f_in:
        for line_id, line in enumerate(f_in):
            cols = [col.strip() for col in line.split("\t")]
            if len(cols) == 2:
                uniq_id, ref = [col.strip() for col in line.split("\t")]
            elif len(cols) == 5:
                uniq_id, img_id, ref, uniq_id, base64 = [col.strip() for col in line.split("\t")]
            else:
                assert(False)
            if "hyp" in gens[line_id]:
                gen = gens[line_id]["hyp"]
            elif "caption" in gens[line_id]:
                gen = gens[line_id]["caption"]
            else:
                print(gens[line_id])
                assert(False)
            accumulate_counts(ref, gen, count_lists)
    # The number of reference and generated tables should be the same
    assert(line_id + 1 == len(gens))
    print("Corpus-F1")
    f_score_lists = calc_score(count_lists)
    for k in f_score_lists.keys():
        print(k + ": " + str(f_score_lists[k]))

if __name__=="__main__":
    main()
