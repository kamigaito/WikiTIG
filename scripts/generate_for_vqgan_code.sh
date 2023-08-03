#!/bin/bash -eu

VQGAN_MODEL="${PWD}/OFA/checkpoints/vqgan/last.ckpt"
VQGAN_CONFIG="${PWD}/OFA/checkpoints/vqgan/model.yaml"
BASE64_DIR="${PWD}/extracted/base64_cropped"

SIZES=("128" "256")
OUT_DIR="${PWD}/extracted/vqgan"

if [ ! -d ${OUT_DIR} ]; then
    mkdir -p ${OUT_DIR}
fi

cd ./OFA/OFA/run_scripts/image_gen

# for image-only data each line of the given input file should contain these information (separated by tabs):
# input format
#   image-id and image base64 string
# input example:
#   12455 /9j/4AAQSkZJ....UCP/2Q==
#
# output format
#   image-id and code
#   12455 6288 4495 4139...4691 4844 6464

for SIZE in ${SIZES[@]}; do
    CUDA_VISIBLE_DEVICES=0 python generate_code.py \
      --file ${BASE64_DIR}/${SIZE}.tsv \
      --outputs ${OUT_DIR}/${SIZE}.tsv \
      --selected_cols 0,1 \
      --code_image_size ${SIZE} \
      --vq_model vqgan \
      --vqgan_model_path ${VQGAN_MODEL} \
      --vqgan_config_path ${VQGAN_CONFIG}
done
