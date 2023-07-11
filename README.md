# wikiExtract2csv

## Description

This is a simple python script to extract the content of a Wikipedia dump and save it as a csv file compatible with Label Studio.

- samples 100 articles randomly
- ...

## Usage

1. Download the [Wikipedia dump](https://dumps.wikimedia.org/) corresponding to the desired languge from e.g. [here for ALS](https://dumps.wikimedia.org/alswiki/20230701/), the required file for ALS is [https://dumps.wikimedia.org/alswiki/20230701/alswiki-20230701-pages-articles.xml.bz2](https://dumps.wikimedia.org/alswiki/20230701/alswiki-20230701-pages-articles.xml.bz2).
2. If not already installed, install Wiki Extractor: `pip install wikiextractor`
3. Run Wiki Extractor on the dump file, e.g.: `python -m wikiextractor.WikiExtractor alswiki-20230701-pages-articles.xml.bz2`
4. To convert the data to the required format, run this script on the output of Wiki Extractor: ...
4. ...

## Dependencies

- wikiextractor
- lxml
- ...
