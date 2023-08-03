#!/bin/bash -eu

SIZES=("128" "256")

for SIZE in ${SIZES[@]}; do
    JSONL_FILE="./extracted/enwiki2008.jsonl"
    VQG_FILE="./extracted/vqgan/${SIZE}.tsv"
    OUT_DIR="./datasets/text-to-image/${SIZE}"
    OUT_DIR_1="${OUT_DIR}/exact"
    OUT_DIR_2="${OUT_DIR}/ease"
    if [ ! -d "${OUT_DIR_1}" ]; then
        mkdir -p "${OUT_DIR_1}"
    fi
    if [ ! -d "${OUT_DIR_2}" ]; then
        mkdir -p "${OUT_DIR_2}"
    fi
    python scripts/make_dataset_text-to-image.py ${JSONL_FILE} ${VQG_FILE} ${OUT_DIR_1} ${OUT_DIR_2}
done
