#!/bin/bash

SIZES=("256" "384" "480")
OUT_DIR="./extracted/base64_resized"
if [ ! -d ${OUT_DIR} ]; then
    mkdir -p ${OUT_DIR}
fi

for SIZE in ${SIZES[@]}; do
    IN_DIR="./extracted/resized/${SIZE}"
    OUT_PATH="${OUT_DIR}/${SIZE}.tsv"
    python scripts/conv_to_base64.py ${IN_DIR} \
    > ${OUT_PATH}
done
