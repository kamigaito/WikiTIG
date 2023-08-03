#!/bin/bash -eu

ROOT=${PWD}
export PYTHONPATH=${PYTHONPATH}:${ROOT}/OFA/fairseq

# The port for communication. Note that if you want to run multiple tasks on the same machine,
# you need to specify different port numbers.
export MASTER_PORT=4081

user_dir=${ROOT}/OFA/ofa_module
bpe_dir=${ROOT}/OFA/utils/BPE

# It may take a long time for the full evaluation. You can sample a small split from the full_test split.
# But please remember that you need at least thousands of images to compute FID and IS, otherwise the resulting scores
# might also no longer correlate with visual quality.

selected_cols=0,2,1
split='test'
VQGAN_MODEL_PATH=${ROOT}/checkpoints/vqgan/last.ckpt
VQGAN_CONFIG_PATH=${ROOT}/checkpoints/vqgan/model.yaml
CLIP_MODEL_PATH=${ROOT}/checkpoints/clip/ViT-B-16.pt
REF_IMAGE_PATH=${ROOT}/../datasets/text-to-image/256/exact/images/test

cd ${ROOT}/OFA/run_scripts/image_gen

for seed in {0,1,2,}; do

  data=${ROOT}/results/ofa_base/title-to-table/${seed}/test_predict_for_image_gen.tsv
  # Preprocess
  python ${ROOT}/scripts/utils/pipeline-for-image-gen.py \
    ${ROOT}/results/ofa_base/title-to-table/${seed}/test_predict.json \
    ${ROOT}/../datasets/text-to-text/ease/title-to-table/test.tsv \
    ${ROOT}/../datasets/text-to-image/256/exact/caption_and_table-to-image/test.tsv \
    ${data}

  path=${ROOT}/models/ofa_base/caption_and_table-to-image/40000_2000_1e-3_${seed}/checkpoint_best.pt
  GEN_IMAGE_PATH=${ROOT}/results/ofa_base/caption_and_ofa_base_gen_table-to-image/${seed}/test

  if [ ! -d ${GEN_IMAGE_PATH} ]; then
    mkdir -p ${GEN_IMAGE_PATH}
  fi
  
  CUDA_VISIBLE_DEVICES=0,1,2,3 python3 -m torch.distributed.launch --nproc_per_node=4 --master_port=${MASTER_PORT} ${ROOT}/OFA/evaluate.py \
    ${data} \
    --path=${path} \
    --user-dir=${user_dir} \
    --task=image_gen \
    --batch-size=1 \
    --log-format=simple --log-interval=1 \
    --seed=42 \
    --gen-subset=${split} \
    --beam=24 \
    --min-len=1024 \
    --max-len-a=0 \
    --max-len-b=1024 \
    --sampling-topk=256 \
    --temperature=1.0 \
    --code-image-size=256 \
    --constraint-range=50265,58457 \
    --fp16 \
    --num-workers=0 \
    --model-overrides="{\"data\":\"${data}\",\"bpe_dir\":\"${bpe_dir}\",\"selected_cols\":\"${selected_cols}\",\"clip_model_path\":\"${CLIP_MODEL_PATH}\",\"vqgan_model_path\":\"${VQGAN_MODEL_PATH}\",\"vqgan_config_path\":\"${VQGAN_CONFIG_PATH}\",\"gen_images_path\":\"${GEN_IMAGE_PATH}\"}" > ${GEN_IMAGE_PATH}/eval.txt
  
  # install requiremnts
  pip install scipy
  # compute IS
  python inception_score.py --gpu 0 --batch-size 128 --path1 ${GEN_IMAGE_PATH}/top1 >> ${GEN_IMAGE_PATH}/eval.txt
  # compute FID, download statistics for test dataset first.
  python fid_score.py --gpu 0 --batch-size 128 --path1 ${GEN_IMAGE_PATH}/top1 --path2 ${REF_IMAGE_PATH} >> ${GEN_IMAGE_PATH}/eval.txt

done
