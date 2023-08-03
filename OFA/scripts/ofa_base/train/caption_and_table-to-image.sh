#!/bin/bash -eu

ROOT=${PWD}
export PYTHONPATH=${PYTHONPATH}:${ROOT}/OFA/fairseq

# Guide:
# This script supports distributed training on multi-gpu workers (as well as single-worker training). 
# Please set the options below according to the comments. 
# For multi-gpu workers training, these options should be manually set for each worker. 
# After setting the options, please run the script on each worker.
# To use the shuffled data (if exists), please uncomment the Line 23.

# The port for communication
export MASTER_PORT=8214

data_dir=${ROOT}/../datasets/text-to-image/256/exact/caption_and_table-to-image
data=${data_dir}/train.tsv,${data_dir}/valid.tsv
# Note: If you have shuffled the data in advance, please uncomment the line below.
# data=${data_dir}/coco_vqgan_train_1.tsv,${data_dir}/coco_vqgan_train_2.tsv,${data_dir}/coco_vqgan_train_3.tsv,${data_dir}/coco_vqgan_train_4.tsv,${data_dir}/coco_vqgan_train_5.tsv,${data_dir}/coco_vqgan_train_6.tsv,${data_dir}/coco_vqgan_train_7.tsv,${data_dir}/coco_vqgan_train_8.tsv,${data_dir}/coco_vqgan_train_9.tsv,${data_dir}/coco_vqgan_train_10.tsv,${data_dir}/coco_vqgan_dev.tsv
restore_file=${ROOT}/checkpoints/ofa_base.pt
selected_cols=0,2,1

log_dir=${ROOT}/logs/ofa_base/caption_and_table-to-image
save_dir=${ROOT}/models/ofa_base/caption_and_table-to-image

if [ ! -d ${log_dir} ]; then
    mkdir -p ${log_dir}
fi
if [ ! -d ${save_dir} ]; then
    mkdir -p ${save_dir}
fi

bpe_dir=../../utils/BPE
user_dir=../../ofa_module

task=image_gen
arch=ofa_base
criterion=adjust_label_smoothed_cross_entropy
label_smoothing=0.0
batch_size=4
update_freq=4
encoder_drop_path_rate=0.1
decoder_drop_path_rate=0.1
dropout=0.1
attention_dropout=0.0
max_src_length=1022
max_tgt_length=1024
num_bins=1000
code_image_size=256
constraint_range=50265,58457

VQGAN_MODEL_PATH=${ROOT}/checkpoints/vqgan/last.ckpt
VQGAN_CONFIG_PATH=${ROOT}/checkpoints/vqgan/model.yaml
CLIP_MODEL_PATH=${ROOT}/checkpoints/clip/ViT-B-16.pt

cd OFA/run_scripts/image_gen

for total_num_updates in {40000,}; do
  echo "total_num_updates "${total_num_updates}
  for warmup_updates in {2000,}; do
    echo "warmup_updates "${warmup_updates}  
    for lr in {1e-3,}; do
      echo "lr "${lr}
      for seed in {0,1,2,}; do
        echo "seed "${seed}

        log_file=${log_dir}/${total_num_updates}"_"${warmup_updates}"_"${lr}"_"${seed}".log"
        save_path=${save_dir}/${total_num_updates}"_"${warmup_updates}"_"${lr}"_"${seed}
        GEN_IMAGES_PATH=${ROOT}/results/ofa_base/caption_and_table-to-image/${seed}/valid
        
        if [ ! -d ${save_path} ]; then
            mkdir -p ${save_path}
        fi
        if [ ! -d ${GEN_IMAGE_PATH} ]; then
          mkdir -p ${GEN_IMAGE_PATH}
        fi

        CUDA_VISIBLE_DEVICES=0,1,2,3 python3 -m torch.distributed.launch --nproc_per_node=4 --master_port=${MASTER_PORT} ../../train.py \
            ${data} \
            --selected-cols=${selected_cols} \
            --bpe-dir=${bpe_dir} \
            --user-dir=${user_dir} \
            --restore-file=${restore_file} \
            --reset-optimizer --reset-dataloader --reset-meters \
            --save-dir=${save_path} \
            --task=${task} \
            --arch=${arch} \
            --criterion=${criterion} \
            --label-smoothing=${label_smoothing} \
            --batch-size=${batch_size} \
            --batch-size-valid=1 \
            --update-freq=${update_freq} \
            --encoder-normalize-before \
            --decoder-normalize-before \
            --share-decoder-input-output-embed \
            --share-all-embeddings \
            --layernorm-embedding \
            --patch-layernorm-embedding \
            --code-layernorm-embedding \
            --encoder-drop-path-rate=${encoder_drop_path_rate} \
            --decoder-drop-path-rate=${decoder_drop_path_rate} \
            --dropout=${dropout} \
            --attention-dropout=${attention_dropout} \
            --weight-decay=0.01 \
            --optimizer=adam \
            --adam-betas="(0.9,0.999)" \
            --adam-eps=1e-08 \
            --clip-norm=1.0 \
            --lr-scheduler=polynomial_decay \
            --lr=${lr} \
            --total-num-update=${total_num_updates} \
            --warmup-updates=${warmup_updates} \
            --log-format=simple \
            --log-interval=10 \
            --seed=${seed} \
            --fixed-validation-seed=7 \
            --keep-last-epochs=15 \
            --save-interval=5 --validate-interval=5 \
            --max-update=${total_num_updates} \
            --best-checkpoint-metric=score --maximize-best-checkpoint-metric \
            --eval-args='{"beam":1,"min_len":1024,"max_len_a":0,"max_len_b":1024,"sampling_topk":256,"temperature":1.0}' \
            --max-src-length=${max_src_length} \
            --max-tgt-length=${max_tgt_length} \
            --find-unused-parameters \
            --add-type-embedding \
            --scale-attn \
            --scale-fc \
            --scale-heads \
            --disable-entangle \
            --num-bins=${num_bins} \
            --code-image-size=${code_image_size} \
            --constraint-range=${constraint_range} \
            --vqgan-model-path=${VQGAN_MODEL_PATH} \
            --vqgan-config-path=${VQGAN_CONFIG_PATH} \
            --clip-model-path=${CLIP_MODEL_PATH} \
            --gen-images-path=${GEN_IMAGES_PATH} \
            --fp16 \
            --fp16-scale-window=256 \
            --num-workers=0 > ${log_file} 2>&1
      done
    done
  done
done
