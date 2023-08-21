from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import os, argparse, csv
from pathlib import Path
from bs4 import BeautifulSoup
from nltk.tokenize import sent_tokenize
import pandas as pd


def get_qid_overlap(NER_dir, args):
    # concatenate all csv files
    files = list(NER_dir.iterdir())
    csv_files = [file for file in files if file.suffix == ".csv"]
    dfs = [pd.read_csv(df, encoding="utf-8", dtype=str, on_bad_lines="skip") for df in csv_files]
    df_concat = pd.concat(dfs, ignore_index=True)

    # group by qid to get frequent ids
    df_grouped = df_concat.groupby("qid")["qid"].count().sort_values(ascending=False)
    frequent_qids = df_grouped.index.tolist()

    # keep as many articles as the sample size requires
    frequent_qids = frequent_qids[: args.sample_size]

    return frequent_qids


def get_text_from_url(url, verbose=True):
    if verbose:
        print(f"Processing {url}")

    # Specify url of the web page
    source = urlopen(url).read()

    # Make a soup
    soup = BeautifulSoup(source, "lxml")

    # remove occurances of tables
    [table.decompose() for table in soup.find_all("table")]

    # get the title
    title = soup.find("h1").text

    # Extract the plain text content from paragraphs
    paras = []
    for paragraph in soup.find_all("p"):
        text = str(paragraph.text)
        if len(text) > 55:
            paras.append(text)

    # Interleave paragraphs & headers
    text = "\n".join(paras)

    # Drop footnote superscripts in brackets
    text = re.sub(r"\[.*?\]+", "", text)

    return title, text


def dir_path(string):
    if os.path.isdir(string):
        return string
    else:
        raise NotADirectoryError(string)


def split_text(text, split_by, sent_threshold=60):
    """splits the text into parts according to the split_by parameter

    Args:
        text (str): text extracted by wikiextractor
        split_by (str): paragraph or sentence splitting
        sent_threshold (int, optional): used to filter out headings and subheadings in the text. Assumes lines below threshold are titles, else it is a sentence / paragraph. Defaults to 60.

    Returns:
        _type_: text splitted into parts according to the split_by parameter
    """

    if split_by == "sentence":  # NER
        # split into sentences using nltk sentence tokenizer
        text_parts = sent_tokenize(text)

    elif split_by == "paragraph":  # QA
        # split into paragraphs
        text_parts = text.split("\n")

    else:
        # no splitting
        text_parts = [text]

    # remove empty paragraphs and paragraphs that are too short (e.g. titles)
    text_parts = [part.strip() for part in text_parts if (len(part.strip()) > 0 and len(part.strip()) > sent_threshold)]

    return text_parts


def extraction(args, frequent_qids):
    # find all files in the input directory
    input_file = Path(args.input)
    output_dir = Path(args.output)

    # create the output directory if it does not exist
    output_dir.mkdir(parents=True, exist_ok=True)

    if args.split_by == "sentence":
        output_file = output_dir / "articles_sampled_NER_new_selection.csv"
    elif args.split_by == "paragraph":
        output_file = output_dir / "articles_sampled_QA_new_selection.csv"

    print(f"Input file: {input_file}")
    print(f"Output file: {output_file}")
    print(f"Generating {args.split_by} samples of {args.sample_size} articles with a minimum length of {args.min} characters")

    # create a new csv file
    outfile = open(output_file, "w")
    writer = csv.writer(outfile, delimiter=",")
    writer.writerow(["id", "sub_id", "title", "url", "text"])

    sample_size = args.sample_size
    min_article_length = args.min

    counter = 0

    # get data from the input file (language biography file)
    url_df = pd.read_csv(input_file, encoding="utf-8", dtype=str, on_bad_lines="skip")
    links = url_df["wiki_url"].tolist()
    qids = url_df["qid"].tolist()

    # TODO sort both such that the frequent qids appear first

    for link, qid in zip(links, qids):
        sub_id = 0
        doc_id = qid
        url = link

        title, text = get_text_from_url(link)

        assert len(text) > 0 and len(title) > 0 and len(url) > 0 and len(doc_id) > 0, f"Error in {input_file}: empty field in article {doc_id}, {url}"

        # require a minimum length of the article
        if len(text) > min_article_length:
            # split the article into parts (sentences or paragraphs)
            text_parts = split_text(text, args.split_by)

            for text in text_parts:
                writer.writerow([doc_id, sub_id, title, url, text])  # WAS OLD VERSION
                sub_id += 1

            counter += 1
            print(f"Processed Article {counter} / {sample_size}")

        if counter == sample_size:
            outfile.close()
            return True

    outfile.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--input", type=str, required=True, help="file path to the links of the language biograpy file, e.g. ../../Documents/alswiki/text/AA")
    parser.add_argument("--output", type=str, default="articles.csv", help="directory where to save the output csv files, e.g. ../../Documents/alswiki/text/")

    parser.add_argument("--sample_size", type=int, default=100, help="first n articles to extract (default: 100)")  # TODO

    parser.add_argument("--min", type=int, default=1000, help="minimal length in characters of each article (default: 200)")

    parser.add_argument("--split_by", default="both", help="select how to split the articles, e.g. 'sentence' or 'paragraph'")
    args = parser.parse_args()
    print(args.split_by)

    # get the q_ids with the most overlap between all langauges
    NER_dir = Path("NER/lang_biography")
    frequent_qids = get_qid_overlap(NER_dir, args)

    if args.split_by == "both":
        """generate two csv files, one for NER and one for QA"""
        # NER
        args.split_by = "sentence"
        extraction(args, frequent_qids)

        # QA
        args.split_by = "paragraph"
        extraction(args, frequent_qids)

    else:
        extraction(args, frequent_qids)
