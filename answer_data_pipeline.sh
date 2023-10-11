LANG=AZ
PART=2

# Validation Sets 
# with Answers
# python answers2csv.py --input "/Users/dug/Py/wikiExtract2csv/Answer_Exports/"$LANG"_Answers_"$PART".csv" --output "/Users/dug/Py/wikiExtract2csv/Data/QA_"$LANG"_Val.csv" --answers --n_tasks 100
# without answers
# python answers2csv.py --input "/Users/dug/Py/wikiExtract2csv/Answer_Exports/"$LANG"_Answers_"$PART".csv" --output "/Users/dug/Py/wikiExtract2csv/Data/QA_"$LANG"_Val_"$PART"_no_labels.csv" --n_tasks 100

# Test Sets
# with Answers
# python answers2csv.py --input "/Users/dug/Py/wikiExtract2csv/Answer_Exports/"$LANG"_Answers_"$PART".csv" --output "/Users/dug/Py/wikiExtract2csv/Data/QA_"$LANG"_Test.csv" --from_n_on 101 --answers 
# without Answers
# python answers2csv.py --input "/Users/dug/Py/wikiExtract2csv/Answer_Exports/"$LANG"_Answers_"$PART".csv" --output "/Users/dug/Py/wikiExtract2csv/Data/QA_"$LANG"_Test_no_labels.csv"  --from_n_on 101

# Test Sets Normalized Lengths
# with Answers
python answers2csv.py --input "/Users/dug/Py/wikiExtract2csv/Answer_Exports/"$LANG"_Answers_"$PART".csv" --output "/Users/dug/Py/wikiExtract2csv/Data/QA_normalized/QA_"$LANG"_Test.csv" --answers #--from_n_on 101  --n_tasks 175 
# without Answers
python answers2csv.py --input "/Users/dug/Py/wikiExtract2csv/Answer_Exports/"$LANG"_Answers_"$PART".csv" --output "/Users/dug/Py/wikiExtract2csv/Data/QA_normalized/QA_"$LANG"_Test_no_labels.csv" # --from_n_on 101 --n_tasks 175