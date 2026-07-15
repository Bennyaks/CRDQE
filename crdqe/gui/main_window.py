"""
===========================================================
CRDQE Main Window
-----------------------------------------------------------
Top-level application window. Creates the theme, menu,
toolbar, sidebar, dashboard and status bar, and wires them
together with the validation engine.
===========================================================
"""

import os
import threading
import tkinter as tk
from tkinter import filedialog

from crdqe.gui.theme import Theme
from crdqe.gui.menu import MenuBar
from crdqe.gui.toolbar import Toolbar
from crdqe.gui.status_bar import StatusBar
from crdqe.gui.dashboard import Dashboard
from crdqe.gui.dialogs import Dialogs
from crdqe.gui.widgets import LogConsole, ProgressFrame

from crdqe.core.engine import Engine


OUTPUT_FOLDER = "output"


class MainWindow(tk.Tk):

    def __init__(self):

        super().__init__()

        self.title("CRDQE - Civil Registration Data Quality Engine")
        self.geometry("1200x750")
        self.minsize(1000, 650)

        self.workbook_path = None
        self.worksheet = None

        self.engine = Engine()

        Theme.configure()

        self.build()

    # ------------------------------------------------------
    # BUILD
    # ------------------------------------------------------

    def build(self):

        self.menu = MenuBar(
            self,
            open_callback=self.browse_workbook,
            validate_callback=self.run_validation,
            output_folder=OUTPUT_FOLDER
        )

        self.toolbar = Toolbar(self)

        self._build_body()

        self.status_bar = StatusBar(self)

    def _build_body(self):

        body = tk.Frame(self, bg=Theme.BACKGROUND)

        body.pack(fill="both", expand=True)

        body.columnconfigure(1, weight=1)
        body.rowconfigure(0, weight=1)

        # ---- Sidebar ------------------------------------
        # PLACEHOLDER: sidebar.py has not been supplied yet.
        # Once available, replace this frame with:
        #     self.sidebar = Sidebar(body, ...)
        self.sidebar = tk.Frame(body, width=220, bg=Theme.LIGHT)
        self.sidebar.grid(row=0, column=0, sticky="ns")
        self.sidebar.grid_propagate(False)

        # ---- Main content --------------------------------
        content = tk.Frame(body, bg=Theme.BACKGROUND)

        content.grid(row=0, column=1, sticky="nsew")

        content.columnconfigure(0, weight=1)
        content.rowconfigure(2, weight=1)

        self.dashboard = Dashboard(
            content,
            open_callback=self.browse_workbook,
            validate_callback=self.run_validation,
            report_callback=self.open_report
        )

        self.dashboard.grid(row=0, column=0, sticky="ew")

        self.progress = ProgressFrame(content)

        self.progress.grid(row=1, column=0, sticky="ew", padx=20, pady=(10, 0))

        self.log = LogConsole(content)

        self.log.grid(row=2, column=0, sticky="nsew", padx=20, pady=(10, 20))

    # ------------------------------------------------------
    # ACTIONS
    # ------------------------------------------------------

    def browse_workbook(self):

        path = filedialog.askopenfilename(
            title="Select Workbook",
            filetypes=[("Excel Workbook", "*.xlsx *.xlsm")]
        )

        if not path:
            return

        self.workbook_path = path

        self.status_bar.set_dataset(os.path.basename(path))
        self.status_bar.set_status("Workbook loaded")
        self.log.append(f"Loaded workbook: {path}")

    def run_validation(self):

        if not self.workbook_path:

            Dialogs.warning(
                "No Workbook",
                "Please open a workbook before running validation."
            )
            return

        self.status_bar.set_status("Validating...")
        self.progress.start()
        self.toolbar.run_button.configure(state="disabled")

        thread = threading.Thread(
            target=self._run_validation_thread,
            daemon=True
        )

        thread.start()

    def _run_validation_thread(self):

        try:

            result = self.engine.run(
                workbook_path=self.workbook_path,
                worksheet=self.worksheet,
                callback=lambda msg: self.after(0, self.log.append, msg)
            )

            self.after(0, self._on_validation_complete, result)

        except Exception as exc:

            self.after(0, self._on_validation_error, exc)

    def _on_validation_complete(self, result):

        self.progress.stop()
        self.toolbar.run_button.configure(state="normal")
        self.status_bar.set_status("Validation complete")

        # NOTE: adjust these lookups to match whatever `Engine.run()`
        # actually returns (object attributes, dict keys, etc.)
        records = getattr(result, "records", 0)
        issues = getattr(result, "issues", 0)
        current = getattr(result, "current", 0)
        late = getattr(result, "late", 0)

        self.status_bar.set_records(records)
        self.status_bar.set_issues(issues)
        self.dashboard.update_statistics(records, issues, current, late)

        Dialogs.info(
            "Validation Complete",
            f"Processed {records} records, found {issues} issues."
        )

    def _on_validation_error(self, exc):

        self.progress.stop()
        self.toolbar.run_button.configure(state="normal")
        self.status_bar.set_status("Validation failed")

        self.log.append(f"ERROR: {exc}")

        Dialogs.error("Validation Error", str(exc))

    def open_report(self):

        if not os.path.exists(OUTPUT_FOLDER):

            Dialogs.warning("Report", "No report has been generated yet.")
            return

        os.startfile(OUTPUT_FOLDER)

    def clear_log(self):

        self.log.clear()