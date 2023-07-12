import argparse, csv, json
from pathlib import Path


def main(args):
    input_file = Path(args.input)
    assert input_file.is_file(), f"Input file {input_file} does not exist"

    output_file = Path(args.output)

    print(f"Input file: {input_file}")
    print(f"Output file: {output_file}")

    # create a new csv file
    outfile = open(output_file, "w")
    writer = csv.writer(outfile, delimiter=",")
    writer.writerow(["id", "title", "url", "text", "question"])

    # read labelstudio json snapshot data
    with open(input_file) as f:
        data = json.load(f)

    for task in data:
        questions = task["annotations"][0]["result"][0]["value"]["text"]  # TODO multiple annotators
        id = task["data"]["id"]
        url = task["data"]["url"]
        title = task["data"]["title"]
        text = task["data"]["text"]

        # create article - question pairs
        for q in questions:
            writer.writerow([id, title, url, text, q])

    outfile.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--input", type=str, required=True, help="...")
    parser.add_argument("--output", type=str, required=False, default="article_question_pairs.csv", help="file path to the output csv file, e.g. ../../Documents/alswiki/text/articles.csv")

    parser.add_argument("--max", type=int, default=100, help="...")

    args = parser.parse_args()

    main(args)
