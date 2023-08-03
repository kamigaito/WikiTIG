#!/bin/bash -eu

ROOT=${PWD}
DATADIR=${PWD}/checkpoints

if [ ! -d ${DATADIR} ]; then
    mkdir -p ${DATADIR}
fi

cd ${DATADIR}

# BART-base
wget https://dl.fbaipublicfiles.com/fairseq/models/bart.base.tar.gz
tar xvzf bart.base.tar.gz

# OFA-base
wget https://ofa-beijing.oss-cn-beijing.aliyuncs.com/checkpoints/ofa_base.pt

# VQGAN & CLIP
wget https://ofa-beijing.oss-cn-beijing.aliyuncs.com/checkpoints/image_gen_large_best.zip
unzip image_gen_large_best.zip
