import argparse, re
from pathlib import Path
import pandas as pd


def main(args):
    input_file = Path(args.input)
    assert input_file.is_file(), f"Input file {input_file} does not exist"

    output_file = Path(args.output)

    print(f"Input file: {input_file}")
    print(f"Output file: {output_file}")

    with open(input_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    print(f"Number of lines: {len(lines)}")

    with open(output_file, "w", encoding="utf-8") as f:
        # remove date tags
        pattern = r"\w-DATE$"
        for line in lines:
            new_line = re.sub(pattern, "O", line)
            f.write(new_line)

    # remove labels
    output_file_no_labels = Path(f"{output_file.parent}/{output_file.stem}_no_labels{output_file.suffix}")
    with open(output_file_no_labels, "w", encoding="utf-8") as f:
        # remove labels
        pattern = r"-X-\s\_\s\w.*$"  # remove this -X- _ O
        for line in lines:
            new_line = re.sub(pattern, "-X- _", line)
            f.write(new_line)

    print(f"Preprocessing Done")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--input", type=str, required=True, help="Path to the input csv file")
    parser.add_argument("--output", type=str, required=False, default="article_question_pairs.csv", help="file path to the output csv file, e.g. ../../Documents/alswiki/text/articles.csv")

    args = parser.parse_args()

    main(args)
