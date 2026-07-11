"""
===========================================================
Civil Registration Data Quality Engine (CRDQE)

Entry Point

Author:
Benard Mandera
===========================================================
"""

from crdqe.core.config_manager import ConfigManager
from crdqe.core.logger import Logger
from crdqe.core.file_manager import FileManager
from crdqe.core.excel_reader import ExcelReader
from crdqe.core.header_detector import HeaderDetector
from crdqe.utils.column_standardizer import ColumnStandardizer
from crdqe.core.schema_mapper import SchemaMapper
from crdqe.core.dataset_detector import DatasetDetector
from crdqe.core.schema_validator import SchemaValidator
from crdqe.core.datatype_processor import DataTypeProcessor
from crdqe.core.rule_loader import RuleLoader
from crdqe.core.rule_engine import RuleEngine
from crdqe.core.issue_collector import IssueCollector
from crdqe.core.summary_builder import SummaryBuilder
from crdqe.core.excel_writer import ExcelWriter
from pathlib import Path

def main():

    # -------------------------------------------------------
    # Load configuration
    # -------------------------------------------------------

    settings = ConfigManager().load()

    logger = Logger.setup()

    logger.info("=" * 60)
    logger.info("Civil Registration Data Quality Engine Started")

    # -------------------------------------------------------
    # File management
    # -------------------------------------------------------

    file_manager = FileManager(settings)
    file_manager.create_directories()

    if not file_manager.workbook_exists():
        logger.error(f"Workbook not found: {file_manager.get_input_file()}")
        return

    logger.info("Workbook found.")
    logger.info(file_manager.get_input_file())

    # -------------------------------------------------------
    # Read workbook
    # -------------------------------------------------------

    reader = ExcelReader(
        workbook_path=file_manager.get_input_file(),
        worksheet=settings["input"]["worksheet"],
    )

    logger.info(f"Available worksheets: {reader.get_sheet_names()}")

    header_row = HeaderDetector.find_header_row(
        file_manager.get_input_file(),
        settings["input"]["worksheet"],
    )

    logger.info(f"Detected Header Row: {header_row}")

    df = reader.read(header=header_row)

    # -------------------------------------------------------
    # Standardize columns
    # -------------------------------------------------------

    df.columns = ColumnStandardizer.clean(df.columns)

    logger.info("Standardized Columns:")
    logger.info(df.columns.tolist())

    # -------------------------------------------------------
    # Detect dataset
    # -------------------------------------------------------

    dataset = DatasetDetector.detect(df.columns)

    logger.info(f"Detected Dataset: {dataset}")

    # -------------------------------------------------------
    # Map schema
    # -------------------------------------------------------

    BASE_DIR = Path(__file__).parent

    if dataset == "Birth":
        schema_file = BASE_DIR / "config" / "birth_schema.yaml"
    elif dataset == "Death":
        schema_file = BASE_DIR / "config" / "death_schema.yaml"
    else:
        raise ValueError(f"Unknown dataset: {dataset}")

    mapper = SchemaMapper(schema_file)

    df = mapper.map_columns(df)

    schema = mapper.get_schema()

    # -------------------------------------------------------
    # Detect dataset
    # -------------------------------------------------------

    dataset = DatasetDetector.detect(df.columns)

    logger.info(f"Detected Dataset: {dataset}")

    # -------------------------------------------------------
    # Convert datatypes
    # -------------------------------------------------------

    df = DataTypeProcessor.process(df, schema)

    # -------------------------------------------------------
    # Validate schema
    # -------------------------------------------------------

    validator = SchemaValidator()

    result = validator.validate(df, schema)

    logger.info(f"Schema Valid: {result['valid']}")

    if result["missing"]:
        logger.warning(f"Missing Columns: {result['missing']}")

    if result["extra"]:
        logger.info(f"Extra Columns: {result['extra']}")

    logger.info("Workbook loaded successfully.")

    logger.info(f"Rows: {len(df)}")
    logger.info(f"Columns: {len(df.columns)}")
    logger.info(df.columns.tolist())

    # -------------------------------------------------------
    # Load rules
    # -------------------------------------------------------

    rules = RuleLoader.load(dataset, schema)

    engine = RuleEngine(
        rules=rules,
        logger=logger,
    )

    # -------------------------------------------------------
    # Run validation
    # -------------------------------------------------------

    df, issues_df = engine.run(df)

    collector = IssueCollector()
    collector.add(issues_df)

    logger.info("Rule Engine completed.")
    logger.info(f"Records processed: {len(df)}")
    logger.info(f"Issues found: {collector.count()}")

    # -------------------------------------------------------
    # Build summary
    # -------------------------------------------------------

    summary = SummaryBuilder.build(
        df,
        issues_df,
    )

    # -------------------------------------------------------
    # Write reports
    # -------------------------------------------------------

    writer = ExcelWriter(settings)

    writer.cleaned(df)
    writer.flags(issues_df)
    writer.summary(summary)

    logger.info("=" * 60)
    logger.info("CRDQE Finished Successfully")


if __name__ == "__main__":
    main()
