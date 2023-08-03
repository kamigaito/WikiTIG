#!/bin/bash

SIZES=("128" "256")
OUT_DIR="./extracted/base64_cropped"
if [ ! -d ${OUT_DIR} ]; then
    mkdir -p ${OUT_DIR}
fi

for SIZE in ${SIZES[@]}; do
    IN_DIR="./extracted/cropped/${SIZE}"
    OUT_PATH="${OUT_DIR}/${SIZE}.tsv"
    python scripts/conv_to_base64.py ${IN_DIR} \
    > ${OUT_PATH}
done
