from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import numpy as np

parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument('--path1', type=str, help='path to images')
parser.add_argument('--path2', type=str, help='path to images')
parser.add_argument('--num_samples', type=int, default=10000, help='number of samples')
parser.add_argument('--sample_ratio', type=float, default=0.5, help='sample ratio')

def ret_scores(file_name):
    scores = []
    with open(file_name) as f_in:
        for line in f_in:
            line = line.strip()
            cols = line.split("|")
            if len(cols) == 4 and "CLIP Score" in cols[3]:
                attr, val = cols[3].strip().split(":")
                if attr == "CLIP Score":
                    scores.append(float(val.strip())) 
    return scores

def sampled_scores(scores_list, reduced_ids):
    ret_score = 0.0
    for scores in scores_list:
        ret_score += np.mean([scores[rid] for rid in reduced_ids])
    return ret_score

if __name__ == '__main__':
    args = parser.parse_args()
    scores_list_1 = []
    scores_list_2 = []
    for f_name in args.path1.split(","):
        scores_list_1.append(ret_scores(f_name))
    for f_name in args.path2.split(","):
        scores_list_2.append(ret_scores(f_name))
    assert(len(scores_list_1) == len(scores_list_2))
    assert(len(scores_list_1[0]) == len(scores_list_2[0]))
    ids = list(range(len(scores_list_1[0])))
    sample_size = int(len(ids)*args.sample_ratio)
    win_1 = 0
    for sample_id in range(args.num_samples):
        reduced_ids = np.random.choice(ids,sample_size,replace=True)
        if sampled_scores(scores_list_1, reduced_ids) > sampled_scores(scores_list_2, reduced_ids):
            win_1 += 1
    p_value = 1.0 - win_1 / args.num_samples
    print("p-value: " + str(p_value))
