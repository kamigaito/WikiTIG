#!/bin/bash -eu

SIZES=("256" "384" "480")

for SIZE in ${SIZES[@]}; do
    JSONL_FILE="./extracted/enwiki2008.jsonl"
    BASE64_FILE="./extracted/base64_resized/${SIZE}.tsv"
    OUT_DIR_1="./datasets/image-to-text/${SIZE}/exact"
    OUT_DIR_2="./datasets/image-to-text/${SIZE}/ease"
    if [ ! -d "${OUT_DIR_1}" ]; then
        mkdir -p "${OUT_DIR_1}"
    fi
    if [ ! -d "${OUT_DIR_2}" ]; then
        mkdir -p "${OUT_DIR_2}"
    fi
    python scripts/make_dataset_image-to-text.py ${JSONL_FILE} ${BASE64_FILE} ${OUT_DIR_1} ${OUT_DIR_2}
done
