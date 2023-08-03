#!/bin/bash -eu

ROOT=${PWD}
INPUT_DIR=${ROOT}/results/ofa_base/caption_and_table-to-image
OUTPUT=${INPUT_DIR}/eval.csv

echo "Seed,CLIP,IS,FID" > ${OUTPUT}

for seed in {0,1,2,}; do

  echo "seed "${seed}

  echo -n ${seed}"," >> ${OUTPUT}

  INPUT=${INPUT_DIR}/${seed}/test/eval.txt

  CLIP_SCORE=`cat ${INPUT} |\
  grep "score_sum" |\
  tail -n 1 |\
  awk -F" " '{print $15}'`  

  echo -n "${CLIP_SCORE}," >> ${OUTPUT}
  
  IS=`cat ${INPUT} |\
  grep "IS mean" |\
  tail -n 1 |\
  awk -F" " '{print $3}'`  
  
  echo -n "${IS}," >> ${OUTPUT}
  
  FID=`cat ${INPUT} |\
  grep "FID" |\
  tail -n 1 |\
  awk -F" " '{print $2}'`  

  echo ${FID} >> ${OUTPUT}

done

echo "Results are recorded in \"${OUTPUT}\"."
