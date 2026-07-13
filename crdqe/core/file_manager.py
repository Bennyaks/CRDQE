"""
===========================================================
Civil Registration Data Quality Engine (CRDQE)

Module:
File Manager

Purpose:
Manage folders and file paths.

Author:
Benard Mandera
===========================================================
"""

from pathlib import Path


class FileManager:
    """Handles folders and file paths."""

    def __init__(self, settings):
        print("FileManager received:", settings)
        self.settings = settings
    def create_directories(self):
        """Create output directory."""

        output = Path(self.settings["output"]["folder"])

        output.mkdir(parents=True, exist_ok=True)
