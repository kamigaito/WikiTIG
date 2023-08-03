#!/bin/bash

IN_DIR="./extracted/images"
SIZES=("256")

for SIZE in ${SIZES[@]}; do
    OUT_DIR="./extracted/resized/${SIZE}"
    if [ ! -d ${OUT_DIR} ]; then
        mkdir -p ${OUT_DIR}
    fi
    for file_path in ${IN_DIR}/*; do
        file_name=`basename ${file_path}`
        file_ext=`echo ${file_name} |awk -F . '{print $NF}' |tr '[:upper:]' '[:lower:]'`
        if [ ${file_ext} = "svg" ]; then
            continue
        fi
        echo ${file_path}
        # imagemagick - https://imagemagick.org
        convert ${file_path} \
            -resize "${SIZE}x${SIZE}" \
            -gravity "Center" \
            -extent "${SIZE}x${SIZE}" \
        ${OUT_DIR}/${file_name}
    done
done
