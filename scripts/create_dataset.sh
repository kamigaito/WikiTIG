#!/bin/bash

bash ./scripts/download_wiki2008en.sh

python ./scripts/page_list.py
python ./scripts/extract.py
python ./scripts/filtering.py

bash ./scripts/download_images.sh

bash ./scripts/crop.sh
bash ./scripts/resize.sh
bash ./scripts/conv_to_base64_cropped.sh
bash ./scripts/conv_to_base64_resized.sh

bash ./scripts/make_dataset_image-to-text.sh
bash ./scripts/split_for_image-to-text_gen.sh

bash ./scripts/make_dataset_text-to-text.sh

bash ./scripts/make_dataset_text-to-image.sh
bash ./scripts/split_for_text-to-image_gen.sh
bash ./scripts/copy_images.sh
