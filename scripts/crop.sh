#!/bin/bash

IN_DIR="./extracted/images"
SIZES=("128" "256")
for SIZE in ${SIZES[@]}; do
    OUT_DIR="./extracted/cropped/${SIZE}"
    if [ ! -d ${OUT_DIR} ]; then
        mkdir -p ${OUT_DIR}
    fi
    python scripts/crop.py ${IN_DIR} ${OUT_DIR} ${SIZE}
done

