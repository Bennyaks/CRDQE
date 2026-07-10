"""
===========================================================
Civil Registration Data Quality Engine (CRDQE)

Module:
Logger

Purpose:
Configure application logging.

Author:
Benard Mandera
===========================================================
"""

import logging
import logging.config
from pathlib import Path
import yaml


class Logger:
    """
    Configure the application logging system.
    """

    @staticmethod
    def setup():
        # Ensure the log directory exists
        log_directory = Path("data/output/logs")
        log_directory.mkdir(parents=True, exist_ok=True)

        # Load logging configuration
        config_path = Path("config/logging.yaml")

        with open(config_path, "r", encoding="utf-8") as file:
            config = yaml.safe_load(file)

        logging.config.dictConfig(config)

        return logging.getLogger("CRDQE")