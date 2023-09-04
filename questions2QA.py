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
    writer.writerow(["id", "title", "url", "text", "question", "Q_Annotator"])

    # read labelstudio json snapshot data
    with open(input_file) as f:
        data = json.load(f)

    nr_questions = 0
    for task in data:
        if task["annotations"] == []:
            print(f"WARNING: no annotations for task {task['id']}")
            continue
        try:
            q_annotator = task["annotations"][0]["completed_by"]["email"]
            questions = task["annotations"][0]["result"][0]["value"]["text"]  # TODO multiple annotators on same task?

            id = task["data"]["id"]
            url = task["data"]["url"]
            title = task["data"]["title"]
            text = task["data"]["text"]
        except:
            print(f"Error: {task}")
        # create article - question pairs

        for q in questions:
            writer.writerow([id, title, url, text, q, q_annotator])
            nr_questions += 1

    outfile.close()

    print(f"Number of questions: {nr_questions}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--input", type=str, required=True, help="...")
    parser.add_argument("--output", type=str, required=False, default="article_question_pairs.csv", help="file path to the output csv file, e.g. ../../Documents/alswiki/text/articles.csv")

    parser.add_argument("--max", type=int, default=100, help="...")

    args = parser.parse_args()

    main(args)
