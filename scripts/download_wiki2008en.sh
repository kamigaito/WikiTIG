#!/bin/bash

cd data
wget https://dumps.wikimedia.org/other/static_html_dumps/current/en/wikipedia-en-html.tar.7z
7z x wikipedia-en-html.tar.7z
tar -xf wikipedia-en-html.tar -C enwiki2008
wget https://dumps.wikimedia.org/other/static_html_dumps/current/en/html.lst
cd .. 
