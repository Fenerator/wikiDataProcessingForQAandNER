import os, argparse, csv
from pathlib import Path
from bs4 import BeautifulSoup


def dir_path(string):
    if os.path.isdir(string):
        return string
    else:
        raise NotADirectoryError(string)


def main(args):
    # find all files in the input directory
    input_dir = Path(args.input)
    output_dir = Path(args.output)
    print(f"Input directory: {input_dir}")
    print(f"Output file: {output_dir}")

    files = list(input_dir.iterdir())

    # create a new csv file
    outfile = open(output_dir, "w")
    writer = csv.writer(outfile, delimiter=",")
    writer.writerow(["id", "title", "url", "text"])

    max_articles = args.max

    counter = 0
    # for each file, read the contents
    for file in files:
        with open(file, "r") as f:
            data = f.read()

        soup = BeautifulSoup(data, "lxml")

        # split into articles
        articles = soup.find_all("doc")

        for article in articles:
            doc_id = article["id"]
            title = article["title"]
            url = article["url"]
            text = article.get_text().strip()

            assert len(text) > 0 and len(title) > 0 and len(url) > 0 and len(doc_id) > 0, f"Error in {file}: empty field in article {doc_id}, {url}"

            writer.writerow([doc_id, title, url, text])
            counter += 1
            print(f"Processed Article {counter} / {max_articles}")

            if counter == max_articles:
                outfile.close()
                exit()

    outfile.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--input", type=dir_path, required=True, help="file path to the wikiextractor output files, e.g. ../../Documents/alswiki/text/AA")
    parser.add_argument("--output", type=str, default="articles.csv", help="file path to the output csv file, e.g. ../../Documents/alswiki/text/articles.csv")

    parser.add_argument("--max", type=int, default=100, help="first n articles to extract (default: 100)")

    args = parser.parse_args()

    main(args)
