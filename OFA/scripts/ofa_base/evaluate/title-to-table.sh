#!/bin/bash -eu

ROOT=${PWD}
OUTPUT=${ROOT}/results/ofa_base/title-to-table/eval.csv

echo "Seed,Rouge-1,Rouge-2,Rouge-F,Table-F1 (header),Table-F1 (group),Table-F1 (value),Corpus-F1 (header),Corpus-F1 (group),Corpus-F1 (value)" > ${OUTPUT}

for seed in {0,1,2,}; do

  echo "seed "${seed}

  echo -n ${seed}"," >> ${OUTPUT}
  cd ${ROOT}/OFA/run_scripts/caption

  RougeF1=`python infobox_rouge.py \
    ${ROOT}/results/ofa_base/title-to-table/${seed}/test_predict.json |\
    grep ":" |\
    awk -F" " '{print $2}'`
  echo -n `echo ${RougeF1} |sed 's/ /,/g'`"," >> ${OUTPUT}

  cd ${ROOT}

  TableF1=`python ${ROOT}/scripts/utils/f_score_table.py \
    ${ROOT}/../datasets/text-to-text/ease/title-to-table/test.tsv \
    ${ROOT}/results/ofa_base/title-to-table/${seed}/test_predict.json |\
  grep ":" |\
  awk -F" " '{print $2}'`
  echo -n `echo ${TableF1} |sed 's/ /,/g'`"," >> ${OUTPUT}

  CorpusF1=`python ${ROOT}/scripts/utils/f_score_corpus.py \
    ${ROOT}/../datasets/text-to-text/ease/title-to-table/test.tsv \
    ${ROOT}/results/ofa_base/title-to-table/${seed}/test_predict.json |\
  grep ":" |\
  awk -F" " '{print $2}'`
  echo `echo ${CorpusF1} |sed 's/ /,/g'` >> ${OUTPUT}

done

echo "Results are recorded in \"${OUTPUT}\"."
