"""
===========================================================
CRDQE Dashboard
-----------------------------------------------------------
Main dashboard shown on application startup.
===========================================================
"""

from tkinter import ttk

from crdqe.gui.widgets import SectionFrame, InfoCard


class Dashboard(ttk.Frame):

    def __init__(
        self,
        parent,
        open_callback=None,
        validate_callback=None,
        report_callback=None
    ):

        super().__init__(parent, padding=10)

        self.open_callback = open_callback
        self.validate_callback = validate_callback
        self.report_callback = report_callback

        self.build()

    # ----------------------------------------------------

    def build(self):

        self.columnconfigure(0, weight=1)

        self._statistics()

    # ----------------------------------------------------

    def _statistics(self):

        section = SectionFrame(self, "Validation Overview")

        section.pack(fill="x", pady=(0, 10))

        cards = ttk.Frame(section)

        cards.pack(fill="x", padx=5, pady=5)

        cards.columnconfigure((0, 1, 2, 3), weight=1)

        self.records = InfoCard(cards, "Records", "0")
        self.issues = InfoCard(cards, "Issues", "0")
        self.current = InfoCard(cards, "Current", "0")
        self.late = InfoCard(cards, "Late", "0")

        self.records.grid(row=0, column=0, padx=8, sticky="ew")
        self.issues.grid(row=0, column=1, padx=8, sticky="ew")
        self.current.grid(row=0, column=2, padx=8, sticky="ew")
        self.late.grid(row=0, column=3, padx=8, sticky="ew")

    # ----------------------------------------------------

    def update_statistics(
        self,
        records,
        issues,
        current,
        late
    ):

        self.records.set(records)
        self.issues.set(issues)
        self.current.set(current)
        self.late.set(late)