#!/bin/bash -eu

ROOT=${PWD}
export PYTHONPATH=${PYTHONPATH}:${ROOT}/OFA/fairseq

# The port for communication. Note that if you want to run multiple tasks on the same machine,
# you need to specify different port numbers.
export MASTER_PORT=1091

cd OFA/run_scripts/caption

user_dir=../../ofa_module
bpe_dir=../../utils/BPE

data_dir=../../../../datasets/image-to-text/480/ease/image-to-table
data=${data_dir}/test.tsv
selected_cols=0,4,2
split='test'

for seed in {0,1,2,}; do
  echo "seed "${seed}
  path=${ROOT}/models/ofa_base/image_and_title-to-table/10_0.06_6000_${seed}/checkpoint_best.pt
  result_path=${ROOT}/results/ofa_base/image_and_title-to-table/${seed}
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
done
