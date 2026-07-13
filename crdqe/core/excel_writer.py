"""
===========================================================
Writes output Excel files.
===========================================================
"""

from pathlib import Path

from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment
from openpyxl.utils import get_column_letter
import pandas as pd


class ExcelWriter:

    def __init__(self, settings):

        output = Path(settings["output"]["folder"])

        self.cleaned_path = (
            output /
            settings["output"]["cleaned_folder"] /
            "cleaned_data.xlsx"
        )

        self.flags_path = (
            output /
            settings["output"]["flags_folder"] /
            "flag_report.xlsx"
        )

        self.summary_path = (
            output /
            settings["output"]["summaries_folder"] /
            "summary_report.xlsx"
        )

    def write_cleaned(self, dataframe):

        df = dataframe.copy()

        date_columns = [
            "date_of_death",
            "registration_date"
        ]

        for col in date_columns:

            if col in df.columns:

                df[col] = (
                    df[col]
                    .dt.strftime("%d/%m/%Y")
                    .fillna("")
                )
            if "entry_number" in df.columns:

                df["entry_number"] = (
                    pd.to_numeric(
                        df["entry_number"],
                        errors="coerce"
                    )
                    .astype("Int64")
                )

        df.to_excel(
            self.cleaned_path,
            index=False
        )

        self._format(self.cleaned_path)

    def write_flags(self, dataframe):

        df = dataframe.copy()

        df.to_excel(
            self.flags_path,
            index=False
        )

        self._format(self.flags_path)

    def write_summary(self, report):

        metrics_df = pd.DataFrame({
            "Metric": [
                "Rows",
                "Columns",
                "Issues Found",
                "Quality Score (%)"
            ],
            "Value": [
                report["rows"],
                report["columns"],
                report["issues"],
                report["quality_score"]
            ]
        })

        field_df = pd.DataFrame(
            list(report["issues_by_field"].items()),
            columns=["Field", "Issues"]
        )

        rule_df = pd.DataFrame(
            list(report["issues_by_rule"].items()),
            columns=["Rule", "Issues"]
        )

        with pd.ExcelWriter(self.summary_path, engine="openpyxl") as writer:

            metrics_df.to_excel(
                writer,
                sheet_name="Summary",
                index=False,
                startrow=0
            )

            field_df.to_excel(
                writer,
                sheet_name="Summary",
                index=False,
                startrow=7
            )

            rule_df.to_excel(
                writer,
                sheet_name="Summary",
                index=False,
                startrow=7 + len(field_df) + 4
            )

        self._format(self.summary_path)

    def _format(self, path):

        workbook = load_workbook(path)

        worksheet = workbook.active

        header_fill = PatternFill(
            fill_type="solid",
            fgColor="1F4E78"
        )

        header_font = Font(
            bold=True,
            color="FFFFFF"
        )

        thin = Side(style="thin")

        border = Border(
            left=thin,
            right=thin,
            top=thin,
            bottom=thin
        )

        for cell in worksheet[1]:

            cell.fill = header_fill
            cell.font = header_font
            cell.border = border
            cell.alignment = Alignment(
                horizontal="center",
                vertical="center"
            )

        worksheet.freeze_panes = "A2"

        worksheet.auto_filter.ref = worksheet.dimensions

        for column in worksheet.columns:

            width = max(
                len(str(cell.value))
                if cell.value is not None
                else 0
                for cell in column
            )

            worksheet.column_dimensions[
                get_column_letter(column[0].column)
            ].width = min(width + 4, 50)

        workbook.save(path)