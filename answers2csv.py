import argparse
from pathlib import Path
import pandas as pd


def main(args):
    input_file = Path(args.input)
    assert input_file.is_file(), f"Input file {input_file} does not exist"

    output_file = Path(args.output)

    print(f"Input file: {input_file}")
    print(f"Output file: {output_file}")

    df = pd.read_csv(input_file, encoding="utf-8", dtype=str, on_bad_lines="skip")

    if args.answers:
        df_light = df[["id", "text", "question", "answer"]]
    else:
        df_light = df[["id", "text", "question"]]

    print(f"Number of answers: {len(df_light)}")
    print(f"Columns new: {df_light.columns}")

    df_light.to_csv(output_file, encoding="utf-8", index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--input", type=str, required=True, help="Path to the input csv file")
    parser.add_argument("--output", type=str, required=False, default="article_question_pairs.csv", help="file path to the output csv file, e.g. ../../Documents/alswiki/text/articles.csv")

    parser.add_argument("--answers", action="store_true", help="to include the answers (labels) in the output file")

    args = parser.parse_args()

    main(args)
