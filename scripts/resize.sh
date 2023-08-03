#!/bin/bash

IN_DIR="./extracted/images"
SIZES=("256" "384" "480")

for SIZE in ${SIZES[@]}; do
    OUT_DIR="./extracted/resized/${SIZE}"
    if [ ! -d ${OUT_DIR} ]; then
        mkdir -p ${OUT_DIR}
    fi
    python scripts/resize.py ${IN_DIR} ${OUT_DIR} ${SIZE}
done
