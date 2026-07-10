"""
===========================================================
Writes output Excel files.
===========================================================
"""

from pathlib import Path

from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment
from openpyxl.utils import get_column_letter


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

    def cleaned(self, dataframe):

        dataframe.to_excel(
            self.cleaned_path,
            index=False
        )

        self._format(self.cleaned_path)

    def flags(self, dataframe):

        dataframe.to_excel(
            self.flags_path,
            index=False
        )

        self._format(self.flags_path)

    def summary(self, dataframe):

        dataframe.to_excel(
            self.summary_path,
            index=False
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