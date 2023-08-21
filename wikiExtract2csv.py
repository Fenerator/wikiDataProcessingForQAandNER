import os, argparse, csv
from pathlib import Path
from bs4 import BeautifulSoup
from nltk.tokenize import sent_tokenize


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


def extraction(args):
    # find all files in the input directory
    input_dir = Path(args.input)
    output_dir = Path(args.output)

    # create the output directory if it does not exist
    output_dir.mkdir(parents=True, exist_ok=True)

    if args.split_by == "sentence":
        output_file = output_dir / "articles_sampled_NER.csv"
    elif args.split_by == "paragraph":
        output_file = output_dir / "articles_sampled_QA.csv"

    print(f"Input directory: {input_dir}")
    print(f"Output file: {output_file}")
    print(f"Generating {args.split_by} samples of {args.sample_size} articles with a minimum length of {args.min} characters")

    files = list(input_dir.iterdir())

    # create a new csv file
    outfile = open(output_file, "w")
    writer = csv.writer(outfile, delimiter=",")
    writer.writerow(["id", "sub_id", "title", "url", "text"])

    sample_size = args.sample_size
    min_article_length = args.min

    counter = 0
    # for each file, read the contents
    for file in files:
        with open(file, "r") as f:
            data = f.read()

        soup = BeautifulSoup(data, "lxml")

        # split into articles
        articles = soup.find_all("doc")

        for article in articles:
            sub_id = 0
            doc_id = article["id"]
            title = article["title"]
            url = article["url"]
            text = article.get_text().strip()

            assert len(text) > 0 and len(title) > 0 and len(url) > 0 and len(doc_id) > 0, f"Error in {file}: empty field in article {doc_id}, {url}"

            # require a minimum length of the article
            if len(text) > min_article_length:
                # split the article into parts (sentences or paragraphs)
                text_parts = split_text(text, args.split_by)

                for text in text_parts:
                    writer.writerow([doc_id, sub_id, title, url, text])
                    sub_id += 1

                counter += 1
                print(f"Processed Article {counter} / {sample_size}")

            if counter == sample_size:
                outfile.close()
                return True

    outfile.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--input", type=dir_path, required=True, help="file path to the wikiextractor output files, e.g. ../../Documents/alswiki/text/AA")
    parser.add_argument("--output", type=str, default="articles.csv", help="directory where to save the output csv files, e.g. ../../Documents/alswiki/text/")

    parser.add_argument("--sample_size", type=int, default=100, help="first n articles to extract (default: 100)")

    parser.add_argument("--min", type=int, default=1000, help="minimal length in characters of each article (default: 200)")

    parser.add_argument("--split_by", default="both", help="select how to split the articles, e.g. 'sentence' or 'paragraph'")
    args = parser.parse_args()
    print(args.split_by)
    if args.split_by == "both":
        """generate two csv files, one for NER and one for QA"""
        # NER
        args.split_by = "sentence"
        extraction(args)

        # QA
        args.split_by = "paragraph"
        extraction(args)

    else:
        extraction(args)
