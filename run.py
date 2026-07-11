"""
===========================================================
Civil Registration Data Quality Engine (CRDQE)

Entry Point

Author:
Benard Mandera
===========================================================
"""

from csv import reader, writer
from logging import config

from crdqe.core import logger
from crdqe.core import file_manager
from crdqe.core.config_manager import ConfigManager
from crdqe.core.file_manager import FileManager
from crdqe.core.issue_collector import IssueCollector
from crdqe.core.logger import Logger
from crdqe.core.excel_reader import ExcelReader
from crdqe.core.excel_writer import ExcelWriter
from crdqe.core.dataset_detector import DatasetDetector
from crdqe.core.header_detector import HeaderDetector
from crdqe.core.rule_loader import RuleLoader
from crdqe.death import schema
from crdqe.utils.column_standardizer import ColumnStandardizer
from crdqe.core.schema_mapper import SchemaMapper
from crdqe.core.schema_validator import SchemaValidator
from crdqe.core.rule_engine import RuleEngine
from crdqe.core.schema_manager import SchemaManager
from crdqe.core.summary_builder import SummaryBuilder


def main():

    # Load configuration
    config = ConfigManager()
    settings = config.load()      # <-- MUST happen first
    print(settings)
    print(type(settings))

    # Setup logger
    logger = Logger.setup()
    logger.info("=" * 60)
    logger.info("Civil Registration Data Quality Engine Started")

    file_manager = FileManager(settings)
    file_manager.create_directories()

    if not file_manager.workbook_exists():
        logger.error(f"Workbook not found: {file_manager.get_input_file()}")
        return

    logger.info("Workbook found.")
    logger.info(file_manager.get_input_file())

    reader = ExcelReader(
        workbook_path=file_manager.get_input_file(),
        worksheet=settings["input"]["worksheet"]
    )

    logger.info(f"Available worksheets: {reader.get_sheet_names()}")

    header_row = HeaderDetector.find_header_row(
        file_manager.get_input_file(),
        settings["input"]["worksheet"]
    )

    logger.info(f"Detected Header Row: {header_row}")

    df = reader.read(header=header_row)
    df.columns = ColumnStandardizer.clean(df.columns)

    logger.info("Standardized Columns:")
    logger.info(df.columns.tolist())

    mapper = SchemaMapper("config/birth_schema.yaml")
    df = mapper.map_columns(df)
    
    logger.info("Mapped Columns:")
    logger.info(df.columns.tolist())
    logger.info(f"Rows: {len(df)}")
    logger.info(f"Columns: {len(df.columns)}")
    logger.info(f"Column Names: {list(df.columns)}")
   


    validator = SchemaValidator()
    result = validator.validate(df, mapper.get_schema())

    logger.info(f"Schema Valid: {result['valid']}")
    if result.get("missing"):
        logger.warning(f"Missing Columns: {result['missing']}")
    if result.get("extra"):
        logger.info(f"Extra Columns: {result['extra']}")

    logger.info(f"Workbook loaded successfully.")
    dataset = DatasetDetector.detect(df.columns)
    logger.info(f"Detected Dataset: {dataset}")

    schema = SchemaManager(mapper.get_schema())
    logger.info(type(schema))
    logger.info(type(getattr(schema, 'schema', None)))
    logger.info(getattr(schema, 'schema', {}).keys())

    rules = RuleLoader.load(dataset, schema)

    engine = RuleEngine(rules=rules, logger=logger)
    collector = IssueCollector()

    df, issues = engine.run(df)
    collector.add(issues)

    logger.info("Rule Engine completed.")
    logger.info(f"Records processed: {len(df)}")
    logger.info(f"Issues found: {collector.count()}")
    df, issues_df = engine.run(df)

    summary = SummaryBuilder.build(df, issues_df)

    writer = ExcelWriter(settings)

    writer.cleaned(df)
    writer.flags(issues_df)
    writer.summary(summary)
if __name__ == "__main__": main()