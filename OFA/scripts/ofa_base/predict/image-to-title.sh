#!/usr/bin/env bash

ROOT=${PWD}
export PYTHONPATH=${PYTHONPATH}:${ROOT}/OFA/fairseq

# The port for communication. Note that if you want to run multiple tasks on the same machine,
# you need to specify different port numbers.
export MASTER_PORT=1091
path=${ROOT}/models/base/image-to-title/10_0.06_6000/checkpoint_best.pt
result_path=${ROOT}/results/base/image-to-title

cd OFA/run_scripts/caption

user_dir=../../ofa_module
bpe_dir=../../utils/BPE

data_dir=../../../../datasets/image-to-text/480/ease/image-to-title
data=${data_dir}/test.tsv
selected_cols=1,4,2
split='test'

CUDA_VISIBLE_DEVICES=0,1,2,3 python3 -m torch.distributed.launch --nproc_per_node=4 --master_port=${MASTER_PORT} ../../evaluate.py \
    ${data} \
    --path=${path} \
    --user-dir=${user_dir} \
    --task=caption \
    --batch-size=16 \
    --log-format=simple --log-interval=10 \
    --seed=7 \
    --gen-subset=${split} \
    --results-path=${result_path} \
    --beam=5 \
    --max-len-b=1023 \
    --no-repeat-ngram-size=3 \
    --fp16 \
    --num-workers=0 \
    --model-overrides="{\"data\":\"${data}\",\"bpe_dir\":\"${bpe_dir}\",\"eval_cider\":False,\"selected_cols\":\"${selected_cols}\"}"

#python coco_eval.py ../../results/caption/test_predict.json ../../dataset/caption_data/test_caption_coco_format.json
