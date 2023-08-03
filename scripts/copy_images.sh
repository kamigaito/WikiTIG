#!/bin/bash

ROOT=${PWD}
SIZES=("128" "256")
TYPES=("ease" "exact")
SPLITS=("valid" "test")

for TYPE in ${TYPES[@]}; do
    for SIZE in ${SIZES[@]}; do
        for SPLIT in ${SPLITS[@]}; do
            IN_DIR="${ROOT}/extracted/cropped/${SIZE}"
            OUT_DIR="${ROOT}/datasets/text-to-image/${SIZE}/${TYPE}/images/${SPLIT}"
            if [ -d ${OUT_DIR} ]; then
                rm -rf ${OUT_DIR}
            fi
            mkdir -p ${OUT_DIR}
            for file in `cat "${ROOT}/datasets/text-to-image/${SIZE}/${TYPE}/caption-to-image/${SPLIT}.tsv" | awk -F"\t" '{print $1}'`; do
                echo ${file}
                cp ${IN_DIR}/${file} ${OUT_DIR}/
            done
        done
    done
done
