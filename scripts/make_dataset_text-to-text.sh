#!/bin/bash -eu

DIR_IN="./datasets/image-to-text"
TYPES=("ease" "exact")

for TYPE in ${TYPES[@]}; do
    FILE_IN="${DIR_IN}/384/${TYPE}/all.tsv"
    OUT_DIR="./datasets/text-to-text/${TYPE}/title-to-table"
    if [ ! -d ${OUT_DIR} ]; then
        mkdir -p ${OUT_DIR}
    fi
    python scripts/split_for_title-to-table_gen.py ${FILE_IN} ${OUT_DIR}
done
