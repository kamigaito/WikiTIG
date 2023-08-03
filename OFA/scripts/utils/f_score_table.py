import json
import sys
import collections

def calc_score(ref_table, gen_table):
    refs = extract_cells(ref_table)
    gens = extract_cells(gen_table)
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
    if sum(ref.values()) == 0:
        return 0.0
    r = r_match / sum(ref.values())
    # precision
    p_match = 0
    for k in gen.keys():
        if k in ref:
            # clip values
            p_match += min(gen[k], ref[k])
    if sum(gen.values()) == 0:
        return 0.0
    p = p_match / sum(gen.values())
    if min(p,r) > 0.0:
        return 2.0 * p * r / (p + r)
    else:
        return 0.0

def extract_cells(table):
    headers = []
    groups = []
    values = []
    group = "<ROOT>"
    for row in table.split("<>"):
        row = row.strip()
        cols = [col.strip() for col in row.split("|")]
        if len(cols) == 1:
            if cols[0] == "":
                group = "<ROOT>"
            else:
                group = cols[0]
                groups.append(group)
        elif len(cols) == 2:
            for cid, col in enumerate(cols):
                if cid != 0:
                    if col != "":
                        values.append((header, col))
                else:
                    if col != "":
                        header = col
                        headers.append(col)
                    else:
                        break
    c_headers = collections.Counter(headers)
    c_groups = collections.Counter(groups)
    c_values = collections.Counter(values)
    return {"headers" : c_headers, "groups" : c_groups, "values" : c_values}
                    
def main():
    REF = sys.argv[1]
    GEN = sys.argv[2]
    f_score_lists = {"headers" : [], "groups" : [], "values" : []}
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
            f_scores = calc_score(ref, gen)
            for k in f_scores.keys():
                f_score_lists[k].append(f_scores[k])
    # The number of reference and generated tables should be the same
    assert(line_id + 1 == len(gens))
    print("Table-F1")
    for k in f_score_lists.keys():
        v = sum(f_score_lists[k]) / len(f_score_lists[k])
        print(k + ": " + str(v) + " (" + str(len(f_score_lists[k])) + ")")

if __name__=="__main__":
    main()
