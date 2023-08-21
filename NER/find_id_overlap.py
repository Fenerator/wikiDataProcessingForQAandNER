import pandas as pd
from pathlib import Path

NER_dir = Path("NER/lang_biography")

# concatenate all csv files
files = list(NER_dir.iterdir())
csv_files = [file for file in files if file.suffix == ".csv"]
dfs = [pd.read_csv(df, encoding="utf-8", dtype=str, on_bad_lines="skip") for df in csv_files]
df_concat = pd.concat(dfs, ignore_index=True)

# group by qid to get frequent ids
print(df_concat.columns)
df_grouped = df_concat.groupby("qid")["qid"].count().sort_values(ascending=False)
frequent_qids = df_grouped.index.tolist()

print(frequent_qids[:10])
# save to csv
# df_grouped.to_csv("NER/lang_biography/NER_qid_counts.csv", encoding="utf-8", index=True, header=True)
