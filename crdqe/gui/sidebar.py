"""
===========================================================
CRDQE Sidebar
-----------------------------------------------------------
Configuration panel for the application.

Responsibilities
----------------
- Workbook selection
- Worksheet selection
- Dataset selection
- Registration month selection
- Validation statistics display

The sidebar contains no business logic. It simply exposes
a clean API for MainWindow.
===========================================================
"""

import tkinter as tk
from tkinter import ttk
from tkinter import StringVar

from crdqe.gui.widgets import SectionFrame
from crdqe.gui.theme import Theme
from datetime import datetime

MONTHS = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
]


class Sidebar(ttk.Frame):

    def __init__(
        self,
        parent,
        browse_callback=None,
        worksheet_callback=None,
        dataset_callback=None,
        month_callback=None,
        year_callback=None
    ):

        current_year = datetime.now().year

        years = [
            str(year)
            for year in range(
                current_year - 10,
                current_year + 2
            )
        ]

        super().__init__(parent, padding=10)

        self.browse_callback = browse_callback
        self.worksheet_callback = worksheet_callback
        self.dataset_callback = dataset_callback
        self.month_callback = month_callback

        self.workbook = tk.StringVar()
        self.worksheet = tk.StringVar()
        self.dataset = tk.StringVar(value="Auto Detect")
        self.month = tk.StringVar(value="January")
        self.year = StringVar(value=str(datetime.now().year))

        self.records = tk.StringVar(value="0")
        self.issues = tk.StringVar(value="0")
        self.score = tk.StringVar(value="100%")
        

        self.build()

    # --------------------------------------------------

    def build(self):

        self.columnconfigure(0, weight=1)

        self._header()

        self._workbook_section()

        self._worksheet_section()

        self._dataset_section()

        self._month_section()

        self._statistics_section()

    # --------------------------------------------------

    def _header(self):

        ttk.Label(
            self,
            text="CRDQE",
            style="Title.TLabel"
        ).pack(pady=(5, 0))

        ttk.Label(
            self,
            text="Civil Registration\nData Quality Engine",
            justify="center"
        ).pack(pady=(0, 15))

    # --------------------------------------------------
    def get_workbook(self):
        return self.workbook.get()

    def _workbook_section(self):

        section = SectionFrame(self, "Workbook")

        section.pack(fill="x", pady=(0, 10))

        self.workbook_entry = ttk.Entry(
            section,
            textvariable=self.workbook,
            state="readonly"
        )

        self.workbook_entry.pack(
            fill="x",
            padx=5,
            pady=(5, 5)
        )

        ttk.Button(
            section,
            text="Browse...",
            command=self.browse_callback
        ).pack(
            fill="x",
            padx=5,
            pady=(0, 5)
        )
        

    # --------------------------------------------------

    def _worksheet_section(self):

        section = SectionFrame(self, "Worksheet")

        section.pack(fill="x", pady=(0, 10))
        ttk.Label(
            section,
            text="Select Worksheet"
        ).pack(anchor="w", padx=5, pady=(5, 0))

        self.worksheet_combo = ttk.Combobox(
            section,
            textvariable=self.worksheet,
            state="readonly",
            width=20
        )

        self.worksheet_combo.pack(
            fill="x",
            padx=5,
            pady=5
        )

        if self.worksheet_callback:

            self.worksheet_combo.bind(
                "<<ComboboxSelected>>",
                lambda e: self.worksheet_callback()
            )

    # --------------------------------------------------

    def _dataset_section(self):

        section = SectionFrame(self, "Dataset")

        section.pack(fill="x", pady=(0, 10))
        ttk.Label(
            section,
            text="Dataset"
        ).pack(anchor="w", padx=5, pady=(5, 0))

        self.dataset_combo = ttk.Combobox(
            section,
            textvariable=self.dataset,
            state="readonly",
            values=[
                "Auto Detect",
                "Birth",
                "Death"
            ]
        )

        self.dataset_combo.pack(
            fill="x",
            padx=5,
            pady=5
        )

        if self.dataset_callback:

            self.dataset_combo.bind(
                "<<ComboboxSelected>>",
                lambda e: self.dataset_callback()
            )
    # --------------------------------------------------

    def _month_section(self):

        section = SectionFrame(
            self,
            "Registration Period"
        )

        section.pack(fill="x", pady=(0, 15))

        ttk.Label(
            section,
            text="Registration Period"
        ).pack(anchor="w", padx=5, pady=(5, 0))

        period_frame = ttk.Frame(section)
        period_frame.pack(fill="x", padx=5, pady=5)

        # -------------------------
        # Month
        # -------------------------

        self.month_combo = ttk.Combobox(
            period_frame,
            textvariable=self.month,
            values=MONTHS,
            state="readonly",
            width=15
        )

        self.month_combo.current(0)

        self.month_combo.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 5)
        )

        # -------------------------
        # Year
        # -------------------------

        current_year = datetime.now().year

        years = [
            str(year)
            for year in range(
                current_year - 5,
                current_year + 6
            )
        ]

        self.year_combo = ttk.Combobox(
            period_frame,
            textvariable=self.year,
            values=years,
            state="readonly",
            width=8
        )

        self.year_combo.set(str(current_year))

        self.year_combo.pack(
            side="left",
            padx=(5, 0)
        )

        # -------------------------
        # Events
        # -------------------------

        if self.month_callback:

            self.month_combo.bind(
                "<<ComboboxSelected>>",
                lambda e: self.month_callback()
            )

            self.year_combo.bind(
                "<<ComboboxSelected>>",
                lambda e: self.month_callback()
            )
        
    # --------------------------------------------------


    def _statistics_section(self):

        section = SectionFrame(
            self,
            "Validation Statistics"
        )

        section.pack(
            fill="x",
            expand=True
        )

        self._stat_row(
            section,
            "Records",
            self.records
        )

        self._stat_row(
            section,
            "Issues",
            self.issues
        )

        self._stat_row(
            section,
            "Quality Score",
            self.score
        )

    # --------------------------------------------------

    def _stat_row(
        self,
        parent,
        label,
        variable
    ):

        frame = ttk.Frame(parent)

        frame.pack(
            fill="x",
            padx=5,
            pady=3
        )

        ttk.Label(
            frame,
            text=f"{label}:"
        ).pack(
            side="left"
        )

        ttk.Label(
            frame,
            textvariable=variable,
            style="Header.TLabel"
        ).pack(
            side="right"
        )

    # ==================================================
    # Public API
    # ==================================================

    def set_workbook(self, path):

        self.workbook.set(path)

    def set_worksheets(self, worksheets):

        self.worksheet_combo["values"] = worksheets

        if worksheets:
            self.worksheet_combo.current(0)
            self.worksheet.set(worksheets[0])

    def get_selected_worksheet(self):
        return self.worksheet_combo.get()

    def get_selected_dataset(self):
        return self.dataset_combo.get()

    def get_selected_month(self):
        return self.month_combo.get()
    def get_selected_year(self):
        return self.year_combo.get()


    def update_statistics(
        self,
        records,
        issues,
        score
    ):

        self.records.set(records)
        self.issues.set(issues)
        self.score.set(score)
        
    def set_dataset(self, dataset):
        self.dataset.set(dataset)

    def reset(self):

        self.workbook.set("")
        self.worksheet.set("")
        self.dataset.set("Auto Detect")
        self.month.set("January")
        self.year.set("2026")

        self.records.set("0")
        self.issues.set("0")
        self.score.set("100%")