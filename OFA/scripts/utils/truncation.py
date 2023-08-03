from argparse import ArgumentParser

parser = ArgumentParser()

parser.add_argument('--prefix', type=str, help='Prefix to the source and target file')
parser.add_argument('--src', type=str, help='Suffix of the source file')
parser.add_argument('--tgt', type=str, help='Suffix of the target file')
parser.add_argument('--max_src_len', type=int, help='Maximum length of a source sequence')
parser.add_argument('--max_tgt_len', type=int, help='Maximum length of a target sequence')

args = parser.parse_args()

for side, limit in [(args.src, args.max_src_len), (args.tgt, args.max_tgt_len)]:
    with open(args.prefix + "." + side) as f_in, open(args.prefix + ".cut." + side, "w") as f_out:
        for line in f_in:
            line = line.strip()
            cols = line.split(" ")
            f_out.write(" ".join(cols[:limit]) + "\n")
