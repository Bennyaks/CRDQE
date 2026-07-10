"""
===========================================================
Civil Registration Data Quality Engine (CRDQE)

Module:
Configuration Manager

Purpose:
Loads and validates user configuration.

Author:
Benard Mandera
===========================================================
"""

from pathlib import Path
import yaml


class ConfigManager:

    def __init__(self, config_path="config/settings.yaml"):
        self.config_path = Path(config_path)
        self.settings = None

    def load(self):

        if not self.config_path.exists():
            raise FileNotFoundError(
                f"Configuration file not found: {self.config_path}"
            )

        with open(self.config_path, "r", encoding="utf-8") as file:
            self.settings = yaml.safe_load(file)

        return self.settings