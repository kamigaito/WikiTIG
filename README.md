# Table and Image Generation for Investigating Knowledge of Entities in Pre-trained Vision and Language Models

This repository includes the code of creating Wikipedia Table and Image Generation (WiKiTIG) dataset and running OFA on WikiTIG used in our paper: "[Table and Image Generation for Investigating Knowledge of Entities in Pre-trained Vision and Language Models](https://aclanthology.org/2023.acl-short.162/)" in ACL 2023.

```
@inproceedings{kamigaito-etal-2023-table,
    title = "Table and Image Generation for Investigating Knowledge of Entities in Pre-trained Vision and Language Models",
    author = "Kamigaito, Hidetaka  and
      Hayashi, Katsuhiko  and
      Watanabe, Taro",
    booktitle = "Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (Volume 2: Short Papers)",
    month = jul,
    year = "2023",
    address = "Toronto, Canada",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2023.acl-short.162",
    pages = "1904--1917",
}
```

# Setup

To reproduce our result, you need to run following commands:

1. Install packages
```
pip install -r requirements.txt
```
2. Download Datasets
```
bash scripts/download_datasets.sh
```
3. Download Checkpoints
```
cd OFA/
bash scripts/download.sh
```

# Wikipedia Table and Image Generation (WikiTIG) Dataset

You can use our created WikiTIG datasets from the directory, `./datasets`.
To use it, you need to follow the instructions below.

## Image Generation

You can directly use the contained files for image generation.
We used the following files for training our models
- Image generation from title and captions
  - Train: `./datasets/text-to-image/256/exact/caption_and_table-to-image/train.tsv`
  - Valid: `./datasets/text-to-image/256/exact/caption_and_table-to-image/valid.tsv`
  - Test: `./datasets/text-to-image/256/exact/caption_and_table-to-image/test.tsv`
- Image generation from title, caption, and tables
  - Train: `./datasets/text-to-image/256/exact/caption_and_table-to-image/train.tsv`
  - Valid: `./datasets/text-to-image/256/exact/caption_and_table-to-image/valid.tsv`
  - Test: `./datasets/text-to-image/256/exact/caption_and_table-to-image/test.tsv`

Note that the path to the dataset in each setting is represented as follows:
```
./datasets/text-to-image/${RESOLUTION}/${FORMAT}/${TASK}/${SPLIT}.tsv
```
- `${RESOLUTION}` denotes the resolution the images to be generated. You can choose `128` or `256` in this dataset.
- `${FORMAT}` denotes the data format. You can choose `ease` or `exact` in this dataset. `exact` does not have empty captions `ease` has.
- `${TASK}` denotes the target task. You can choose `caption_and_table-to-image` or `caption-to-image` in this dataset.
- `${SPLIT}` denotes what split (e.g., `Train`, `Valid`, or `Test`) the file follows.

## Table Generation

You can directly use the contained files for table generation from titles.
- Table generation from titles
  - Train: `./datasets/text-to-text/ease/title-to-table/train.tsv`
  - Valid: `./datasets/text-to-text/ease/title-to-table/valid.tsv`
  - Test: `./datasets/text-to-text/ease/title-to-table/test.tsv`

Different from image generation from texts, you cannot directly use our WikiTIG datasets for table generation from images.
To use it, first you need to open the file `./datasets/scripts/download_images.sh` and edit the part
```
# https://meta.wikimedia.org/wiki/User-Agent_policy
USER_AGENT="Write your user agent here"
```
to specify your user agent. Note that without setting the user agent, your IP may be listed to the `robots.txt` in Wikipedia English.

After writing your user agent in the file `./datasets/scripts/download_images.sh`, you can download images by the following command.

```
cd datasets
./scripts/setup.sh
```

It takes several days to finish. Downloaded images will be converted to the data for table generation.
By the above procedure, you can use the contained files for table generation from title and images as follows:
- Table generation from title and images
  - Train: `./datasets/image-to-text/480/ease/image-to-table/train.tsv`
  - Valid: `./datasets/image-to-text/480/ease/image-to-table/valid.tsv`
  - Test: `./datasets/image-to-text/480/ease/image-to-table/test.tsv`

Note that the path to the dataset in each setting is represented as follows:
```
./datasets/image-to-text/${RESOLUTION}/${FORMAT}/${TASK}/${SPLIT}.tsv
```
- `${RESOLUTION}` denotes the resolution the images to be generated. You can choose `256`, `384`, or `480` in this dataset.
- `${FORMAT}` denotes the data format. You can choose `ease` or `exact` in this dataset. `exact` does not have empty captions `ease` has.
- `${TASK}` denotes the target task. You can choose `image-to-table` or `title-to-table` in this dataset.
- `${SPLIT}` denotes what split (e.g., `Train`, `Valid`, or `Test`) the file follows.

# Training & Inference

You can download our generated table and images from [here](https://drive.google.com/file/d/1-S85Q4C9GjkSsmhjkoCh0Vq3XgiHjytc/view?usp=sharing). However, if you desire, you can reproduce the results in our paper by the following commands. Note that all models are trained on three different initial seeds 0, 1, and 2.

## Table Generation

### Training

- Table Generation from titles (BART)
```
cd OFA/
bash scripts/bart_base/train/title-to-table.sh
```
The trained models are stored in `models/bart_base/title-to-table` as checkpoints.
- Table Generation from titles (OFA)
```
cd OFA/
bash scripts/ofa_base/train/title-to-table.sh
```
The trained models are stored in `models/ofa_base/title-to-table` as checkpoints.
- Table Generation from images
```
cd OFA/
bash scripts/ofa_base/train/image-to-table.sh
```
The trained models are stored in `models/ofa_base/image-to-table` as checkpoints.
- Table Generation from title and images
```
cd OFA/
bash scripts/ofa_base/train/image_and_title-to-table.sh
```
The trained models are stored in `models/ofa_base/image_and_title-to-table` as checkpoints.

### Inference

- Table Generation from titles (BART)
```
cd OFA/
bash scripts/bart_base/predict/title-to-table.sh
```
The generated tables are stored in `results/bart_base/title-to-table/{SEED}/test_predict.json`.
- Table Generation from titles (OFA)
```
cd OFA/
bash scripts/ofa_base/predict/title-to-table.sh
```
The generated tables are stored in `results/ofa_base/title-to-table/{SEED}/test_predict.json`.
- Table Generation from images
```
cd OFA/
bash scripts/ofa_base/predict/image-to-table.sh
```
The generated tables are stored in `results/ofa_base/image-to-table/{SEED}/test_predict.json`.
- Table Generation from title and images
```
cd OFA/
bash scripts/ofa_base/predict/image_and_title-to-table.sh
```
The generated tables are stored in `results/ofa_base/image-to-table/{SEED}/test_predict.json`.

### Evaluation

- Table Generation from titles (BART)
```
cd OFA/
bash scripts/bart_base/evaluate/title-to-table.sh
```
After the execution, you can see the evaluation result in `results/bart_base/title-to-table/eval.csv`.
- Table Generation from titles (OFA)
```
cd OFA/
bash scripts/ofa_base/evaluate/title-to-table.sh
```
After the execution, you can see the evaluation result in `results/ofa_base/title-to-table/eval.csv`.
- Table Generation from images
```
cd OFA/
bash scripts/ofa_base/evaluate/image-to-table.sh
```
After the execution, you can see the evaluation result in `results/ofa_base/image-to-table/eval.csv`.
- Table Generation from title and images
```
cd OFA/
bash scripts/ofa_base/evaluate/image_and_title-to-table.sh
```
After the execution, you can see the evaluation result in `results/ofa_base/image_and_title-to-table/eval.csv`.

## Image Generation

### Training

- Image Generation from captions
```
cd OFA
bash scripts/ofa_base/train/caption-to-image.sh
```
The trained models are stored in `models/ofa_base/caption-to-image` as checkpoints.
- Image Generation from caption and tables (Gold)
```
cd OFA
bash scripts/ofa_base/train/caption_and_table-to-image.sh
```
The trained models are stored in `models/ofa_base/caption_and_table-to-image` as checkpoints.

### Inference

- Image Generation from captions
```
cd OFA
bash scripts/ofa_base/predict/caption-to-image.sh
```
The generated images are stored in `results/ofa_base/caption-to-image/{SEED}/test/top1/`.
- Image Generation from caption and tables (Gold)
```
cd OFA
bash scripts/ofa_base/predict/caption_and_table-to-image.sh
```
The generated images are stored in `results/ofa_base/caption_and_table-to-image/{SEED}/test/top1/`.
- Image Generation from caption and tables (generated from BART)
```
cd OFA
bash scripts/ofa_base/predict/caption_and_bart_base_gen_table-to-image.sh
```
The generated images are stored in `results/ofa_base/caption_and_bart_base_gen_table-to-image/{SEED}/test/top1/`.
- Image Generation from caption and tables (generated from OFA)
```
cd OFA
bash scripts/ofa_base/predict/caption_and_ofa_base_gen_table-to-image.sh
```
The generated images are stored in `results/ofa_base/caption_and_ofa_base_gen_table-to-image/{SEED}/test/top1/`.

### Evaluation

- Image Generation from captions
```
cd OFA
bash scripts/ofa_base/evaluate/caption-to-image.sh
```
After the execution, you can see the evaluation result in `results/ofa_base/caption-to-image/eval.csv`.
- Image Generation from caption and tables (Gold)
```
cd OFA
bash scripts/ofa_base/evaluate/caption_and_table-to-image.sh
```
After the execution, you can see the evaluation result in `results/ofa_base/caption_and_table-to-image/eval.csv`.
- Image Generation from caption and tables (generated from BART)
```
cd OFA
bash scripts/ofa_base/evaluate/caption_and_bart_base_gen_table-to-image.sh
```
After the execution, you can see the evaluation result in `results/ofa_base/caption_and_bart_base_gen_table-to-image/eval.csv`.
- Image Generation from caption and tables (generated from OFA)
```
cd OFA
bash scripts/ofa_base/evaluate/caption_and_ofa_base_gen_table-to-image.sh
```
After the execution, you can see the evaluation result in `results/ofa_base/caption_and_ofa_base_gen_table-to-image/eval.csv`.

