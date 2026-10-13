"""
Data Processing Pipeline - CLI

DS 3500 - MP1

Usage:
    python pipeline.py --input fixtures/sample_data.csv --output output/clean.csv --config config/config.yaml
    python pipeline.py --input fixtures/sample_data.csv --output output/clean.csv --config config/config.yaml --verbose
"""

import argparse
import logging
import sys
from pprint import pprint

from src import (
    create_cleaning_report,
    load_data,
    process_data,
    save_data,
    setup_logging,
    validate_dataframe,
    validate_input,
)


logger = logging.getLogger(__name__)


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Data processing pipeline"
    )
    parser.add_argument(
        "--input",
        "-i",
        required=True,
        help="Path to the input file"
    )
    parser.add_argument(
        "--config",
        required=True,
        help="Path to the YAML configuration file"
    )
    parser.add_argument(
        "--output",
        "-o",
        required=True,
        help="Path to the output file"
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose logging"
    )
    return parser.parse_args()


def main():
    """Main pipeline function."""
    args = parse_arguments()
    setup_logging(args.verbose)
    logger.debug(
        f"Arguments parsed: input={args.input}, "
        f"output={args.output}, config={args.config}"
    )

    if not validate_input(args.input):
        sys.exit(1)
    if not validate_input(args.config):
        sys.exit(1)

    try:
        df = load_data(args.input)
        config = load_data(args.config)
    except ValueError:
        sys.exit(1)

    # Read the validation settings from the config
    required_columns = config["validation"]["required_columns"]
    numeric_columns = config["validation"]["numeric_columns"]

    rows_loaded = len(df)
    try:
        df = validate_dataframe(df, required_columns, numeric_columns)
    except ValueError:
        sys.exit(1)
    logger.info(f"Validation complete: {rows_loaded} -> {len(df)} rows")

    # Save a copy of the validated DataFrame
    df_original = df.copy()

    try:
        df = process_data(df, config)
    except ValueError:
        sys.exit(1)
    logger.info(f"Processing complete: {len(df_original)} -> {len(df)} rows")

    output_path = save_data(df, args.output)
    logger.info(f"Saved cleaned data to {output_path}")

    report = create_cleaning_report(df_original, df)
    print("\nCleaning report:")
    pprint(report, sort_dicts=False)


if __name__ == "__main__":
    main()