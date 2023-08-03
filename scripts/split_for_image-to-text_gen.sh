#!/bin/bash

DIR_IN="./datasets/image-to-text"
SIZES=("256" "384" "480")
TYPES=("ease" "exact")

for SIZE in ${SIZES[@]}; do
    for TYPE in ${TYPES[@]}; do
        FILE_IN="${DIR_IN}/${SIZE}/${TYPE}/all.tsv"
        OUT_DIR="${DIR_IN}/${SIZE}/${TYPE}/image-to-title"
        if [ ! -d ${OUT_DIR} ]; then
            mkdir -p ${OUT_DIR}
        fi
        python scripts/split_for_image-to-title_gen.py ${FILE_IN} ${OUT_DIR}
        OUT_DIR="${DIR_IN}/${SIZE}/${TYPE}/image-to-caption"
        if [ ! -d ${OUT_DIR} ]; then
            mkdir -p ${OUT_DIR}
        fi
        python scripts/split_for_image-to-caption_gen.py ${FILE_IN} ${OUT_DIR}
        OUT_DIR="${DIR_IN}/${SIZE}/${TYPE}/image-to-table"
        if [ ! -d ${OUT_DIR} ]; then
            mkdir -p ${OUT_DIR}
        fi
        python scripts/split_for_image-to-table_gen.py ${FILE_IN} ${OUT_DIR}
    done
done
