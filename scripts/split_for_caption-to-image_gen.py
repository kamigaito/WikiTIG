import os
import sys
import hashlib

FILE_IN = sys.argv[1]
OUT_DIR = sys.argv[2]
SPLIT_SIZE = 20 # 1 / SPLIT_SIZE will be the size of the test and validation dataset

test_file = OUT_DIR + "/test.tsv"
valid_file = OUT_DIR + "/valid.tsv"
train_file = OUT_DIR + "/train.tsv"

# Each line of the dataset represents a sample with the following format. The information of uniq-id, image-code (produced by vqgan, a list of integers separated by single-whitespaces), caption are separated by tabs.
def line_format(f_out, uniq_id, caption, table, img, code):
    f_out.write("\t".join([img, code, caption, uniq_id]) + "\n")

with open(FILE_IN) as f_in, open(test_file, "w") as f_test, open(valid_file, "w") as f_valid, open(train_file, "w") as f_train:
    for line in f_in:
        line = line.strip()
        title, caption, table, img, code = line.split("\t")
        title_hash = int(hashlib.sha256(title.encode("UTF-8")).hexdigest(), 16)
        if title_hash % SPLIT_SIZE == 0:
            line_format(f_test, title, caption, table, img, code)
        elif title_hash % SPLIT_SIZE == 1:
            line_format(f_valid, title, caption, table, img, code)
        else:
            line_format(f_train, title, caption, table, img, code)
