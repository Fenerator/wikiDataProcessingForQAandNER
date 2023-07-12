# wikiExtract2csv

## Description

This is a simple python script to extract the content of a Wikipedia dump and save it as a csv file compatible with Label Studio.

- by default, it samples the firest 100 articles from the dump
- it extracts the title, id, url, and text of each article

## Getting started

1. Download the [Wikipedia dump](https://dumps.wikimedia.org/) corresponding to the desired languge from e.g. [here for ALS](https://dumps.wikimedia.org/alswiki/20230701/), the required file for ALS is [https://dumps.wikimedia.org/alswiki/20230701/alswiki-20230701-pages-articles.xml.bz2](https://dumps.wikimedia.org/alswiki/20230701/alswiki-20230701-pages-articles.xml.bz2). The corresponding file on the site [https://dumps.wikimedia.org/alswiki/20230701/](https://dumps.wikimedia.org/alswiki/20230701/):
<img width="743" alt="image" src="https://github.com/Fenerator/wikiExtract2csv/assets/33670163/01e9561d-0860-46c4-9b7e-6bdd07914b9e">


3. Run Wiki Extractor on the downloaded dump file, e.g.: `python -m wikiextractor.WikiExtractor alswiki-20230701-pages-articles.xml.bz2`
4. To convert the data to the required format, run the script [wikiExtract2csv.py](wikiExtract2csv.py) on the output generated in step 2.

## Usage

```python
python wikiExtract2csv.py --input INPUT_DIR [--output OUTPUT_DIR] [--max SAMPLE_SIZE]
```

- `INPUT_DIR`: path to the directory containing the output of Wiki Extractor.
- `OUTPUT_DIR`: path to the directory where the output csv file will be saved, default is `./articles.csv`
- `SAMPLE_SIZE`: number of articles to sample from the input, default is `100`

### Example usage

```python
python wikiExtract2csv.py --input "../../Documents/alswiki/text/AA/" --output "../../Documents/alswiki/articles.csv" --max 100
```

## Dependencies

- Python 3.9.12
- other dependencies are listed in [requirements.txt](requirements.txt)
