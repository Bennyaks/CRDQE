"""
===========================================================
CRDQE Status Bar
-----------------------------------------------------------
Displays application status and progress.
===========================================================
"""

import tkinter as tk
from tkinter import ttk


class StatusBar(ttk.Frame):

    def __init__(self, parent):

        super().__init__(parent)

        self.parent = parent

        self.build()

    def build(self):

        self.columnconfigure(0, weight=1)

        self.status = tk.StringVar(
            value="Ready"
        )

        self.records = tk.StringVar(
            value="Records: 0"
        )

        self.issues = tk.StringVar(
            value="Issues: 0"
        )

        self.dataset = tk.StringVar(
            value="Dataset: None"
        )

        ttk.Separator(
            self,
            orient="horizontal"
        ).grid(
            row=0,
            column=0,
            columnspan=4,
            sticky="ew"
        )

        ttk.Label(
            self,
            textvariable=self.status
        ).grid(
            row=1,
            column=0,
            sticky="w",
            padx=10,
            pady=5
        )

        ttk.Label(
            self,
            textvariable=self.records
        ).grid(
            row=1,
            column=1,
            padx=10
        )

        ttk.Label(
            self,
            textvariable=self.issues
        ).grid(
            row=1,
            column=2,
            padx=10
        )

        ttk.Label(
            self,
            textvariable=self.dataset
        ).grid(
            row=1,
            column=3,
            padx=10
        )

        self.pack(
            side="bottom",
            fill="x"
        )

    def set_status(self, message):

        self.status.set(message)

    def set_records(self, count):

        self.records.set(f"Records: {count}")

    def set_issues(self, count):

        self.issues.set(f"Issues: {count}")

    def set_dataset(self, name):

        self.dataset.set(f"Dataset: {name}")

    def reset(self):

        self.status.set("Ready")
        self.records.set("Records: 0")
        self.issues.set("Issues: 0")
        self.dataset.set("Dataset: None")