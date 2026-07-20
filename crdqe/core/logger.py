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
import yaml

from crdqe.utils.paths import BASE_DIR, CONFIG_DIR


class Logger:
    """
    Configure the application logging system.
    """

    @staticmethod
    def setup():
        # Ensure the log directory exists
        log_directory = BASE_DIR / "data" / "output" / "logs"
        log_directory.mkdir(parents=True, exist_ok=True)

        # Load logging configuration
        config_path = CONFIG_DIR / "logging.yaml"

        with open(config_path, "r", encoding="utf-8") as file:
            config = yaml.safe_load(file)

        # The YAML's file handler uses a relative "filename" path
        # (e.g. "data/output/logs/pipeline.log"). dictConfig() would
        # resolve that relative to whatever the current working
        # directory happens to be at runtime -- not BASE_DIR -- so
        # rewrite it to an absolute, anchored path before applying
        # the config. This keeps it working whether run from source
        # or from a launch shortcut with a different working directory.
        file_handler = config.get("handlers", {}).get("file")

        if file_handler and "filename" in file_handler:
            file_handler["filename"] = str(
                BASE_DIR / file_handler["filename"]
            )

        logging.config.dictConfig(config)

        return logging.getLogger("CRDQE")