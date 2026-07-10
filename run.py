"""
===========================================================
Civil Registration Data Quality Engine (CRDQE)

Entry Point

Author:
Benard Mandera
===========================================================
"""

from crdqe.core.config_manager import ConfigManager


def main():

    print("=" * 60)
    print("Civil Registration Data Quality Engine")
    print("=" * 60)

    config = ConfigManager()

    settings = config.load()

    print("\nConfiguration Loaded Successfully\n")

    print(settings)


if __name__ == "__main__":
    main()