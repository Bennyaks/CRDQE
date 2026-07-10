"""
===========================================================
Civil Registration Data Quality Engine (CRDQE)

Module:
Excel Reader

Purpose:
Read Excel workbooks.

Author:
Benard Mandera
===========================================================
"""

from email import header
from pathlib import Path
import pandas as pd


class ExcelReader:

    def __init__(self, workbook_path, worksheet):
        self.workbook_path = Path(workbook_path)
        self.worksheet = worksheet

    def get_sheet_names(self):
        """Return all worksheet names."""

        workbook = pd.ExcelFile(
            self.workbook_path,
            engine="openpyxl"
        )

        return workbook.sheet_names

    def read(self, header=0):
        return pd.read_excel(
            self.workbook_path,
            sheet_name=self.worksheet,
            header=header,
            engine="openpyxl"
        )