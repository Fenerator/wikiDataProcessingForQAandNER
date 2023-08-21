#!/bin/bash

# SETTINGS:
LANG="en" # TODO
OUT_FOLDER="../../Documents/MRL_ST_2023/"$LANG"wiki_extracted" # TODO
# END SETTINGS

# scrape, filter, sample and save to csv
python get_text_from_url.py --input "/Users/dug/Py/wikiExtract2csv/NER/lang_biography/"$LANG".csv" --output $OUT_FOLDER --sample_size 100 --min 1000

