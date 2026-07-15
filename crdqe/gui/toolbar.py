"""
===========================================================
CRDQE Toolbar
-----------------------------------------------------------
Contains the main application actions.
===========================================================
"""

import tkinter as tk
from tkinter import ttk


class Toolbar(ttk.Frame):

    def __init__(self, parent):

        super().__init__(parent, padding=10)

        self.parent = parent

        self.build()

    def build(self):

        self.columnconfigure(10, weight=1)

        self.open_button = ttk.Button(
            self,
            text="📂 Open Workbook",
            command=self.parent.browse_workbook,
            width=18
        )

        self.open_button.grid(
            row=0,
            column=0,
            padx=5
        )

        self.run_button = ttk.Button(
            self,
            text="▶ Run Validation",
            command=self.parent.run_validation,
            width=18
        )

        self.run_button.grid(
            row=0,
            column=1,
            padx=5
        )

        self.report_button = ttk.Button(
            self,
            text="📊 Open Report",
            command=self.parent.open_report,
            width=18
        )

        self.report_button.grid(
            row=0,
            column=2,
            padx=5
        )

        self.clear_button = ttk.Button(
            self,
            text="🗑 Clear Log",
            command=self.parent.clear_log,
            width=15
        )

        self.clear_button.grid(
            row=0,
            column=3,
            padx=5
        )

        self.pack(fill="x")