LANG=ALS
PART=1

# Validation Sets 
# with Answers
python answers2csv.py --input "/Users/dug/Py/wikiExtract2csv/Answer_Exports/"$LANG"_Answers_"$PART".csv" --output "/Users/dug/Py/wikiExtract2csv/Data/QA_"$LANG"_Val_"$PART".csv" --answers
# without answers
python answers2csv.py --input "/Users/dug/Py/wikiExtract2csv/Answer_Exports/"$LANG"_Answers_"$PART".csv" --output "/Users/dug/Py/wikiExtract2csv/Data/QA_"$LANG"_Val_"$PART"_no_labels.csv"

# Test Sets
# with Answers

# without Answers