#!/bin/bash -eu

ROOT=${PWD}
FILE_ID="1y2bOn6MBQCzvB2xbxK9k-S2gn_op0ZdJ"

gdown --id ${FILE_ID}
unzip ${ROOT}/datasets.zip
