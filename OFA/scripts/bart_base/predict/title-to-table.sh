#!/bin/bash -eu

ROOT=${PWD}
export PYTHONPATH=${PYTHONPATH}:${ROOT}/OFA/fairseq

# The port for communication. Note that if you want to run multiple tasks on the same machine,
# you need to specify different port numbers.

export MASTER_PORT=2081

cd OFA/run_scripts/gigaword

user_dir=${ROOT}/OFA/ofa_module
bpe_dir=${ROOT}/checkpoints/bart.base

data_dir=${ROOT}/../datasets/text-to-text/ease/title-to-table
data=${data_dir}/test.tsv
selected_cols=0,1
split='test'

for seed in {0,1,2,}; do
  echo "seed "${seed}
  path=${ROOT}/models/bart_base/title-to-table/10_1e-4_0.2_${seed}/checkpoint_best.pt
  result_path=${ROOT}/results/bart_base/title-to-table/${seed}
  CUDA_VISIBLE_DEVICES=0,1,2,3 python3 -m torch.distributed.launch --nproc_per_node=4 --master_port=${MASTER_PORT} ../../evaluate.py \
    ${data} \
    --path=${path} \
    --user-dir=${user_dir} \
    --task=gigaword \
    --batch-size=32 \
    --log-format=simple --log-interval=10 \
    --seed=7 \
    --gen-subset=${split} \
    --results-path=${result_path} \
    --beam=5 \
    --max-len-b=1023 \
    --no-repeat-ngram-size=3 \
    --fp16 \
    --num-workers=0 \
    --model-overrides="{\"data\":\"${data}\",\"bpe_dir\":\"${bpe_dir}\",\"selected_cols\":\"${selected_cols}\"}"
done
