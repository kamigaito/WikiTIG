#!/bin/bash

DIR_IN="./datasets/text-to-image"
SIZES=("128" "256")
TYPES=("ease" "exact")

for SIZE in ${SIZES[@]}; do
    for TYPE in ${TYPES[@]}; do
        FILE_IN="${DIR_IN}/${SIZE}/${TYPE}/all.tsv"
        OUT_DIR="${DIR_IN}/${SIZE}/${TYPE}/caption-to-image"
        if [ ! -d ${OUT_DIR} ]; then
            mkdir -p ${OUT_DIR}
        fi
        python scripts/split_for_caption-to-image_gen.py ${FILE_IN} ${OUT_DIR}
        OUT_DIR="${DIR_IN}/${SIZE}/${TYPE}/caption_and_table-to-image"
        if [ ! -d ${OUT_DIR} ]; then
            mkdir -p ${OUT_DIR}
        fi
        python scripts/split_for_caption_and_table-to-image_gen.py ${FILE_IN} ${OUT_DIR}
    done
done
