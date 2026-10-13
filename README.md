# MP1 Data Pipeline

This command-line pipeline loads a CSV file together with a YAML configuration file, validates the data, cleans it, and saves the result as a new CSV file. Data moves through the pipeline in order: load, validate, process, and save, and a cleaning report summarizing the changes is printed at the end. `pipeline.py` parses the command-line arguments and coordinates each step, while all reusable code is in the `src/` package. `data_loaders.py` reads CSV, JSON, and YAML files based on their extension, and `data_validator.py` checks that required columns exist and removes rows with invalid numeric values. `data_processor.py` removes duplicates, handles missing values, and removes outliers according to the settings in `config/config.yaml`, and `data_output.py` saves the cleaned dataframe. `utils.py` provides the logging setup and input file validation. Test data is stored in `fixtures/`, and generated results are written to `output/`, which is ignored by Git.

## Example

```bash
python pipeline.py --input fixtures/sample_data.csv --output output/clean.csv --config config/config.yaml --verbose
```

Output:

```text
23:31:45 DEBUG    __main__ — Arguments parsed: input=fixtures/sample_data.csv, output=output/clean.csv, config=config/config.yaml
23:31:45 INFO     src.utils — Input file validated: fixtures/sample_data.csv
23:31:45 INFO     src.utils — Input file validated: config/config.yaml
23:31:45 INFO     src.data_loaders — Loaded CSV file: fixtures\sample_data.csv (100 rows)
23:31:45 INFO     src.data_loaders — Loaded YAML file: config\config.yaml
23:31:45 WARNING  src.data_validator — Invalid numeric value in rating at row 94: not_available
23:31:45 WARNING  src.data_validator — Invalid numeric value in rating at row 95: error
23:31:45 WARNING  src.data_validator — Removed 2 rows with invalid numeric values in rating
23:31:45 DEBUG    src.data_validator — Validation: 100 -> 98 rows
23:31:45 INFO     __main__ — Validation complete: 100 -> 98 rows
23:31:45 DEBUG    src.data_processor — remove_duplicates: 98 -> 96 rows
23:31:45 DEBUG    src.data_processor — handle_missing: 96 -> 94 rows
23:31:45 DEBUG    src.data_processor — rating: method=iqr, threshold=1.5, removed=2
23:31:45 INFO     __main__ — Processing complete: 98 -> 92 rows
23:31:45 DEBUG    src.data_output — Saved 92 rows to output\clean.csv
23:31:45 INFO     __main__ — Saved cleaned data to output\clean.csv

Cleaning report:
{'rows_before': 98,
 'rows_after': 92,
 'rows_removed': 6,
 'columns_before': 5,
 'columns_after': 5,
 'columns_removed': 0}
```