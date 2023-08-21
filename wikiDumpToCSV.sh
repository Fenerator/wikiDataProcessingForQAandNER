#!/bin/bash

# SETTINGS:
LANG="en" # TODO
LINK="https://dumps.wikimedia.org/enwiki/20230720/enwiki-20230720-pages-articles1.xml-p1p41242.bz2" # TODO
DUMP_FILE=$LANG"wiki-20230720-pages-articles.xml.bz2"
OUT_FOLDER="../../Documents/MRL_ST_2023/"$LANG"wiki_extracted" # TODO
# END SETTINGS

# download dump file
wget -nc $LINK -O $DUMP_FILE

# run wikiextractor
python -m wikiextractor.WikiExtractor $DUMP_FILE  --output $OUT_FOLDER

# filter, sample and save to csv
python wikiExtract2csv.py --input $OUT_FOLDER"/AA/" --output $OUT_FOLDER --sample_size 100 --min 1000

