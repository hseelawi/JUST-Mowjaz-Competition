# Mowjaz just competition

## Evaluating 
To run the baseline model evaluation call `evaluate.py` script. It has the following arguments:

* `--input_file`: File path defining the evaluating file.
* `--model_dir`: (Optional) Directory defining the classifier and vectroizer (`models/` by default).
* `--output_dir`: (Optional) Directory path to save the prediction results (`outputs/` by default).
* `--model_type`: (Optional) Whether BiLstm model or SVM model (`SVM` by default).
* `--max_sentence_len`: (Optional) The number of tokens per sentence (`170` by default).
* `--normalize`: (Optional) Whether normalize the text or not (`True` by default).

Usage example:
```bash
python3 evaluate.py \
--input_file=<path_of_testing_file> \
--model_dir=<path_of_classifier_vectroizer>  \
--output_dir=<path_to_save_results> \
--model_type=BiLstm \
--output_dir=170 \
--normalize=True 
```

### Data Format
We assume that you will pass TSV file that contains `ID` column and the feature column name should be `Article`.

### Output Format
We provide a TSV file with the following columns:
- `ID` column represent the article id.
- Next 11 columns represent labels for each article `['فن ومشاهير','أخبار','رياضة','اقتصاد','تكنولوجيا', 'اسلام و أديان','سيارات','طقس','منوعات أخرى','صحة','مطبخ']`. For each article we have binary list consist of 11 item mapped to our labels each item either `0` means that we couldn't assign this class for the article `1` means that we could assign this class for the article.
