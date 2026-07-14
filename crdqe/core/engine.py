from pathlib import Path

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
from crdqe.core.excel_writer import ExcelWriter
from crdqe.reporting.summary_report import SummaryReport
from crdqe.reports.issue_statistics import IssueStatistics
from crdqe.core.placeholder_processor import PlaceholderProcessor
# from crdqe.core.schema_detector import SchemaDetector


class CRDQEEngine:

    def __init__(self):

        self.settings = None
        self.workbook_path = None
        self.callback = None

    def log(self, message):

        if hasattr(self, "logger"):
            self.logger.info(message)
        else:
            print(message)

        if self.callback:
            self.callback(message)
    def run(
        self,
        workbook_path,
        worksheet,
        callback=None
    ):
        self.log(f"Workbook received : {workbook_path}")
        self.log(f"Worksheet received: {worksheet}")

        self.callback = callback
        self.workbook_path = Path(workbook_path)

        # -------------------------------------------------------
        # Load configuration
        # -------------------------------------------------------

        self.settings = ConfigManager().load()

        self.logger = Logger.setup()

        self.logger.info("=" * 60)
        self.logger.info("Civil Registration Data Quality Engine Started")

        # -------------------------------------------------------
        # File management
        # -------------------------------------------------------

        self.file_manager = FileManager(self.settings)

        self.file_manager.create_directories()

        if not Path(workbook_path).exists():

            self.logger.error(
                f"Workbook not found: {workbook_path}"
            )

            self.log("Workbook not found.")

            return False
        self.logger.info("Workbook found.")
        self.logger.info(workbook_path)
        # -------------------------------------------------------
        # Read workbook
        # -------------------------------------------------------

        self.reader = ExcelReader(
        workbook_path=workbook_path,
        worksheet=worksheet
        )

        self.logger.info(
        f"Available worksheets: {self.reader.get_sheet_names()}"
        )

        self.header_row = HeaderDetector.find_header_row(
        workbook_path,
        worksheet
        )

        self.logger.info(
        f"Detected Header Row: {self.header_row}"
        )

        self.df = self.reader.read(
        header=self.header_row
        )

        self.logger.info("Workbook loaded successfully.")
        self.logger.info(f"Rows: {len(self.df)}")
        self.logger.info(f"Columns: {len(self.df.columns)}")
        self.logger.info(list(self.df.columns))

        # -------------------------------------------------------
        # Standardize columns
        # -------------------------------------------------------

        self.df.columns = ColumnStandardizer.clean(
        self.df.columns
        )

        self.logger.info("Standardized Columns:")
        self.logger.info(self.df.columns.tolist())

        # -------------------------------------------------------
        # Detect dataset
        # -------------------------------------------------------

        dataset = DatasetDetector.detect(self.df.columns)

        self.dataset = dataset

        self.logger.info(
            f"Detected Dataset: {self.dataset}"
        )

        # -------------------------------------------------------
        # Map schema
        # -------------------------------------------------------

        BASE_DIR = Path(__file__).parents[2]

        if self.dataset == "Birth":

            schema_file = (
                BASE_DIR /
                "config" /
                "birth_schema.yaml"
            )

        elif self.dataset == "Death":

            schema_file = (
                BASE_DIR /
                "config" /
                "death_schema.yaml"
            )

        else:

            raise ValueError(
                f"Unknown dataset: {self.dataset}"
            )

        self.mapper = SchemaMapper(schema_file)
        self.schema = self.mapper.get_schema()

        self.df = self.mapper.map_columns(self.df)

        # detector = SchemaDetector(self.schema)

        # mapping, confidence = detector.detect(self.df.columns)

        # self.log("")
        # self.log("Detected Schema")

        # for column, field in mapping.items():
            # self.log(f"{column}  -->  {field} ({confidence[field]}%)")
        self.df = PlaceholderProcessor.process(
        self.df,
        self.schema
        )

        # -------------------------------------------------------
        # Convert datatypes
        # -------------------------------------------------------

        self.df = DataTypeProcessor.process(
            self.df,
            self.schema
        )

        # -------------------------------------------------------
        # Validate schema
        # -------------------------------------------------------

        self.validator = SchemaValidator()

        result = self.validator.validate(
            self.df,
            self.schema
        )

        self.logger.info(
            f"Schema Valid: {result['valid']}"
        )

        if result["missing"]:

            self.logger.warning(
                f"Missing Columns: {result['missing']}"
            )

        if result["extra"]:

            self.logger.info(
                f"Extra Columns: {result['extra']}"
            )

        self.logger.info(
            f"Rows: {len(self.df)}"
        )

        self.logger.info(
            f"Columns: {len(self.df.columns)}"
        )

        self.logger.info(
            self.df.columns.tolist()
        )

        # -------------------------------------------------------
        # Load rules
        # -------------------------------------------------------

        self.rules = RuleLoader.load(
            self.dataset,
            self.schema
        )

        # -------------------------------------------------------
        # Run Rule Engine
        # -------------------------------------------------------

        self.engine = RuleEngine(
            self.rules
        )

        self.df, self.issues_df = self.engine.run(
            self.df
        )


        self.issue_summary = IssueStatistics.generate(
            self.issues_df
        )

        self.log("Rule Engine completed.")
        self.log(
            f"Records processed: {len(self.df)}"
        )
        self.log(
            f"Issues found: {len(self.issues_df)}"
        )

        # -------------------------------------------------------
        # Collect Issues
        # -------------------------------------------------------

        self.collector = IssueCollector()

        self.collector.add(self.issues_df)

        self.issues_df = self.collector.to_dataframe()

        # -------------------------------------------------------
        # Write Excel Reports
        # -------------------------------------------------------

        self.writer = ExcelWriter(
            self.settings
        )

        self.writer.write_cleaned(
            self.df
        )

        self.writer.write_flags(
            self.issues_df
        )

        # -------------------------------------------------------
        # Generate Summary
        # -------------------------------------------------------

        summary = SummaryReport(
        self.df,
        self.issues_df
        )

        report = summary.generate()

        self.writer.write_summary(report)
        self.dataset = dataset
        self.records = len(self.df)
        self.issue_count = len(self.issues_df)
        return {
            "cleaned": self.df,
            "issues": self.issues_df,
            "summary": report
        }