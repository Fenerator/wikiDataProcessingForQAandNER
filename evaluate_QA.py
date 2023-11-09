import argparse, os
from pathlib import Path
import pandas as pd
import evaluate


def read_csv(file_path, args=None):
    if not (args.baseline or args.gpt):
        df = pd.read_csv(file_path, encoding="utf-8", dtype=str, on_bad_lines="skip")

        questions = df["question"].tolist()
        answers = df["answer"].tolist()
        ids = df["id"].tolist()

        assert (
            len(questions) == len(answers) == len(ids)
        ), f"Number of questions, answers and ids does not match in file {file_path}, len(questions)={len(questions)}, len(answers)={len(answers)}, len(ids)={len(ids)}"

        return questions, answers, df, ids

    elif args.baseline:
        try:
            df = pd.read_csv(
                file_path, encoding="utf-8", dtype=str, on_bad_lines="skip", sep="\t"
            )
            predictions = df["hyp"].tolist()
            labels = df["pred"].tolist()
            print(f"columns in df: {df.columns}")
        except KeyError:  # tsv was processed before and is now a csv actually
            df = pd.read_csv(
                file_path,
                encoding="utf-8",
                dtype=str,
                on_bad_lines="skip",
            )
            predictions = df["hyp"].tolist()
            labels = df["pred"].tolist()

        assert len(predictions) == len(
            labels
        ), f"Number of questions, answers does not match in file {file_path}, len(predictions)={len(predictions)}, len(labels)={len(labels)})"

        return predictions, labels, df

    elif args.gpt:
        df = pd.read_csv(
            file_path,
            encoding="utf-8",
            dtype=str,
            on_bad_lines="skip",
        )

        predictions = df["gpt-4"].tolist()
        labels = df["answer"].tolist()

        assert len(predictions) == len(
            labels
        ), f"Number of questions, answers does not match in file {file_path}, len(predictions)={len(predictions)}, len(labels)={len(labels)})"

        return predictions, labels, df


def calculate_chrf(predictions, labels):
    """calculate ChrF, there should be one reference sub-list for each prediction sentence."""
    chrf = evaluate.load("chrf")

    charf = [
        chrf.compute(predictions=[prediction], references=[[label]], word_order=0)[
            "score"
        ]
        for prediction, label in zip(predictions, labels)
    ]

    charf1 = [
        chrf.compute(predictions=[prediction], references=[[label]], word_order=1)[
            "score"
        ]
        for prediction, label in zip(predictions, labels)
    ]

    charf2 = [
        chrf.compute(predictions=[prediction], references=[[label]], word_order=2)[
            "score"
        ]
        for prediction, label in zip(predictions, labels)
    ]

    return charf, charf1, charf2


def calculate_rougeL(predictions, labels):
    rouge = evaluate.load("rouge")

    rougeL = [
        rouge.compute(predictions=[prediction], references=[[label]])["rougeL"]
        for prediction, label in zip(predictions, labels)
    ]

    return rougeL


def calculate_BERTScore(predictions, labels):
    bertscore = evaluate.load("bertscore")
    results = [
        bertscore.compute(
            predictions=[prediction], references=[label], model_type="roberta-base"
        )["f1"].pop()
        for prediction, label in zip(predictions, labels)
    ]

    return results


def main(args):
    prediction_file = Path(args.predictions)
    assert (
        prediction_file.is_file()
    ), f"Predictions file {prediction_file} does not exist"

    label_file = Path(args.labels)
    assert label_file.is_file(), f"Labels file {label_file} does not exist"

    results_file = Path(args.results)
    os.makedirs(results_file.parent, exist_ok=True)
    f = open(results_file, "a", encoding="utf-8")

    print(f"Prediction file: {prediction_file}")
    print(f"Label file: {label_file}")
    print(f"Results file: {results_file}")

    # file reading
    if args.baseline or args.gpt:
        predictions_a, labels_a, df_pred = read_csv(prediction_file, args)
    else:
        _, predictions_a, df_pred, predictions_ids = read_csv(prediction_file, args)
        _, labels_a, _, labels_ids = read_csv(label_file, args)

        for i in range(len(predictions_ids)):
            assert predictions_ids[i] == labels_ids[i], f"IDs do not match at index {i}"

    print(f"Number of tasks: {len(df_pred)}")

    # calculate metrics
    chrf_results, chrf1_results, charf2_results = calculate_chrf(
        predictions_a, labels_a
    )

    f.write(
        f"{prediction_file.parent.name}/{prediction_file.stem}{prediction_file.suffix}\n"
    )
    # store per sentence results in file
    df_pred["score_chrf"] = chrf_results
    df_pred["score_chrf+"] = chrf1_results
    df_pred["score_chrf++"] = charf2_results

    f.write(f"ChrF ('char_order': 6, 'word_order': 0, 'beta': 2)\t")
    f.write(f"ChrF+ ('char_order': 6, 'word_order': 1, 'beta': 2)\t")
    f.write(f"ChrF++ ('char_order': 6, 'word_order': 2, 'beta': 2)\t")
    f.write(f"RougeL\t")
    f.write(
        f"BERTScore F1 ('hashcode': 'roberta-base_L10_no-idf_version=0.3.12(hug_trans=4.34.0)\t\n"
    )

    f.write(f"{sum(chrf_results) / len(chrf_results)}\t")
    f.write(f"{sum(chrf1_results) / len(chrf1_results)}\t")
    f.write(f"{sum(charf2_results) / len(charf2_results)}\t")

    rougeL_results = calculate_rougeL(predictions_a, labels_a)
    f.write(f"{sum(rougeL_results) / len(rougeL_results)}\t")
    df_pred["score_rougeL"] = rougeL_results

    bertScore_results = calculate_BERTScore(predictions_a, labels_a)
    f.write(
        f"{sum(bertScore_results) / len(bertScore_results)}\t\n===================\n"
    )
    df_pred["score_BERTScoreF1"] = bertScore_results

    # save metrics to file
    df_pred.to_csv(prediction_file, index=False)

    # results per language and system, each seperatly

    # aggregate to get results per language, and per system
    # results per language, weighted by number of sentences per language

    # results per system

    # sample random sentences from each language and system, and store in file


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--predictions",
        type=str,
        required=True,
        help="Path to the input csv file containing the predictions (answers)",
    )
    parser.add_argument(
        "--labels",
        type=str,
        required=True,
        default="article_question_pairs.csv",
        help="Path to the input csv file containing the true labels (answers)",
    )

    parser.add_argument(
        "--results",
        type=str,
        required=True,
        help="Path where the average results should be stored",
    )

    parser.add_argument(
        "--baseline",
        action="store_true",
        help="Whether the predictions are from the baseline system, changes the input file format",
    )
    parser.add_argument(
        "--gpt",
        action="store_true",
        help="Whether the predictions are from the GPT baseline system, changes the input file format",
    )

    args = parser.parse_args()

    main(args)
