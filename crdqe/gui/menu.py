"""
===========================================================
CRDQE Menu Bar
-----------------------------------------------------------
Application menu.
===========================================================
"""

import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from pathlib import Path
import subprocess
import os


class MenuBar:

    def __init__(
        self,
        parent,
        open_callback=None,
        validate_callback=None,
        output_folder=None
    ):

        self.parent = parent

        self.open_callback = open_callback
        self.validate_callback = validate_callback
        self.output_folder = output_folder

        self.menu = tk.Menu(parent)

        self.build()

    def build(self):

        self.build_file_menu()

        self.build_tools_menu()

        self.build_reports_menu()

        self.build_help_menu()

        self.parent.config(menu=self.menu)

    # -----------------------------------------------------
    # FILE
    # -----------------------------------------------------

    def build_file_menu(self):

        file_menu = tk.Menu(
            self.menu,
            tearoff=0
        )

        file_menu.add_command(
            label="Open Workbook...",
            command=self.open_workbook
        )

        file_menu.add_separator()

        file_menu.add_command(
            label="Save Cleaned Data"
        )

        file_menu.add_command(
            label="Open Output Folder",
            command=self.open_output_folder
        )
        file_menu.add_separator()

        file_menu.add_command(
            label="Exit",
            command=self.parent.quit
        )

        self.menu.add_cascade(
            label="File",
            menu=file_menu
        )

    # -----------------------------------------------------
    # TOOLS
    # -----------------------------------------------------

    def build_tools_menu(self):

        tools_menu = tk.Menu(
            self.menu,
            tearoff=0
        )

        tools_menu.add_command(
            label="Validate Workbook",
            command=self.validate_workbook
        )

        tools_menu.add_command(
            label="Detect Dataset"
        )

        tools_menu.add_separator()

        tools_menu.add_command(
            label="Settings"
        )

        self.menu.add_cascade(
            label="Tools",
            menu=tools_menu
        )

    # -----------------------------------------------------
    # REPORTS
    # -----------------------------------------------------

    def build_reports_menu(self):

        report_menu = tk.Menu(
            self.menu,
            tearoff=0
        )

        report_menu.add_command(
            label="Validation Report"
        )

        report_menu.add_command(
            label="Open Output Folder"
        )

        self.menu.add_cascade(
            label="Reports",
            menu=report_menu
        )

    # -----------------------------------------------------
    # HELP
    # -----------------------------------------------------

    def build_help_menu(self):

        help_menu = tk.Menu(
            self.menu,
            tearoff=0
        )

        help_menu.add_command(
            label="User Guide"
        )

        help_menu.add_command(
            label="About CRDQE",
            command=self.show_about
        )

        self.menu.add_cascade(
            label="Help",
            menu=help_menu)
        # --------------------------------------------------
    # MENU ACTIONS
    # --------------------------------------------------

    def open_workbook(self):

        if self.open_callback:

            self.open_callback()

    def validate_workbook(self):

        if self.validate_callback:

            self.validate_callback()

    def open_output_folder(self):

        if not self.output_folder:

            messagebox.showinfo(
                "Output Folder",
                "Output folder not configured."
            )
            return

        folder = Path(self.output_folder)

        if not folder.exists():

            messagebox.showwarning(
                "Output Folder",
                "Folder does not exist."
            )
            return

        os.startfile(folder)

    def show_about(self):

        messagebox.showinfo(

            "About CRDQE",

            "Civil Registration Data Quality Engine\n\n"

            "Version 1.0\n"

            "Developed by Benard Mandera\n"

            "Python • Pandas • OpenPyXL"
        )