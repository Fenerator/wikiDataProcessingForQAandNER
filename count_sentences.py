import pandas as pd
from pathlib import Path

sent_dir = Path("~/Py/wikiExtract2csv/NER_V2_Outputs/articles_sampled_NER_new_selection_yo.csv")
para_dir = Path("~/Py/wikiExtract2csv/NER_V2_Outputs/articles_sampled_QA_new_selection_yo.csv")

df_sent = pd.read_csv(sent_dir, encoding="utf-8", dtype=str, on_bad_lines="skip")
df_para = pd.read_csv(para_dir, encoding="utf-8", dtype=str, on_bad_lines="skip")

qids = df_sent["id"].tolist()

required_nr_q_ids = qids[:500]

print(len(required_nr_q_ids))

print(f"Last required qid: {required_nr_q_ids[-1]}")
