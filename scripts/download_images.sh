#!/bin/bash

USER_AGENT="Write your user agent here"

cd extracted/
mkdir images
cd images
wget --user-agent="${USER_AGENT}" -i ../images.txt
cd ../../

