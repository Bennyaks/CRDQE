"""
===========================================================
Civil Registration Data Quality Engine (CRDQE)

Entry Point

Author:
Benard Mandera
===========================================================
"""

from crdqe.core.config_manager import ConfigManager
from crdqe.core.logger import Logger


def main():

    logger = Logger.setup()

    logger.info("=" * 60)
    logger.info("Civil Registration Data Quality Engine Started")

    config = ConfigManager()

    settings = config.load()

    logger.info("Configuration Loaded Successfully")

    logger.info(settings)


if __name__ == "__main__":
    main()