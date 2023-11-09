import argparse, re
from pathlib import Path


def extract_tags(lines):
    pattern = r"-X-\s\_\s(\w.*)$"

    tags = []
    for l in lines:
        try:
            tag = re.search(pattern, l).group(1)
            tags.append(tag)
        except AttributeError:
            tags.append("")

    return tags


def main(args):
    prediction_file = Path(args.predictions)
    assert (
        prediction_file.is_file()
    ), f"Predictions file {prediction_file} does not exist"

    label_file = Path(args.labels)
    assert label_file.is_file(), f"Labels file {label_file} does not exist"

    output_file = Path(args.output)

    print(f"Prediction file: {prediction_file}")
    print(f"Label file: {label_file}")
    print(f"Output file: {output_file}")

    # Extract tags for predictions and labels
    with open(prediction_file, "r", encoding="utf-8") as f:
        prediction_lines = f.readlines()
        predictions = extract_tags(prediction_lines)

    # for the sake of completeness and validation: are not actually used
    with open(label_file, "r", encoding="utf-8") as f:
        label_lines = f.readlines()
        labels = extract_tags(label_lines)

    assert len(label_lines) == len(
        prediction_lines
    ), f"Number of lines does not match labels: {len(label_lines)} predictions: {len(prediction_lines)}"
    assert len(predictions) == len(
        labels
    ), f"Number of predictions ({len(predictions)}) does not match number of labels ({len(labels)})"
    assert len(label_lines) == len(
        predictions
    ), f"Number of lines does not match the number of predictions"

    # Create output file for conlleval
    with open(output_file, "w", encoding="utf-8") as f:
        for label, prediction in zip(label_lines, predictions):
            f.write(f"{label.strip()} {prediction.strip()}\n")

    print(f"Done. Number of lines: {len(label_lines)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--predictions",
        type=str,
        required=True,
        help="Path to the input conll file containing the predictions",
    )
    parser.add_argument(
        "--labels",
        type=str,
        required=True,
        default="article_question_pairs.csv",
        help="Path to the input conll file containing the true laebels",
    )

    parser.add_argument(
        "--output",
        type=str,
        required=True,
        help="Path to the output file, containing the labels and predictions",
    )

    args = parser.parse_args()

    main(args)
